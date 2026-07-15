---
name: j5ik2o:gh-issue-organizer
description: >
  Systematically inventory and organize GitHub Issues. Classify open issues,
  group related work, identify close candidates, prioritize remaining work, and
  propose useful batches. This includes separating CodeRabbit-generated issues
  from human-reported issues, grouping by root cause, and finding completed
  issues that can be closed. Trigger on GitHub Issue organization requests such
  as "organize issues", "triage GitHub issues", "audit open issues", "close
  stale issues", or "prioritize issues".
---

# GitHub Issue Organizer

Systematically inventory, classify, and organize open GitHub Issues.

## Workflow

Run the following five steps in order.

### Step 1: Understand the Current State

Use the `gh` CLI to fetch every open issue and summarize the current backlog.

> **Complete retrieval guarantee**: `gh issue list --limit` is an upper bound, and the default limit is 30. Open issues beyond the limit are silently omitted. Do not let counting or retrieval stop at the default limit.
> - Count issues with a sufficiently high limit: `gh issue list --state open --limit 100000 --json number --jq 'length'`.
> - Fetch all issues with a limit at least as large as the actual issue count. For large repositories, use `gh api --paginate "repos/{owner}/{repo}/issues?state=open&per_page=100" | jq -s 'add | [.[] | select(.pull_request | not)]'`. `--paginate` emits one JSON array per page, so applying `--jq` page by page splits the result. Use `jq -s 'add'` to combine all pages first, then remove PRs returned by the Issues endpoint by excluding entries with `.pull_request`.

```bash
# Fetch all open issues with labels, author, and timestamps. Set --limit above the open issue count.
gh issue list --state open --limit 1000 --json number,title,labels,author,createdAt,updatedAt,body

# Count issues by label.
gh issue list --state open --limit 1000 --json labels --jq '[.[].labels[].name] | group_by(.) | map({label: .[0], count: length}) | sort_by(-.count)'
```

Summarize the result as a table:

| Item | Count |
|------|-------|
| Total open issues | N |
| CodeRabbit-generated | N |
| Human-reported | N |

> At this stage, use only two high-level buckets: generated and human-reported. Total equals CodeRabbit-generated plus human-reported. The CodeRabbit criteria are author `coderabbitai` or a label containing `coderabbit`; other bots such as `github-actions[bot]` are not CodeRabbit. Step 2 defines the detailed extraction commands. Treat Step 1 counts as a preliminary overview, then produce final category counts in Step 5 after classification.

### Step 2: Classify Issues

Classify each issue into the categories below.

#### Classification Criteria

| Category | Rule |
|----------|------|
| **CodeRabbit-generated** | Author is `coderabbitai`, or any label contains `coderabbit`. Other automation bots such as `github-actions[bot]` are not included; put non-CodeRabbit bot issues in Other. |
| **Human-reported bug** | Issue has the `bug` label, or the title contains clear bug wording such as `bug`, `defect`, `failure`, or `broken`. |
| **Human-reported feature request** | Labels include `enhancement` or `feature`. |
| **Epic / refactoring** | Labels include `refactoring` or `epic`, or the title contains `Phase` or `refactoring`. |
| **Other** | Every issue that does not match the four categories above, including human-created issues with no bug, feature, or epic signal, and non-CodeRabbit bot issues such as Dependabot. |

> Evaluate categories from top to bottom and use the first match. After CodeRabbit-generated, check bug, then feature request, then Epic / refactoring, and finally Other. This guarantees every issue belongs to exactly one category and keeps Step 5 totals consistent. The reliable bug signal is the `bug` label; title keywords are best-effort language-dependent helpers. If an unlabeled issue is hard to classify mechanically, leave it in Other and ask for a label when needed.

#### Classification Commands

```bash
# Extract CodeRabbit-generated issues. Keep this aligned with the classification table.
gh issue list --state open --limit 1000 --json number,title,author,labels --jq '[.[] | select(.author.login == "coderabbitai" or (.labels | any(.name | ascii_downcase | contains("coderabbit"))))]'

# Extract human-reported issues by negating the CodeRabbit condition.
gh issue list --state open --limit 1000 --json number,title,author,labels --jq '[.[] | select((.author.login == "coderabbitai" or (.labels | any(.name | ascii_downcase | contains("coderabbit")))) | not)]'
```

### Step 3: Group Related Work

Group classified issues by root cause or theme.

#### Grouping Dimensions

1. **Code area**: target module, crate, package, service, or UI area.
2. **Root cause**: shared design problem, such as locking strategy, type design, encapsulation, or error handling.
3. **Work granularity**: independently fixable versus more efficient as a batch.

#### Output Format

```md
## Group: [Theme]
- Related issues: #N, #M, #K
- Root cause: [Explanation]
- Proposed handling: [Individual / Batch]
- Estimated effort: [Small / Medium / Large]
```

### Step 4: Decide Close Candidates With Code Verification

For each issue, decide whether it is already resolved by **reading the current code**.
Do not rely only on PR history or commit logs. Always inspect the current code.

#### Verification Steps

**Run these steps for each issue:**

1. **Parse the issue body** and extract:
   - Target file paths
   - Target symbols, such as function names, structs, classes, traits, or types
   - The reported problem
   - Quoted code snippets

2. **Check whether the target code still exists**:
   ```bash
   # When a file path is known.
   test -f <file-path>

   # Search current code for symbols, function names, or type names.
   rg -n "<symbol>|<function>|<type>" .

   # Search for distinctive snippets or error messages from the issue.
   rg -n "<distinctive-string>" .
   ```
   If `rg` is unavailable, use the best available file-read or grep equivalent.
   If the current path or name is found, continue to step 3.

   **If it is not found, do not immediately mark the target as gone.** It may have been renamed, moved, or split. Track it through git history so a still-valid issue is not closed incorrectly:
   ```bash
   # Track file renames and moves.
   git log --follow -M --oneline -- <file-path>
   git log -p -M --follow -- <file-path>        # Inspect moved paths and changed content.

   # Find where a symbol may have moved.
   git log -S'<symbol>' --oneline --all         # Commits where the string occurrence count changed.
   git log -G'<symbol>' --oneline --all         # Commits with diffs containing the string.

   # Search broadly for possible renamed terms in the current codebase.
   rg -n "<renamed-candidate>|<related-term>" .
   ```
   - If a rename or move is found, inspect the new path or name in step 3. Do not treat it as gone.
   - If git history shows deletion and no moved target, mark it as **Target gone**.

   Git history is only for locating the current code. The resolved/unresolved decision must still come from reading the current implementation.

3. **Read the relevant code** for the target symbol, including renamed or moved targets:
   ```bash
   # Read the relevant range when line numbers are known.
   sed -n '<start-line>,<end-line>p' <file-path>

   # Search around the target.
   rg -n "<symbol>|<reported-pattern>" <file-path>
   ```
   If a file-read tool is available, use it to inspect the relevant section directly.
   Symbolic tools such as Serena may be used as optional helpers only when available; do not depend on them.

   Check:
   - Does the reported problematic pattern still exist?
   - Did refactoring make the report obsolete?
   - Has the exact requested fix already been applied?

4. **Record one status for each issue**:

| Status | Rule | Evidence format |
|--------|------|-----------------|
| **Closable** | Current code shows the report has been resolved. | "Checked `<symbol>` in `<file>`; the reported `<problem>` is resolved by `<current implementation>`." |
| **Target gone** | The target file or symbol no longer exists, and git history shows no rename or move target. | "`<file>` was deleted; `git log --follow` showed no moved target" or "`<symbol>` no longer exists." |
| **Unresolved** | Current code still contains the reported problem. | "Checked `<symbol>` in `<file>`; the reported `<problem>` still exists." |
| **Needs confirmation** | Code alone cannot decide because the result depends on design intent or product direction. | State why the decision cannot be made from code alone. |
| **Duplicate** | The same report is already covered by another issue. | State the duplicate issue number. |

#### Decision Principles

- **Do not mark an issue as closable without reading code**. Do not infer resolution from PR titles, commit messages, or merge history alone.
- **Do not assume missing file or symbol equals deletion**. Before using Target gone, follow renames and moves with `git log --follow -M`, `git log -S`, and `git log -G`; if a moved target exists, inspect that current code.
- Inspect the relevant current code for every issue.
- CodeRabbit issues usually point to a concrete file and line, so inspect that exact location first.
- For large issue sets, use agent tooling to verify issues in parallel when available.

#### Close Comment Format

When closing an issue, include code-verification evidence in this format:

```md
## Resolution Check

- Checked target: `<symbol>` in `<file-path>`
- Result: `<reported problem>` is resolved by `<specific current implementation>`
- Related: [PR #N / Refactoring Phase X] when applicable

Closing this issue.
```

**Important**: Do not close issues until the user approves the proposed close list. The skill may prepare the analysis automatically, but the actual close action requires user approval.

### Step 5: Report

Report the analysis in the format below.

#### Summary

```md
## Issue Inventory Summary

| Category | Count | Close candidates | Remaining |
|----------|-------|------------------|-----------|
| CodeRabbit-generated | N | N | N |
| Human-reported bug | N | N | N |
| Human-reported feature request | N | N | N |
| Epic / refactoring | N | N | N |
| Other | N | N | N |
| Total | N | N | N |
```

#### Close Candidates

```md
## Close Candidates

| # | Title | Status | Checked location | Evidence |
|---|-------|--------|------------------|----------|
| #N | ... | Closable | `Bar::baz()` in `src/actor/foo.rs` | Reported mutex usage has been replaced with `Arc<RwLock>`. |
| #N | ... | Target gone | `src/old_module.rs` | File was deleted. |
| #N | ... | Duplicate | - | Same report as #M. |
```

#### Group Details

For each group, include:

- Related issues
- Root cause
- Recommended action: close, fix, or defer
- Batch proposal for issues that should be handled together

#### Priority Proposal

Recommend the order for remaining issues:

1. **High**: Safety or correctness issues
2. **Medium**: Design or maintainability improvements
3. **Low**: Style or minor improvements

## gh CLI Command Reference

```bash
# Detailed issue list.
gh issue list --state open --limit 1000 --json number,title,labels,author,createdAt,updatedAt,body,comments

# Issues with a specific label.
gh issue list --state open --limit 1000 --label "bug" --json number,title

# Issue details.
gh issue view <number> --json number,title,body,labels,author,comments

# Close an issue with a comment.
gh issue close <number> --comment "Reason"

# Add a label to an issue.
gh issue edit <number> --add-label "label-name"

# Recently merged PRs.
gh pr list --state merged --limit 50 --json number,title,mergedAt

# Files changed by a PR.
gh pr view <number> --json files
```

## Notes

- **Close decisions must be based on reading current code**. Do not decide from PR history, commit messages, or titles alone.
- **Close actions require user approval**. The skill can prepare the findings, but the user must approve actual closures.
- Prefer `rg`, file read, `git log --follow -M`, `git log -S`, and `git log -G` for code verification. Use symbolic tools such as Serena only as optional helpers when available.
- CodeRabbit issues usually include concrete file and line references, so inspect those locations directly.
- CodeRabbit issue sets can be large; group them first to understand the shape of the backlog before close-candidate verification.
- To process many issues efficiently, inspect issues about the same file together.
- When issue bodies are long, use `--jq` to extract only the needed fields.
- Leave ambiguous issues as Needs confirmation and ask the user to decide.
