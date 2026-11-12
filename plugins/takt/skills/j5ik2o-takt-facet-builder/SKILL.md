---
name: j5ik2o-takt-facet-builder
description: >
  TAKTファセット（Persona/Policy/Instruction/Knowledge/Output Contract）の
  個別作成・編集スキル。各ファセットのスタイルガイドに準拠した単体ファイルを生成する。
  references/taktにあるスタイルガイド・ビルトインファセット群を参照資料として活用し、
  ファセット種別の判断、テンプレート選択、品質チェックを行う。
  トリガー：「ペルソナを作りたい」「ポリシーを追加」「インストラクションを書く」
  「ナレッジを定義」「出力契約を作成」「ファセットを編集」「takt facet」
  「レビュアーのペルソナ」「コーディングポリシー」
---

# TAKT Facet Builder

TAKTの5種類のファセットファイルを個別に作成・編集する。

> **前提 takt バージョン**: v0.75.0

## 参照資料

ファセット作成時は `references/takt/builtins/ja/` の資料を参照する。

| 資料 | パス | 用途 |
|------|------|------|
| スタイルガイド総合 | `references/takt/builtins/ja/STYLE_GUIDE.md` | 各ファセットの位置づけ |
| ペルソナガイド | `references/takt/builtins/ja/PERSONA_STYLE_GUIDE.md` | ペルソナ記述規約 |
| ポリシーガイド | `references/takt/builtins/ja/POLICY_STYLE_GUIDE.md` | ポリシー記述規約 |
| インストラクションガイド | `references/takt/builtins/ja/INSTRUCTION_STYLE_GUIDE.md` | インストラクション記述規約 |
| 出力契約ガイド | `references/takt/builtins/ja/OUTPUT_CONTRACT_STYLE_GUIDE.md` | 出力契約記述規約 |
| Faceted Prompting | `references/takt/docs/faceted-prompting.ja.md` | 5ファセット設計の理論 |
| ビルトインファセット | `references/takt/builtins/ja/facets/{personas,policies,instructions,knowledge,output-contracts}/` | 既存ファセット例 |

**注意**: `references/takt/builtins/{ja,en}/templates/` は v0.43.0 でも実在する。雛形として参照してよいが、実際の命名・責務分割・文体はビルトインファセットを source of truth として合わせる。

**重要**: ファセット作成前に該当するスタイルガイドを必ず読む。

## ワークフロー

### Step 1: ファセット種別の判定

ユーザーの要件から、作成すべきファセット種別を判定する。

```
この内容は…
├── 特定エージェントのidentity・専門知識 → Persona
├── 複数エージェントが共有する行動規範 → Policy
├── ステップ固有の実行手順 → Instruction
├── 判断の前提となる参照情報 → Knowledge
└── エージェント出力の構造定義 → Output Contract
```

| ファセット | 配置先 | 対象 | キー判断 |
|-----------|--------|------|----------|
| Persona | system prompt | 1エージェント | 「この知識はこのエージェント固有か？」 |
| Policy | user message内 | 複数エージェント | 「複数エージェントが同じルールに従うか？」 |
| Instruction | Phase 1 message | 1ステップ | 「この手順はこのステップ固有か？」 |
| Knowledge | user message内 | 1+エージェント | 「判断の前提となる参照情報か？」 |
| Output Contract | Phase 2 message | 1レポート | 「後続が`{report:filename}`で参照するか？」 |

### Step 2: ビルトイン確認

同種のビルトインファセットを確認し、再利用できるか判断する。

| ファセット | ビルトイン例 |
|-----------|-------------|
| Persona | ai-antipattern-reviewer, architecture-reviewer, balthasar, casper, coder, coding-reviewer, companion-round-adjudicator, conductor, cqrs-es-reviewer, director, dual-supervisor, exec-assistant, exec-worker, frontend-reviewer, loop-analysis-reviewer, loop-analyzer, manager, melchior, planner, research-analyzer, research-digger, research-planner, research-supervisor, review-adjudicator, security-reviewer, supervisor, terraform-coder, terraform-reviewer, test-planner, testing-reviewer |
| Policy | ai-antipattern, applicable-inputs, architecture, backend, caccia-review, coding, companion-review, companion-round-adjudication, contract-change, cqrs-es, design-fidelity, design-planning, director, evidence-based-judgment, existing-system-respect, frontend, gui, implementation-semantics, manager, merge-ci-recovery, process-deviation, react, repair-strategy, research, review, review-adjudication, screen-api, security-review, takt, takt-testing, takt-testing-review, task-decomposition, terraform, testing |
| Instruction | adjudicate-review-findings, ai-antipattern-fix, ai-antipattern-review, apply-fix-plan, apply-fix-verification, arbitrate, architect, architecture-audit-plan, architecture-audit-review, architecture-audit-supervise, architecture-audit-team-leader, architecture-review, audit-security-plan, audit-security-review, audit-security-supervise, audit-security-team-leader, caccia, coding-review, companion-moderate-review, companion-watch-review, companion-watch-testing, cqrs-es-review, development-implement-with-reports, development-implementation-completion, development-maintenance-with-reports, development-reimplement-with-reports, development-team-with-reports, director, e2e-audit-plan, e2e-audit-review, e2e-audit-supervise, e2e-audit-team-leader, exec-loop-monitor, exec-replan, exec-review, exec-worker, fix, fix-completion-retry, fix-maintenance, fix-plan, fix-plan-from-review-resolution, fix-replan, fix-supervisor, follow-up-ai-antipattern-review, follow-up-architecture-review, follow-up-coding-review, follow-up-cqrs-es-review, follow-up-frontend-review, follow-up-review-completion-retry, follow-up-security-review, follow-up-testing-review, frontend-review, gather-review, implement, implement-after-tests, implement-maintenance, implement-terraform, initial-ai-antipattern-review, initial-review-completion-retry, loop-analysis, loop-monitor-reviewers-fix, manager, merge-ci-fix, merge-ci-investigate, merge-ci-review, plan, plan-maintenance, reanalyze-loop-analysis, replan-implementation, request-replan, research-analyze, research-dig, research-plan, research-supervise, review-arch, review-coding, review-completion-retry, review-cqrs-es, review-frontend, review-loop-analysis, review-remediation-problem-tracking, review-security, review-terraform, review-test, scenario-based-fix-plan-from-review-resolution, scenario-based-fix-replan, scenario-based-plan, scenario-based-plan-maintenance, scenario-based-replan-implementation, scenario-based-supervise-review-resolution, scenario-based-verification-replan, scenario-based-write-tests-first, security-review, select-applicable-candidates, simple-implement, simple-implement-after-tests, simple-plan, simple-review-coding, simple-supervise, supervise, supervise-maintenance, supervise-review-resolution, team-leader-fix, team-leader-fix-plan, team-leader-fix-verification, team-leader-implement, testing-review, unit-audit-plan, unit-audit-review, unit-audit-supervise, unit-audit-team-leader, verification-replan, verify-fix, workflow-maker-create, workflow-maker-fix, workflow-maker-review, write-tests-first |
| Knowledge | architecture, backend, cqrs-es, director, e2e-testing, existing-system, frontend, gui, implementation-semantics, loop-analysis, manager, react, research, security, security-api, security-data, security-dependencies, security-local, security-web, takt, takt-test-execution, task-decomposition, terraform-aws, unit-testing |
| Output Contract | ai-antipattern-review, architecture-audit, architecture-audit-plan, architecture-review, audit-security, caccia-decisions, coder-decisions, coder-scope, coding-review, cqrs-es-review, e2e-audit, e2e-audit-plan, exec-review-result, fix-plan, fix-report, fix-verification, frontend-review, implementation-report, implementation-report-order, loop-analysis, maintenance-scope, merge-ci-fix, merge-ci-investigation, merge-ci-review, plan, plan-frontend, research-report, review-decision, review-gather, scenario-based-fix-plan, scenario-based-plan, scenario-based-test-report, security-review, supervisor-summary, supervisor-validation, terraform-review, test-report, testing-review, unit-audit, unit-audit-plan, workflow-maker-doctor, workflow-maker-review |

**v0.75.0 の変更点**: 大幅なファセット再編成が行われた。
- **Persona**: `pure-reviewer`・`findings-manager`・`architect-planner`・`pr-commenter` を削除。`companion-round-adjudicator`・`director`・`exec-assistant`・`exec-worker`・`loop-analysis-reviewer`・`loop-analyzer`・`manager`・`review-adjudicator` を新規追加
- **Policy**: 多数の新規ポリシー追加（`applicable-inputs`, `caccia-review`, `companion-review`, `companion-round-adjudication`, `contract-change`, `director`, `evidence-based-judgment`, `gui`, `implementation-semantics`, `manager`, `merge-ci-recovery`, `process-deviation`, `repair-strategy`, `review`, `review-adjudication`, `security-review`, `takt-testing`, `takt-testing-review`, `testing`）
- **Instruction**: シナリオベース実装フロー（`scenario-based-*`）・development 系（`development-*-with-reports`）・シンプル系（`simple-*`）・merge CI 系（`merge-ci-*`）・exec 系（`exec-*`）・workflow-maker 系（`workflow-maker-*`）・companion 系（`companion-*`）など多数追加
- **Knowledge**: `director`・`gui`・`implementation-semantics`・`loop-analysis`・`manager`・`security-api`・`security-data`・`security-dependencies`・`security-local`・`security-web`・`takt-test-execution` 追加。`research-comparative` 削除
- **Output Contract**: `caccia-decisions`・`exec-review-result`・`fix-report`・`fix-verification`・`implementation-report`・`implementation-report-order`・`loop-analysis`・`merge-ci-*`・`review-decision`・`scenario-based-*`・`supervisor-summary`・`workflow-maker-*` を新規追加。旧 `findings-manager`・`*-finding-contract` 系・`pure-review`・`qa-review`・`architecture-design`・`summary`・`validation`・`test-plan`・`e2e-coverage-plan` を削除

**再利用判断**: ビルトインで足りる場合はカスタムファセットを作らない。

### Step 3: テンプレート選択と作成

#### Persona

参照: `references/takt/builtins/ja/facets/personas/` の既存ファセット

| テンプレート | 用途 | 例 |
|------------|------|-----|
| `simple.md` | ドメイン知識なし | coder, planner |
| `expert.md` | ドメイン知識あり | architecture-reviewer |
| `character.md` | 固有の人格・口調 | melchior, balthasar, casper |

```markdown
# {エージェント名}

{1-2文のロール定義。「あなたは〜です。」で始める}

## 役割の境界

**やること:**
- ...

**やらないこと:**
- ...（担当エージェント名を明記）

## 行動姿勢

- ...（3-8項目）

## ドメイン知識（expertのみ）

### {観点}
...
```

**サイズ目安**: simple 30-50行（上限100行）、expert 50-300行（上限550行）

**禁止事項**:
- ポリシーの詳細ルール（コード例・テーブル）を転記（1行の行動指針はOK）
- ワークフロー固有の概念（ステップ名、レポートファイル名）
- ツール固有のパス（`.takt/runs/`等）
- 実行手順

#### Policy

参照: `references/takt/builtins/ja/facets/policies/` の既存ファセット

```markdown
# {ポリシー名}

{1文の目的説明}

## 原則

| 原則 | 基準 |
|------|------|
| ... | ... |

## {ルールカテゴリ1}

{テーブル、コード例、箇条書きを自由に組み合わせ}
```

**サイズ目安**: 60-250行（上限300行）

**禁止事項**:
- 特定エージェント固有の知識
- ワークフロー固有の概念、ツール固有のパス
- 実行手順

#### Instruction

参照: `references/takt/builtins/ja/facets/instructions/` の既存ファセット

```markdown
{目的宣言。1-2行、命令形}

**注意:** {条件付き注意事項（該当する場合）}

**やること:**
1. {手順1}
2. {手順2}
3. {手順3}

**必須出力（見出しを含める）**
## {出力セクション1}
- {内容}
## {出力セクション2}
- {内容}
```

**サイズ目安**: レビュー sub-step 5-12行、計画・修正 10-20行、実装・検証 30-50行

**禁止事項**:
- ペルソナの内容（専門知識、行動姿勢）
- ポリシーの内容（共有コーディング原則）
- 自動注入される変数（`{task}`, `{previous_response}`）の手動記述
- 他ステップ名の直接参照

**テンプレート変数**（使用可能）:
- `{iteration}`, `{max_steps}`, `{step_iteration}`
- `{report_dir}`, `{report:filename}`, `{cycle_count}`

#### Knowledge

参照: `references/takt/builtins/ja/facets/knowledge/` の既存ファセット

```markdown
# {ドメイン名}知識

## {トピック1}

{概要。1-2文}

| 基準 | 判定 |
|------|------|
| ... | ... |

### {サブトピック}

{コード例で具体的に}

## {トピック2}

| パターン | 例 | 問題 |
|---------|-----|------|
| ... | `{コード}` | ... |

検証アプローチ:
1. {手順}
```

**特徴**: 記述的（「こうなっている」）。ポリシーの「WHY」を提供する。

#### Output Contract

参照: `references/takt/builtins/ja/facets/output-contracts/` の既存ファセット

````markdown
```markdown
# {レポートタイトル}

## 結果: APPROVE / REJECT

## サマリー
{1-2文で結果を要約}

## 詳細
| 観点 | 結果 | 備考 |
|------|------|------|
```

**認知負荷軽減ルール:**
- APPROVE → サマリーのみ（5行以内）
- REJECT → 問題点を表形式で（30行以内）
````

**サイズ目安**: 10-25行（上限30行、認知負荷軽減ルール除く）

**ステータスパターン**: `APPROVE / REJECT`（二値）、`APPROVE / IMPROVE / REJECT`（三値）、`完了`（固定値）

**レビュー出力契約の構造**（v0.30.0〜）:
- 各指摘に `family_tag` 列を追加（指摘のカテゴリ分類）
- セクション構成: `new`（新規）→ `persists`（継続）→ `resolved`（解消済み）→ `reopened`（再開）

**禁止事項**:
- 実行手順（インストラクションの責務）
- 判断基準の詳細（ペルソナ/インストラクションの責務）

### Step 4: 共通ルール適用

全ファセット共通のルールを確認する。

| ルール | 内容 |
|--------|------|
| 見出し深さ | `###` まで。`####` 以下は不可 |
| コード例 | 良い例/悪い例のペア。`// REJECT` `// OK` コメント |
| 文体 | ペルソナ・ポリシー・ナレッジ: 常体。インストラクション: 丁寧語（命令調） |
| ファイル命名 | `{name}.md`、ハイフン区切り、英語小文字 |
| 配置 | `~/.takt/{facet-type}/` または プロジェクト固有の場所 |

### Step 5: 検証

作成したファセットの品質を確認する。

**全ファセット共通:**
- [ ] `####` 以下のネストがないか
- [ ] ファイル命名規約に従っているか
- [ ] サイズ上限内か

**Persona:**
- [ ] ロール定義が1-2文か
- [ ] 「やること」「やらないこと」に担当エージェント名があるか
- [ ] ポリシーの詳細ルールが混入していないか
- [ ] ワークフロー固有の概念がないか

**Policy:**
- [ ] 目的説明が1文か
- [ ] 原則テーブルがあるか
- [ ] 複数エージェントに適用可能か

**Instruction:**
- [ ] 冒頭が命令形か
- [ ] 自動注入変数を手動記述していないか
- [ ] ペルソナ/ポリシーの内容が混入していないか

**Knowledge:**
- [ ] 記述的（宣言的）な文体か
- [ ] テーブルとコード例で具体的か

**Output Contract:**
- [ ] ```markdownコードブロックで囲まれているか
- [ ] レビュー系にステータスと認知負荷軽減ルールがあるか
- [ ] 番号プレフィックスがファイル名にないか

## バリデーション

作成・編集したファイルは `validate-takt-files.sh` で機械的に検証できる:

```bash
bash .agents/skills/takt-facet/scripts/validate-takt-files.sh
```

検証項目:
- **ワークフロー YAML**: 必須フィールド（`name`/`initial_step`/`steps`）、`initial_step` の step 参照、ファセットファイル参照の実在
- **ファセット .md**: 空チェック、persona/policy/knowledge は `# 見出し` 必須、instruction/output-contract は内容存在

オプション `--workflows` / `--facets` で対象を絞り込み可能。
