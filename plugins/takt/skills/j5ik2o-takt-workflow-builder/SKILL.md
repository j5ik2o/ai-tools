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

> **前提 takt バージョン**: v0.77.0

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

| ビルトイン | 構成 | 用途 |
|-----------|------|------|
| `default.yaml` | plan→write_tests→implement→ai_review→reviewers(arch+qa)→fix→supervise | 標準開発 |
| `dual.yaml` | plan→write_tests→team_leader_implement→ai_review→reviewers(2段階)→fix→supervise | フロントエンド＋バックエンド |
| `backend.yaml` | plan→write_tests→implement→ai_review→reviewers→fix→supervise | バックエンド特化 |
| `backend-cqrs.yaml` / `backend-cqrs-mini.yaml` | CQRS+ESバックエンド開発 | CQRS/ES特化 |
| `frontend.yaml` | plan→write_tests→implement→ai_review→reviewers→fix→supervise | フロントエンド特化 |
| `frontend-maintenance.yaml` | 既存フロントエンド保守スコープ | フロントエンド保守 |
| `backend-maintenance.yaml` | 既存バックエンド保守スコープ | バックエンド保守 |
| `maintenance.yaml` | 汎用保守ワークフロー | 保守全般 |
| `backend-mini.yaml` / `dual-mini.yaml` / `dual-cqrs-mini.yaml` / `frontend-mini.yaml` | plan→implement→supervise | 最小構成（開発系） |
| `mini-core.yaml` | 最小コア構成 | 最小構成（コア） |
| `simple.yaml` | シンプル実装 | 軽量実装 |
| `simple-backend.yaml` / `simple-core.yaml` / `simple-cqrs.yaml` / `simple-dual.yaml` / `simple-dual-cqrs.yaml` / `simple-frontend.yaml` / `simple-mini.yaml` | simple 系バリアント | 軽量実装（特化） |
| `pure.yaml` | 純粋なコアフロー | 純粋実装 |
| `cli.yaml` | CLI ツール向け | CLI 開発 |
| `development-core.yaml` | コア開発フロー | 開発コア |
| `development-implement.yaml` / `development-implement-dynamic.yaml` / `development-implement-team.yaml` | 実装フロー（通常/動的/チーム） | 実装特化 |
| `development-remediation.yaml` / `development-remediation-dynamic.yaml` / `development-remediation-team.yaml` | 修正フロー（通常/動的/チーム） | 修正特化 |
| `development-review.yaml` | 開発レビューフロー | 開発レビュー |
| `review.yaml` / `review-fix.yaml` / `review-fix-simple.yaml` | レビュー / レビュー→修正 | コードレビュー |
| `review-backend.yaml` / `review-dual.yaml` / `review-frontend.yaml` | バックエンド/デュアル/フロントエンドレビュー | コードレビュー（特化） |
| `review-fix-backend.yaml` / `review-fix-dual.yaml` / `review-fix-frontend.yaml` | レビュー→修正（特化系） | レビュー＋修正 |
| `review-remediation.yaml` | レビュー→修正（リメディエーション） | 修正ループ |
| `single-review-suite.yaml` | 単一レビュースイート | レビュースイート |
| `peer-review-suite-base.yaml` / `peer-review-suite-cqrs.yaml` / `peer-review-suite-frontend.yaml` / `peer-review-suite-frontend-cqrs.yaml` | ピアレビュースイート（基本/CQRS/フロントエンド系） | ピアレビュー |
| `final-gate.yaml` | 最終ゲート | リリースゲート |
| `loop-analysis.yaml` | ループ分析フロー | ループ分析 |
| `merge-prepare.yaml` | マージ前準備 | マージ前 |
| `merge-review.yaml` / `merge-review-ci.yaml` / `merge-review-fix.yaml` / `merge-review-fix-simple.yaml` | マージレビュー（通常/CI/修正） | マージレビュー |
| `caccia.yaml` | Caccia 自動化フロー | Caccia |
| `takt-default.yaml` / `review-takt-default.yaml` / `review-fix-takt-default.yaml` | TAKT 開発用 | TAKT 開発 |
| `takt-default-team.yaml` | チーム構成 TAKT 開発 | TAKT チーム開発 |
| `takt-development-review.yaml` | TAKT 開発レビュー | TAKT レビュー |
| `auto-improvement-loop.yaml` | system step と `managed_pr` を使う自己改善ループ | 自己改善 |
| `workflow-maker.yaml` | ワークフロー自動生成 | ワークフロー作成 |
| `audit-architecture.yaml` / `audit-architecture-backend.yaml` / `audit-architecture-dual.yaml` / `audit-architecture-frontend.yaml` | アーキテクチャ監査 | 品質監査 |
| `audit-e2e.yaml` / `audit-security.yaml` / `audit-unit.yaml` | E2E/セキュリティ/ユニットテスト監査 | 品質監査 |
| `terraform.yaml` | インフラストラクチャ | Terraform |
| `research.yaml` / `deep-research.yaml` | 調査・研究 | リサーチ |
| `magi.yaml` / `compound-eye.yaml` | 特殊構成 | 多視点分析 |

**v0.77.0 の主な変更点**:
- **削除**: `default-draft`, `default-high`, `default-mini`, `default-peer-review`, `draft`, `peer-review-with-fc`, `review-default`, `review-fix-default`, `takt-default-refresh-all`, `takt-default-refresh-fast`, `takt-default-with-fc`
- **追加**: `development-*`, `simple-*`, `merge-*`, `peer-review-suite-*`, `loop-analysis`, `final-gate`, `caccia`, `cli`, `workflow-maker`, `takt-default-team`, `takt-development-review`, `maintenance`, `backend-maintenance` 等（40本超）
- **Finding Contract 機能削除**: `peer-review-with-fc`, `takt-default-with-fc` と関連ファセット（`findings-manager` 系）が削除された。`finding_contract:` ブロックは現バージョンでは使用不可
- **`capabilities` キーワード追加**: ワークフロー YAML で provider option を指定できるのは `capabilities`（プリセット名の参照のみ）だけになった。ビルトインプリセットは `readonly` / `edit` / `enable-skills`
- **実行設定の削除**: `workflow_config.provider` / `model` / `provider_options`、step の `provider` / `model` / `provider_options`、`workflow_call.overrides` はロード時に拒否される。provider・model・effort 等は `runtime.yaml` に移す
- **`uses: <name>` ステップフラグメント**: `steps/<name>.yaml` に置いた step 定義を名前で参照して再利用可能（v0.77.0〜）

**再利用判断**: ビルトインのファセットで足りる場合はカスタムファセットを作らない。

### Step 3: ワークフローYAML作成

以下の構造でYAMLを作成する。

```yaml
name: workflow-name
description: ワークフローの説明
max_steps: 30
initial_step: plan

# ワークフロー全体の既定ケーパビリティ（v0.77.0〜。step の capabilities は既定値を置き換える）
capabilities: readonly  # ビルトイン: readonly / edit / enable-skills

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
    capabilities: readonly    # 読み取り・検索・シェル・Web 検索
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
    required_permission_mode: edit
    capabilities: edit        # readonly の既定値を上書きし Edit / Write を許可する
    persona: coder
    policy: [coding, testing]
    session: refresh
    instruction: implement
    rules:
      - condition: 実装完了
        next: review
```

**`capabilities` によるツール許可（v0.77.0〜、step の `provider_options` は廃止）**: `capabilities` はプリセット名（または名前のリスト）だけを受け付け、inline の options ブロックは書けない。プリセットは `.takt/provider-options/` → `~/.takt/provider-options/` → builtin の順に解決される。受け付ける leaf は `allowed_tools` / `network_access` / `sandbox` / `skills` のみで、`effort` や `base_url` 等を含むプリセットはロード時に失敗する（それらは `runtime.yaml` に書く）。`edit: true` だけでは Edit / Write は許可されないため、編集するステップには `capabilities: edit` を付ける。

```yaml
# ワークフロー既定は readonly、実装ステップだけ edit + skills
capabilities: readonly

steps:
  - name: implement
    capabilities: [edit, enable-skills]   # リストは左から右にマージ（後勝ち）

# 独自のツール許可はプリセット YAML（.takt/provider-options/<name>.yaml）を作って名前で参照する
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
      - name: testing-review
        edit: false
        tags: [review]
        persona: testing-reviewer
        policy: [review, testing]
        instruction: review-test
        output_contracts:
          report:
            - name: 06-testing-review.md
              format: testing-review
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

#### 設計判断ガイド

| 判断ポイント | 基準 |
|-------------|------|
| `edit: true/false` | コード変更するステップのみtrue |
| `session: refresh` | 実装系ステップで新規セッション開始 |
| `pass_previous_response: false` | レビュー結果を直接読ませたくない場合 |
| `required_permission_mode` | edit権限が必要な場合に `edit` を指定 |
| `capabilities`（step / parallel サブステップ） | ステップ単位のツール許可。`readonly` / `edit` / `enable-skills` またはカスタムプリセット名。step の値はワークフロー既定を置き換える。`system` / `workflow_call` ステップでは指定不可 |
| provider / model / effort / Kiro agent 等 | ワークフロー YAML には書けない（v0.77.0〜 拒否）。`runtime.yaml` に書く |
| `quality_gates` | agent step の完了条件。文字列 gate と `type: command` gate を混在可能 |
| `tags` | step / parallel サブステップのタグ配列（例: `[plan]`, `[coding]`, `[review]`）。`provider_routing.tags` でタグ単位のプロバイダー/モデル指定に使用 |
| `capabilities`（トップレベル） | 全ステップの既定ケーパビリティ（v0.77.0〜）。ワークフロー YAML で唯一の provider option 指定方法 |

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

#### ステップフラグメント（`uses: <name>`）（v0.77.0〜）

別のステップ定義を名前で参照して再利用する。フラグメントは `steps/<name>.yaml` に1ステップずつ置く（プロジェクトは `.takt/steps/`、ビルトインは `builtins/ja/steps/`）。

```yaml
steps:
  - name: plan
    uses: development-core-plan   # builtins/ja/steps/development-core-plan.yaml
    with:                         # フラグメントの params に値を渡す（必須パラメータはすべて指定）
      plan_policy: [design-planning]
      plan_knowledge: [architecture]
      plan_instruction: plan
      plan_report_format: plan
    rules:                        # uses するステップは自前の rules が必須
      - condition: 要件が明確で実装可能
        next: implement
      - condition: 要件が不明確、情報不足
        next: ABORT
```

- `uses:` で参照したフラグメントのフィールドはそのステップに展開される（ロード時、スキーマ検証の前）
- inline で指定した同名フィールドは `uses:` の値を上書きする
- フラグメント自身は `rules` を持てない。遷移先は呼び出し側のワークフローが決める

#### 全ステップ共通ルール（`all_steps.rules`）

`workflows/rules/<ref>.md` の Markdown ルールを、すべての agent ステップの Phase 1 指示に差し込む。遷移条件（`rules:`）ではない。

```yaml
all_steps:
  rules:
    - findings-handling             # 文字列参照（既定位置は自動実行ルールの後）
    - ref: plain-terminology
      position: before_instruction  # Instructions セクションの直前に置く
```

解決順: `.takt/workflows/rules/` → `~/.takt/workflows/rules/` → builtin（`builtins/ja/workflows/rules/`）。

#### サブワークフロー呼び出し（`call:` ステップ）

別のワークフローをサブルーチンとして呼び出す。

```yaml
steps:
  - name: run-sub
    kind: workflow_call
    call: sub-workflow-name    # 呼び出し先ワークフロー名
    args:                       # 呼び出し先の subworkflow.params に渡す値（任意）
      impl_knowledge: cqrs-es
    rules:
      - condition: completed
        next: next-step
```

- 呼び出し先には `subworkflow: { callable: true }` が必要
- `overrides` による provider / model 上書きは v0.77.0 で廃止（子は親の解決済み実行コンテキストを継承する）
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
