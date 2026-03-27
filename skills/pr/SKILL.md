---
name: pr
description: Commit, push, create PR, and optionally run Gemini code review — the full ship-it workflow in one command
user-invocable: true
disable-model-invocation: true
---

# /pr — Ship It

One command to go from working changes to a reviewed PR. Handles commit, push, PR creation, and Gemini review.

## Usage

- `/pr` — commit all staged/unstaged changes, push, create PR, run Gemini review
- `/pr --no-review` — skip the Gemini review step
- `/pr --draft` — create as draft PR
- `/pr fix the auth redirect bug` — use the provided text as context for the commit message and PR description

## Steps

### 1. Safety Check

Run `git branch --show-current`. If on `main` or `master`:

- STOP immediately
- Tell the user: "You're on main. Create a feature branch first: `git checkout -b feature/your-feature`"
- Do NOT proceed

### 2. Assess Changes

Run these in parallel:

- `git status` — see what's changed (never use -uall flag)
- `git diff` — see unstaged changes
- `git diff --cached` — see staged changes
- `git log main..HEAD --oneline` — see commits already on this branch

### 3. Commit (if there are uncommitted changes)

- Stage relevant files (prefer specific files over `git add .`)
- Do NOT stage .env files, credentials, or secrets — warn if found
- Write a conventional commit message (feat:, fix:, chore:, etc.) based on the actual changes
- Do NOT add Co-Authored-By lines
- If no uncommitted changes exist, skip to step 4

### 4. Push

- Push the branch with `-u` flag to set upstream tracking
- If the branch has no remote yet, this creates it

### 5. Create PR

- Use `gh pr create` with:
  - A concise title (under 70 chars) using the conventional commit prefix
  - A body with:
    - `## Summary` — 1-3 bullet points describing what changed and why
    - `## Test plan` — how to verify the changes work
  - If user provided context text with the command, use it to inform the title and description
  - If `--draft` flag was passed, add `--draft` to the gh command

Use a HEREDOC for the body to preserve formatting:

```bash
gh pr create --title "feat: title here" --body "$(cat <<'EOF'
## Summary
- bullet points here

## Test plan
- [ ] verification steps here
EOF
)"
```

### 6. Gemini Code Review (unless --no-review)

Check if `gemini` CLI is available. If yes:

- Get the diff: `git diff main...HEAD`
- Run Gemini review: `gemini -p "Review this pull request diff for bugs, security issues, TypeScript best practices, and any issues. Be concise — list only actionable findings categorized as Critical / Warning / Suggestion: $(git diff main...HEAD)"`
- Summarize findings to the user

If `gemini` is not available, skip and note that Gemini CLI is not installed.

### 7. Fix Critical Issues (if any)

If Gemini found Critical issues:

- Ask the user if they want to fix them now
- If yes: fix, commit with `fix: address code review feedback`, push, and note the PR will update automatically

### 8. Report

Display:

- PR URL (from gh pr create output)
- Branch name
- Number of commits included
- Gemini review summary (if run)
