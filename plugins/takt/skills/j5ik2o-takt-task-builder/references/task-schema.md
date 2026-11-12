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
| `owner_start_time` | string/null | - | null | 実行中プロセス起動時刻（自動設定、`running` かつ `owner_pid` 存在時のみ有効） |
| `failure` | object | - | - | 失敗情報（自動設定） |
| `base_branch` | string | - | - | クローン元ブランチ（省略時: デフォルトブランチ） |
| `exceeded_max_steps` | int | - | - | exceeded時のmax_steps値（自動設定） |
| `exceeded_current_iteration` | int | - | - | exceeded時のイテレーション数（自動設定） |
| `run_slug` | string | - | - | 実行スラグ（タスク実行ごとの一意ID） |
| `resume_point` | object | - | - | サブワークフロー再開ポイント（自動設定） |
| `source_resume_point` | object | - | - | ソースワークフロー再開ポイント（自動設定） |
| `restart_point` | object | - | - | ワークフロー再起動ポイント（`resume_point` / `start_step` / `exceeded_*` とは同時指定不可） |
| `should_publish_branch_to_origin` | boolean | - | - | ブランチをoriginにpushするか |
| `source` | enum | - | - | タスクソース: `pr_review` / `issue` / `manual` |
| `pr_number` | int | - | - | PR番号（`source: pr_review` 時は必須） |
| `context_pr_number` | int | - | - | コンテキスト参照用PR番号 |
| `goal_id` | uuid | - | - | Goal管理用UUID |
| `goal_purpose` | string | - | - | Goalの目的 |
| `goal_work_key` | string | - | - | Goalの作業キー |
| `execution_id` | string | - | - | 実行ID（自動設定） |
| `stop_request` | object | - | - | 停止リクエスト（自動設定）: `{ execution_id, requested_at }` |
| `source_run_slug` | string | - | - | 再開元の実行スラグ（`resume_mode` と対になる、自動設定） |
| `resume_mode` | enum | - | - | 再開モード: `requeue` / `retry` / `instruct`（`source_run_slug` 存在時は必須、自動設定） |
| `deletion` | object | - | - | 削除管理オブジェクト（自動設定）: `{ id: uuid, owner_pid, owner_start_time? }` |
| `completion` | object | - | - | Goal完了結果（自動設定） |
| `auto_requeue_count` | int | - | - | 自動再キュー回数（自動設定） |
| `caccia_execution_source` | literal | - | - | Caccia実行ソース: `from_pr`（`source: pr_review` 時のみ有効） |
| `caccia_pushed_head` | object | - | - | Cacciaが処理したpush HEAD情報（自動設定） |
| `merge_task` | boolean | - | - | マージタスクフラグ（自動設定） |
| `merge_until` | enum | - | - | マージ進行制御: `prepare` / `merge` |
| `merge_method` | enum | - | - | マージ方式: `squash` / `merge` / `rebase` |
| `merge_concurrency` | int | - | - | マージ並列数 |
| `merge_head_repository_url` | string | - | - | マージ対象HEADリポジトリURL |
| `merge_head_repository_push_urls` | string[] | - | - | マージ対象HEADリポジトリpush URL一覧 |
| `merge_initial_head_sha` | string | - | - | マージ対象初期HEAD SHA（40桁hex） |
| `merge_clone_prepared` | boolean | - | - | マージクローン準備完了フラグ |
| `merge_threat_check_max_diff_bytes` | int | - | - | マージ脅威チェック最大diff bytes |
| `merge_known_remote_head_sha` | string | - | - | マージ既知リモートHEAD SHA |
| `merge_pushed_head_sha` | string | - | - | マージpush済みHEAD SHA |
| `merge_push_base_head_sha` | string | - | - | マージpush時の直前リモートHEAD SHA |
| `merge_push_source` | enum | - | - | マージpushソース: `caccia` / `manual` |

**※ `content`, `content_file`, `task_dir` のいずれか正確に1つが必須。**

推奨: 新規タスクは `task_dir` 形式で作成する。

## TaskFailure オブジェクト

```yaml
failure:
  step: plan             # 失敗が発生したstep名（任意）
  error: "エラーメッセージ"  # エラー本体（必須、oversized時は自動truncate）
  last_message: "..."    # 最後の出力（任意）
  retryable: false       # リトライ可否（任意、goal_id付きタスクの未開始失敗に使用）
```

## TaskExecutionConfig の追加制約

- `source: pr_review` のときは `pr_number` と `branch` が必須
- `managed_pr: true` のときは `auto_pr: true` が必須
- `managed_pr: true` のときは `worktree` を有効化する必要がある
- `caccia_execution_source` は `source: pr_review` 時のみ有効
- `restart_point` は `resume_point` / `start_step` / `exceeded_current_iteration` / `exceeded_max_steps` と同時指定不可
- `merge_task: true` のときは `source: pr_review`, `pr_number`, `branch`, `base_branch`, `worktree: true`, `merge_method`, `merge_head_repository_url`, `merge_head_repository_push_urls`, `merge_initial_head_sha`, `merge_threat_check_max_diff_bytes`, `merge_clone_prepared` が全て必須
- `source_run_slug` を設定した場合は `resume_mode` が必須

## resume_point / restart_point オブジェクト

`resume_point` と `restart_point` はいずれもサブワークフロー再開用の内部状態。手動作成対象ではなく、自動設定値として扱う。両者は同時指定不可。

v0.75.0 では `resume_point` は `WorkflowResumePointCodecSchema`（codec経由parse）に変更され、フォーマット詳細は実装側が管理する。

## ステータス遷移と不変条件

```
pending ──→ running ──→ completed
                ├──→ failed
                ├──→ exceeded
                └──→ pr_failed
```

| フィールド | pending | running | completed | failed | exceeded | pr_failed |
|----------|---------|---------|-----------|--------|----------|-----------|
| started_at | **null** | 必須 | 必須 | 必須※2 | 必須 | 必須 |
| completed_at | **null** | **null** | 必須 | 必須※2 | 必須 | 必須 |
| owner_pid | **null** | 任意 | **null** | **null** | **null** | **null** |
| owner_start_time | **null** | 任意（owner_pid存在時のみ） | **null** | **null** | **null** | **null** |
| failure | **null** | **null** | **null** | 必須 | **null** | 任意 |
| exceeded_max_steps | - | - | - | - | 必須※1 | - |
| exceeded_current_iteration | - | - | - | - | 必須※1 | - |

**※1 `exceeded_max_steps` と `exceeded_current_iteration` は両方同時に設定するか、両方省略する。**
**※2 `failed` 状態の例外: `goal_id` が設定されており `failure.retryable === false` の場合、`started_at: null` / `completed_at: null` でも有効（未開始Goal失敗）。**

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
