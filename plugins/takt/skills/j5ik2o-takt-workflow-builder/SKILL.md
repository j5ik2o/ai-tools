---
name: j5ik2o-takt-workflow-builder
description: >
  TAKTワークフロー（ワークフローYAML）の作成・カスタマイズスキル。Faceted Prompting
  （Persona/Policy/Instruction/Knowledge/Output Contract）に基づくファセット群の
  生成を含む。references/taktにあるtaktのソースコード・ドキュメント・ビルトインワークフロー群を
  参照資料として活用する。ユーザーの要件をヒアリングし、step構成、ルール設計、
  ファセットファイル生成を一括で行う。
  トリガー：「ワークフローを作りたい」「ワークフローを定義」「taktのワークフローを作成」
  「新しいtaktワークフローを作って」「takt workflow」「ワークフローYAML」
---

# TAKT Workflow Builder

TAKTワークフロー（ワークフローYAML）とその関連ファセットファイルを作成する。

> **前提 takt バージョン**: v0.73.0

## 参照資料

taktのコードベースとドキュメントは `references/takt/` にある。必要に応じて以下を参照する。

| 資料 | パス | 用途 |
|------|------|------|
| YAMLスキーマ | `references/takt/builtins/skill/references/yaml-schema.md` | ワークフローYAMLの構造定義 |
| エンジン仕様 | `references/takt/builtins/skill/references/engine.md` | プロンプト構築・ルール評価の詳細 |
| Faceted Prompting | `references/takt/docs/faceted-prompting.ja.md` | 5ファセット設計の理論 |
| ビルトインワークフロー | `references/takt/builtins/ja/workflows/` | 実例（default.yaml, dual.yaml等） |
| スタイルガイド | `references/takt/builtins/ja/STYLE_GUIDE.md` | ファセット記述規約 |
| ペルソナガイド | `references/takt/builtins/ja/PERSONA_STYLE_GUIDE.md` | ペルソナ記述規約 |
| ビルトインファセット | `references/takt/builtins/ja/facets/{personas,policies,instructions,knowledge,output-contracts}/` | 既存ファセット例 |

**重要**: ワークフロー作成前に `references/takt/builtins/ja/workflows/default.yaml` を読み、プロジェクトのパターンを把握する。

## ワークフロー

### Step 1: 要件ヒアリング

以下を確認する（不明な点はユーザーに質問）:

1. **目的**: このワークフローで何を達成するか
2. **ステップ構成**: どんなステップが必要か（plan→implement→review→supervise等）
3. **レビュー体制**: 並列レビューの有無、レビュアーの種類
4. **ループ制御**: 修正ループの有無と閾値
5. **出力先**: ワークフローとファセットの配置場所（デフォルト: `~/.takt/workflows/`）

### Step 2: ビルトイン参照

ビルトインワークフロー（`references/takt/builtins/ja/workflows/`）から類似パターンを探す。

| ビルトイン | 用途 |
|-----------|------|
| `default.yaml` | 標準開発（plan→実装→並列レビュー→修正→supervise） |
| `dual.yaml` | フロントエンド＋バックエンド並列実装 |
| `backend.yaml` / `backend-mini.yaml` | バックエンド特化 / 最小構成 |
| `backend-cqrs.yaml` / `backend-cqrs-mini.yaml` | CQRS/ES特化 / 最小構成 |
| `backend-maintenance.yaml` | バックエンド保守 |
| `frontend.yaml` / `frontend-mini.yaml` | フロントエンド特化 / 最小構成 |
| `frontend-maintenance.yaml` | 既存フロントエンド保守 |
| `dual-cqrs.yaml` / `dual-cqrs-mini.yaml` / `dual-mini.yaml` | デュアル CQRS / 最小構成 |
| `review.yaml` / `review-backend.yaml` / `review-dual.yaml` / `review-frontend.yaml` | コードレビューワークフロー |
| `review-backend-cqrs.yaml` / `review-dual-cqrs.yaml` | CQRS 系コードレビュー |
| `review-fix.yaml` / `review-fix-backend.yaml` / `review-fix-dual.yaml` / `review-fix-frontend.yaml` | レビュー＋修正ループ |
| `review-fix-backend-cqrs.yaml` / `review-fix-dual-cqrs.yaml` / `review-fix-simple.yaml` | CQRS / シンプル 版レビュー＋修正 |
| `takt-default.yaml` / `takt-default-team.yaml` | TAKT開発用 / チーム構成版 |
| `review-takt-default.yaml` / `review-fix-takt-default.yaml` / `takt-development-review.yaml` | TAKT開発用レビュー |
| `peer-review.yaml` / `single-review-suite.yaml` | peer review |
| `peer-review-suite-base.yaml` / `peer-review-suite-cqrs.yaml` / `peer-review-suite-frontend.yaml` / `peer-review-suite-frontend-cqrs.yaml` | peer review suite（callable）|
| `development-implement.yaml` / `development-implement-team.yaml` / `development-implement-dynamic.yaml` | 実装フェーズ（callable）|
| `development-remediation.yaml` / `development-remediation-team.yaml` / `development-remediation-dynamic.yaml` | remediation フェーズ（callable）|
| `development-review.yaml` / `development-core.yaml` / `mini-core.yaml` | 開発コアフロー |
| `simple.yaml` / `simple-backend.yaml` / `simple-frontend.yaml` / `simple-core.yaml` | シンプル構成 |
| `simple-dual.yaml` / `simple-cqrs.yaml` / `simple-dual-cqrs.yaml` / `simple-mini.yaml` | シンプル dual / CQRS 系 |
| `maintenance.yaml` | 保守フロー |
| `audit-architecture.yaml` / `audit-architecture-backend.yaml` / `audit-architecture-dual.yaml` / `audit-architecture-frontend.yaml` | アーキテクチャ監査 |
| `audit-e2e.yaml` / `audit-security.yaml` / `audit-unit.yaml` | E2E/セキュリティ/ユニットテスト監査 |
| `review-remediation.yaml` | レビュー後 remediation |
| `merge-review.yaml` / `merge-review-fix.yaml` / `merge-review-fix-simple.yaml` | PR マージ系レビュー |
| `final-gate.yaml` | 最終ゲート（callable）|
| `loop-analysis.yaml` | ループ分析 |
| `pure.yaml` | 純粋レビュー |
| `terraform.yaml` | Terraform インフラストラクチャ |
| `research.yaml` / `deep-research.yaml` | 調査・研究 |
| `magi.yaml` / `compound-eye.yaml` | 多視点分析 |
| `auto-improvement-loop.yaml` | system step を使う自己改善ループ |
| `caccia.yaml` | Caccia 統合 |
| `cli.yaml` | CLI ツール開発 |
| `workflow-maker.yaml` | ワークフロー自動生成 |

**v0.73.0 で追加・変更された代表例**:
- **BREAKING**: `workflow_config: provider_options:` → `capabilities:` に変更。provider / model / options は runtime.yaml が所有し、ワークフロー YAML では `capabilities` で能力プリセットのみを参照する（同梱プリセット: `readonly` / `edit` / `enable-skills`）
- **BREAKING**: `review-default.yaml` → `review.yaml`、`review-fix-default.yaml` → `review-fix.yaml` にリネーム
- **BREAKING**: Finding Contract（`finding_contract:` セクション、`takt-default-with-fc`、`peer-review-with-fc`）廃止
- `session: compact` 追加。保存済み persona session を resume したうえで Phase 1 前だけ圧縮 capability を呼び出す
- `uses: <name>` で `steps/<name>.yaml` の step fragment を参照可能（top-level agent / workflow_call / parallel で利用可能）
- `input_reports:` フィールド追加。同一 workflow の完了済み step からレポートを受け取る
- Team Leader step（`team_leader:` キー）追加。タスクを独立 part に分解して並列実行
- `command_gates: required / skip` フィールドを rule に追加。`required`（省略時）では command gate を実行、`skip` ではスキップ
- ルール評価: `ai("...")` 廃止 → 意味ラベル（semantic label）の YAML 順 first-match 評価に変更
- `loop_monitors[].ignore_steps` 追加。サイクル照合から除外する中間 step を指定可能
- `instruction` フィールドが配列指定に対応（複数 facet 参照を `\n\n---\n\n` で結合）
- 新規ワークフロー多数追加: `development-*`, `simple-*`, `peer-review-suite-*`, `merge-review*`, `backend-maintenance`, `maintenance`, `final-gate`, `loop-analysis`, `pure`, `caccia`, `cli`, `workflow-maker` 等

**再利用判断**: ビルトインのファセットで足りる場合はカスタムファセットを作らない。

### Step 3: ワークフローYAML作成

以下の構造でYAMLを作成する。

```yaml
name: workflow-name
description: ワークフローの説明
max_steps: 30
initial_step: plan

# ワークフロー全体の設定
workflow_config:
  provider_options:
    codex:
      network_access: true

# セクションマップ（カスタムファセットがある場合のみ）
personas:
  custom-role: ../personas/custom-role.md
policies:
  custom-policy: ../policies/custom-policy.md
instructions:
  custom-step: ../instructions/custom-step.md
knowledge:
  domain: ../knowledge/domain.md
report_formats:
  custom-report: ../output-contracts/custom-report.md

steps:
  - name: plan
    edit: false
    persona: planner          # ビルトイン参照（bare name）
    knowledge: architecture
    provider_options:
      claude:
        allowed_tools:
          - Read
          - Glob
          - Grep
          - Bash
          - WebSearch
          - WebFetch
    instruction: plan
    output_contracts:
      report:
        - name: 00-plan.md
          format: plan
    rules:
      - condition: 要件が明確で実装可能
        next: implement
      - condition: 要件が不明確、情報不足
        next: ABORT

  - name: implement
    edit: true
    persona: coder
    policy: [coding, testing]
    session: refresh
    instruction: implement
    rules:
      - condition: 実装完了
        next: review
```

**`provider_options.extends` による共通化（v0.47.0〜、旧 `$ref` は廃止）**: `provider_options` は bare name でビルトインプリセットや `.takt/provider-options/` のカスタム YAML を参照できる。inline 値が同じ leaf を上書きする。ビルトインプリセット: `edit`, `review-readonly`, `review-files`, `review-web`。

```yaml
# プリセットを参照（claude + opencode の両方に allowed_tools が設定される）
provider_options:
  extends: review-readonly

# プリセットを参照しつつ一部を上書き
provider_options:
  extends: edit
  opencode:
    allowed_tools: [read, grep, bash]
```

**注意**: 旧用語エイリアス（`movements`, `initial_movement`, `max_movements`, `piece_config`, `piece_categories`）は引き続き使用不可。正式名のみ使用する。

#### Parallel Step 例

```yaml
  - name: reviewers
    parallel:
      - name: arch-review
        edit: false
        tags: [review]            # v0.47.0〜: provider_routing.tags でルーティング可能
        persona: architecture-reviewer
        policy: review
        instruction: review-arch
        output_contracts:
          report:
            - name: 05-architect-review.md
              format: architecture-review
        rules:
          - condition: approved
          - condition: needs_fix
      - name: qa-review
        edit: false
        tags: [review]
        persona: qa-reviewer
        policy: [review, qa]
        instruction: review-qa
        rules:
          - condition: approved
          - condition: needs_fix
    rules:
      - condition: all("approved")
        next: supervise
      - condition: any("needs_fix")
        next: fix
```

**注意**: サブステップの `rules` は結果分類用。`next` は無視され、親の `rules` が遷移先を決定する。

#### Finding Contract 例（v0.47.0〜）

ワークフロートップレベルに `finding_contract:` を追加すると、review findings の構造化ライフサイクル管理（ledger、severity、deduplication）が有効になる。`peer-review-with-fc.yaml` のような callable ワークフローを `call:` ステップで呼び出す構成が推奨。

```yaml
name: takt-default-with-fc
description: Finding Contract付きワークフロー例
initial_step: plan
max_steps: 30

finding_contract:
  ledger_path: .takt/findings-ledger.yaml      # 既知/修正済みfindingを蓄積するledger
  raw_findings_path: .takt/raw-findings.yaml   # レビュー結果の生findings出力先
  manager:
    persona: findings-manager                   # ビルトイン: finding照合・判定ペルソナ
    instruction: findings-manager               # ビルトイン: findings-manager instruction
    output_contract: findings-manager           # ビルトイン: findings-manager output contract

steps:
  - name: plan
    tags: [plan]
    edit: false
    persona: planner
    instruction: plan
    rules:
      - condition: 実装可能
        next: implement

  - name: implement
    tags: [coding]
    edit: true
    persona: coder
    instruction: implement
    rules:
      - condition: 実装完了
        next: peer-review

  - name: peer-review
    call: peer-review-with-fc   # Finding Contract付き callable ワークフロー
    rules:
      - condition: approved
        next: supervise
      - condition: needs_fix
        next: fix
```

#### 設計判断ガイド

| 判断ポイント | 基準 |
|-------------|------|
| `edit: true/false` | コード変更するステップのみtrue |
| `session: refresh` | 実装系ステップで新規セッション開始 |
| `pass_previous_response: false` | レビュー結果を直接読ませたくない場合 |
| `required_permission_mode` | edit権限が必要な場合に `edit` を指定 |
| `provider_options.claude.allowed_tools` | ステップ単位でClaudeの使用ツールを制限 |
| `provider_options.opencode.allowed_tools` | ステップ単位でOpenCodeの使用ツールを制限（lowercase: `read`, `glob`, `grep`, `bash` 等） |
| `provider_options.kiro.agent` | Kiro CLI の custom agent 名を指定（`kiro-cli chat --agent` として渡される） |
| `provider_options.extends` | bare name でプリセット YAML を参照（3層リゾルバー: `.takt/provider-options/` → `~/.takt/provider-options/` → builtin。inline 値が leaf を上書き。旧 `$ref` は v0.47.0 で廃止） |
| `provider_options.<provider>.effort` | 思考深度を上げる場合に指定。モデル互換性を確認する |
| `quality_gates` | agent step の完了条件。文字列 gate と `type: command` gate を混在可能 |
| `tags` | step / parallel サブステップのタグ配列（例: `[plan]`, `[coding]`, `[review]`）。`provider_routing.tags` でタグ単位のプロバイダー/モデル指定に使用 |
| `finding_contract` | ワークフロートップレベルに追加して Finding Contract を有効化。`ledger_path`, `raw_findings_path`, `manager`（`persona`/`instruction`/`output_contract`）を指定する |

#### ルール設計

| ルール種別 | 記法 | 使い分け |
|-----------|------|----------|
| テキスト条件 | `"条件文"` | Phase 3タグ判定（推奨） |
| AI判定 | `ai("条件")` | タグ判定が不適な場合 |
| 全一致 | `all("条件")` | parallelの親のみ |
| いずれか | `any("条件")` | parallelの親のみ |
| 決定論的条件 | `when: <expr>` | AI不要のルーティング（`condition:` 不要） |

`when:` は比較演算子（`==`, `!=`, `>`, `<`, `>=`, `<=`）、ブール論理（`&&`, `\|\|`）、ワークフロー状態参照（`context.*`, `structured.*`, `effect.*`）を使用可能。

特殊遷移先: `COMPLETE`（成功終了）、`ABORT`（失敗終了）

#### サブワークフロー呼び出し（`call:` ステップ）

別のワークフローをサブルーチンとして呼び出す。

```yaml
steps:
  - name: run-sub
    call: sub-workflow-name    # 呼び出し先ワークフロー名
    overrides:                  # プロバイダ/モデル上書き（任意）
      provider_options:
        claude:
          model: claude-opus-4-5
    rules:
      - condition: completed
        next: next-step
```

- 呼び出し先には `subworkflow: { callable: true }` が必要
- 再帰呼び出し検知あり、最大ネスト深度: 5

#### システムステップ（`kind: system`）

AIエージェントを介さず実行されるステップ。副作用（PR作成・タスクキュー操作等）を実行する。

```yaml
steps:
  - name: enqueue
    kind: system
    system_inputs:
      task: context.task        # ランタイムコンテキストをバインド
    effects:
      - type: enqueue_task
        workflow: default
    rules:
      - when: "effect.enqueued == true"
        next: next-step
```

`effects` の種別: `enqueue_task`, `comment_pr`, `sync_with_root`, `resolve_conflicts_with_ai`, `merge_pr`

#### 構造化出力（`structured_output:`）

ステップ出力をJSON スキーマでバリデーション・保存する。

```yaml
schemas:
  review-result:
    type: object
    properties:
      approved: { type: boolean }
      issues: { type: array, items: { type: string } }

steps:
  - name: review
    instruction: review
    structured_output:
      schema_ref: review-result   # schemas: マップのキーを参照
    rules:
      - when: "structured.review.approved == true"
        next: COMPLETE
      - condition: needs_fix
        next: fix
```

他ステップから `{structured:step-name.field}` でテンプレート参照可能。

### Step 4: ファセットファイル作成

カスタムファセットが必要な場合、以下の規約で作成する。

#### ディレクトリ構造

```
~/.takt/
├── workflows/
│   └── my-workflow.yaml
├── personas/
│   └── custom-role.md
├── policies/
│   └── custom-policy.md
├── instructions/
│   └── custom-step.md
├── knowledge/
│   └── domain.md
└── output-contracts/
    └── custom-report.md
```

#### ファセット作成規約

**Persona**: system promptに配置。identity + 専門性 + 境界。

```markdown
# {ロール名}

{1-2文のロール定義}

## 役割の境界

**やること:**
- ...

**やらないこと:**
- ...（担当エージェント名を明記）

## 行動姿勢

- ...
```

**Policy**: 複数ステップで共有する行動規範。

```markdown
# {ポリシー名}

## 原則

| 原則 | 基準 |
|------|------|
| ... | REJECT / APPROVE 判定 |

## 禁止事項

- ...
```

**Instruction**: ステップ固有の手順。命令形で記述。`{task}`, `{previous_response}`は自動注入されるため不要。

**Knowledge**: 判断の前提となる参照情報。記述的（「こうなっている」）。

**Output Contract**: レポートの構造定義。

````markdown
```markdown
# {レポートタイトル}

## 結果: APPROVE / REJECT

## サマリー
{1-2文で要約}

## 詳細
| 観点 | 結果 | 備考 |
|------|------|------|
```
````

詳細なスタイル規約は `references/takt/builtins/ja/STYLE_GUIDE.md` を参照。

### Step 5: Loop Monitor（任意）

修正ループが想定される場合に設定する。

```yaml
loop_monitors:
  - cycle: [ai_antipattern_review, ai_antipattern_fix]
    threshold: 3
    judge:
      persona: supervisor
      instruction: loop-monitor-ai-antipattern-fix   # ビルトインファセット参照
      rules:
        - condition: 健全（進捗あり）
          next: ai_antipattern_review
        - condition: 非生産的（改善なし）
          next: reviewers
  - cycle: [reviewers, fix]
    threshold: 3
    judge:
      persona: supervisor
      instruction: loop-monitor-reviewers-fix        # ビルトインファセット参照
      rules:
        - condition: 健全（指摘数が減少、修正が反映されている）
          next: reviewers
        - condition: 非生産的（同じ指摘が繰り返される）
          next: supervise
```


### Step 6: 検証

作成したファイルの整合性を確認する:

- [ ] セクションマップのキーとステップ内の参照が一致
- [ ] セクションマップのパスが実際のファイル位置と一致（ワークフローYAMLからの相対パス）
- [ ] ビルトイン参照（bare name）とカスタム参照（セクションマップキー）が混在していないか
- [ ] `initial_step` が `steps` 配列内に存在
- [ ] 全ステップの `rules.next` が有効な遷移先（他のステップ名 or COMPLETE/ABORT）
- [ ] parallel ステップの親ルールが `all()` / `any()` を使用
- [ ] parallel サブステップのルールに `next` がない（親が制御）

## バリデーション

作成・編集したファイルは `validate-takt-files.sh` で機械的に検証できる:

```bash
bash .agents/skills/j5ik2o-takt-workflow-builder/scripts/validate-takt-files.sh
```

検証項目:
- **ワークフロー YAML**: 必須フィールド（`name`/`initial_step`/`steps`）、`initial_step` の step 参照、ファセットファイル参照の実在
- **ファセット .md**: 空チェック、persona/policy/knowledge は `# 見出し` 必須、instruction/output-contract は内容存在

オプション `--workflows` / `--facets` で対象を絞り込み可能。
