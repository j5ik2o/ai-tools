# TaskRecord スキーマ詳細

ソース: `references/takt/src/infra/task/taskRecordSchemas.ts` / `references/takt/src/infra/task/taskExecutionSchemas.ts`

## TaskRecord フィールド一覧

| フィールド | 型 | 必須 | デフォルト | 説明 |
|-----------|------|------|---------|------|
| `name` | string | YES | - | タスク識別名（AI自動生成、一意） |
| `status` | enum | YES | - | `pending` / `running` / `completed` / `failed` / `exceeded` / `pr_failed` |
| `workflow` | string | - | - | 実行ワークフロー名 |
| `task_dir` | string | ※ | - | タスクディレクトリパス（`.takt/tasks/{slug}` 形式） |
| `content` | string | ※ | - | インラインタスク本文（レガシー） |
| `content_file` | string | ※ | - | 外部ファイルパス参照（レガシー） |
| `slug` | string | - | - | 短い一意識別子 |
| `created_at` | ISO8601 | YES | - | タスク作成時刻 |
| `started_at` | ISO8601/null | YES | null | 実行開始時刻 |
| `completed_at` | ISO8601/null | YES | null | 実行完了時刻 |
| `worktree` | bool/string | - | - | `true`（自動）/ パス文字列 / 省略 |
| `branch` | string | - | auto | gitブランチ名（省略時: `takt/{timestamp}-{slug}`） |
| `auto_pr` | boolean | - | false | 実行後にPR自動作成 |
| `draft_pr` | boolean | - | false | PRをドラフト状態で作成 |
| `managed_pr` | boolean | - | false | TAKT管理下のPRフローを使う。`auto_pr: true` かつ `worktree` 有効が前提 |
| `issue` | int | - | - | GitHub Issue番号 |
| `start_step` | string | - | - | 開始step名 |
| `retry_note` | string | - | - | リトライ時のメモ |
| `worktree_path` | string | - | - | 実行時worktree絶対パス（自動設定） |
| `pr_url` | string | - | - | 生成PR URL（自動設定） |
| `summary` | string | - | - | 実行結果サマリ（自動設定） |
| `owner_pid` | int/null | - | null | 実行中プロセスPID（自動設定） |
| `owner_start_time` | string/null | - | null | 実行中プロセス開始時刻（自動設定、running + owner_pid 必須） |
| `failure` | object | - | - | 失敗情報（自動設定） |
| `completion` | object | - | - | ゴールタスク完了結果（自動設定） |
| `base_branch` | string | - | - | クローン元ブランチ（省略時: デフォルトブランチ） |
| `exceeded_max_steps` | int | - | - | exceeded時のmax_steps値（自動設定） |
| `exceeded_current_iteration` | int | - | - | exceeded時のイテレーション数（自動設定） |
| `run_slug` | string | - | - | 実行スラグ（タスク実行ごとの一意ID） |
| `source_run_slug` | string | - | - | 再開元の run_slug（自動設定、`resume_mode` と同時必須） |
| `resume_mode` | enum | - | - | 再開モード（`source_run_slug` が設定された場合は必須） |
| `resume_point` | object | - | - | サブワークフロー再開ポイント（自動設定、`restart_point` と排他） |
| `restart_point` | object | - | - | ワークフロー再起動ポイント（自動設定、`resume_point`/`start_step`/`exceeded_*` と排他） |
| `source_resume_point` | object | - | - | 再開元のresumeポイント（自動設定） |
| `should_publish_branch_to_origin` | boolean | - | - | ブランチをoriginにpushするか |
| `source` | enum | - | - | タスクソース: `pr_review` / `issue` / `manual` |
| `pr_number` | int | - | - | PR番号（`source: pr_review` 時は必須） |
| `context_pr_number` | int | - | - | コンテキスト参照用PR番号 |
| `goal_id` | uuid | - | - | ゴールID（ゴールタスク用） |
| `goal_purpose` | string | - | - | ゴール目的（ゴールタスク用） |
| `goal_work_key` | string | - | - | ゴール作業キー（ゴールタスク用） |
| `runtime_assignment` | string | - | - | ランタイム割り当て指定 |
| `execution_id` | string | - | - | 実行ID（自動設定） |
| `stop_request` | object | - | - | 停止リクエスト情報（自動設定） |
| `deletion` | object | - | - | 削除ロック情報（自動設定） |
| `auto_requeue_count` | int | - | - | 自動再キュー回数（自動設定） |
| `caccia_execution_source` | enum | - | - | Caccia実行ソース: `from_pr`（`source: pr_review` 時のみ有効） |
| `caccia_pushed_head` | object | - | - | Caccia のプッシュ済みHEAD情報（自動設定） |
| `merge_task` | boolean | - | - | マージタスクフラグ（自動設定、特定フィールドとの組み合わせ必須） |
| `merge_until` | enum | - | - | マージフェーズ: `prepare` / `merge` |
| `merge_method` | enum | - | - | マージ方式: `squash` / `merge` / `rebase` |
| `merge_concurrency` | int | - | - | マージ並行数 |
| `merge_head_repository_url` | string | - | - | マージ元リポジトリURL |
| `merge_head_repository_push_urls` | array | - | - | マージ元プッシュURL一覧 |
| `merge_initial_head_sha` | string | - | - | マージ開始時のHEAD SHA（40桁hex） |
| `merge_clone_prepared` | boolean | - | - | マージ用クローン準備済みフラグ |
| `merge_known_remote_head_sha` | string | - | - | 既知のリモートHEAD SHA |
| `merge_pushed_head_sha` | string | - | - | プッシュ済みHEAD SHA |
| `merge_push_base_head_sha` | string | - | - | プッシュ前のベースHEAD SHA（`merge_pushed_head_sha` 必須） |
| `merge_push_source` | enum | - | - | プッシュ元: `caccia` / `manual`（pushed_head + base_head SHA 必須） |
| `merge_threat_check_max_diff_bytes` | int | - | - | 脅威チェックの最大diff許容バイト数 |

**※ `content`, `content_file`, `task_dir` のいずれか正確に1つが必須。**

推奨: 新規タスクは `task_dir` 形式で作成する。

## TaskFailure オブジェクト

```yaml
failure:
  step: plan             # 失敗が発生したstep名（任意）
  error: "エラーメッセージ"  # エラー本体（必須、上限超過時は自動切り詰め）
  last_message: "..."    # 最後の出力（任意）
  retryable: false       # リトライ可能フラグ（任意、false かつ goal_id あり → 未開始 failed が許可）
```

## TaskExecutionConfig の追加制約

- `source: pr_review` のときは `pr_number` が必須
- `source: pr_review` のときは `branch` が必須（v0.77.0〜、ブランチ名バリデーションあり）
- `source: pr_review` のときは `base_branch` のブランチ名バリデーションあり
- `managed_pr: true` のときは `auto_pr: true` が必須
- `managed_pr: true` のときは `worktree` を有効化する必要がある
- `resume_point` と `restart_point` は排他（同時指定不可）
- `start_step` / `exceeded_current_iteration` / `exceeded_max_steps` と `restart_point` は排他
- `caccia_execution_source` は `source: pr_review` のときのみ有効
- `caccia_pushed_head` は `caccia_execution_source: from_pr` かつ `merge_task: true` でないときのみ有効
- `source_run_slug` を設定するときは `resume_mode` が必須
- `merge_push_base_head_sha` は `merge_pushed_head_sha` が必須
- `merge_push_source` は `merge_pushed_head_sha` と `merge_push_base_head_sha` が必須

## resume_point オブジェクト

```yaml
resume_point:
  version: 1
  stack:
    - workflow: child-workflow
      workflow_ref: references/takt/builtins/ja/workflows/default.yaml   # 任意
      step: review
      kind: workflow_call   # agent / system / workflow_call
  iteration: 12
  elapsed_ms: 38124
```

サブワークフロー再開用の内部状態。手動作成対象ではなく、自動設定値として扱う。

## ステータス遷移と不変条件

```
pending ──→ running ──→ completed
                ├──→ failed
                ├──→ exceeded
                └──→ pr_failed
```

| フィールド | pending | running | completed | failed | exceeded | pr_failed |
|----------|---------|---------|-----------|--------|----------|-----------|
| started_at | **null** | 必須 | 必須 | 必須 | 必須 | 必須 |
| completed_at | **null** | **null** | 必須 | 必須 | 必須 | 必須 |
| owner_pid | **null** | 任意 | **null** | **null** | **null** | **null** |
| failure | **null** | **null** | **null** | 必須 | **null** | 任意 |
| exceeded_max_steps | - | - | - | - | 必須※ | - |
| exceeded_current_iteration | - | - | - | - | 必須※ | - |

**※ `exceeded_max_steps` と `exceeded_current_iteration` は両方同時に設定するか、両方省略する。**

## task_dir パス形式

- 相対パス必須（絶対パス不可）
- `.takt/tasks/<slug>` 形式
- slug例: `20260201-015714-foptng`（`{YYYYMMDD}-{HHmmss}-{random6}`）

## テンプレート変数（order.md内では不要）

order.md自体ではテンプレート変数は不要。エンジンが `{task}` として自動注入する。

ワークフローの `instruction` 内では以下が使用可能（`instruction_template` は v0.36.0 で完全廃止）:

| 変数 | 説明 |
|------|------|
| `{task}` | タスク内容（自動注入） |
| `{previous_response}` | 前step出力 |
| `{iteration}` | ワークフロー全体イテレーション数 |
| `{max_steps}` | ワークフローの max_steps 値 |
| `{step_iteration}` | このstepの実行回数 |
| `{report_dir}` | レポートディレクトリ名 |
| `{report:filename}` | レポートファイル内容 |
