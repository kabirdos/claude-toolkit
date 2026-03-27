---
name: gemini-review
description: Run a Gemini CLI code review on the current branch diff — categorizes findings as Critical/Warning/Suggestion and offers to fix critical issues
user-invocable: true
disable-model-invocation: true
---

# /gemini-review — Cross-Model Code Review

Run Gemini as an external code reviewer on your current branch. Gets a second opinion on bugs, security, and best practices.

## Usage

- `/gemini-review` — review all changes on current branch vs main
- `/gemini-review --staged` — review only staged changes
- `/gemini-review --file src/auth.ts` — review a specific file's changes
- `/gemini-review --fix` — auto-fix critical issues without asking

## Steps

### 1. Check Prerequisites

Verify `gemini` CLI is installed:

```bash
command -v gemini
```

If not found, tell the user:

> "Gemini CLI is not installed. Install it with: `npm install -g @anthropic-ai/gemini-cli` or check https://github.com/anthropics/gemini-cli"

Stop if not available.

### 2. Get the Diff

Based on flags:

- Default: `git diff main...HEAD` (all changes on branch)
- `--staged`: `git diff --cached`
- `--file <path>`: `git diff main...HEAD -- <path>`

If the diff is empty, tell the user there are no changes to review and stop.

### 3. Run Gemini Review

```bash
gemini -p "You are a senior code reviewer. Review this diff for:

1. **Critical** — Bugs, security vulnerabilities, data loss risks, broken functionality
2. **Warnings** — Performance issues, missing error handling, race conditions, incomplete implementations
3. **Suggestions** — Code style, naming, simplification opportunities, best practices

For each finding, include:
- Category (Critical/Warning/Suggestion)
- File and approximate location
- What's wrong
- How to fix it

Be concise. Skip praise. Only report actionable findings.

Diff:
$(git diff main...HEAD)"
```

Capture the full output.

### 4. Parse and Display Results

Show the Gemini review output, organized by severity:

```
Gemini Code Review
──────────────────
Branch: feature/your-branch → main
Files changed: N

🔴 Critical (N)
  - [file:line] Description — fix suggestion

🟡 Warnings (N)
  - [file:line] Description — fix suggestion

🔵 Suggestions (N)
  - [file:line] Description — fix suggestion

✅ No critical issues (if none found)
```

### 5. Handle Critical Issues

**If critical issues found and `--fix` flag:**

- Fix each critical issue
- Run tests to verify the fix doesn't break anything
- Stage and commit: `fix: address Gemini review — [description]`

**If critical issues found without `--fix`:**

- Ask: "Found N critical issues. Want me to fix them now?"
- If yes, fix, test, commit
- If no, just report them

**If no critical issues:**

- Report the warnings and suggestions
- Ask if the user wants any of them addressed

### 6. Summary

```
Review complete: N critical, N warnings, N suggestions
Fixes applied: [list any commits made]
```
