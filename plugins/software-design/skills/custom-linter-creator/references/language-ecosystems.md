# Custom Linter Language Ecosystems

## TypeScript And JavaScript

Use ESLint. Create a local plugin or flat-config rule under `lints/eslint/`. Add fixtures with valid and invalid samples. Diagnostics should include repair steps and the exact replacement scope.

## Python

Use pylint when custom static checks are needed. Ruff is excellent for built-in rules but is not the easiest route for project-specific custom rules. Put checkers under `lints/pylint/` and test them with small fixture modules.

## Go

Use `golang.org/x/tools/go/analysis`. Provide a standalone analyzer command first; integrate with golangci-lint only after the analyzer is stable. Report positions with `pass.Fset.Position`.

## Rust

Prefer Clippy configuration for existing lints. For project-specific rules, use dylint or a custom rustc-driver-based lint only when the rule is important enough to justify maintenance.

## Diagnostic Message Contract

Every diagnostic should contain:

1. The violated rule.
2. Concrete repair steps.
3. The allowed edit scope.
4. The reason the rule exists.
5. A stable rule id for suppression and documentation.
