# Global Claude Code Instructions

## Git Workflow

- When making git commits, do not add Co-Authored-By lines.
- Always work on feature branches — never commit directly to main.
- Create PRs to merge into main — never push directly.
- Use conventional commits: feat:, fix:, chore:, docs:, refactor:, test:.
- When in doubt about which branch you're on, run `git branch --show-current` before committing.
- MUST NOT commit .env files, API keys, credentials, or secrets.

## Session Start

- If /agent/WORKFLOWS.md exists in the project, read it before starting work and follow it over any default workflow.
- If /agent/HANDOFF.md exists in the project, read it on session start for context from previous sessions.

## Code Quality

- Run Gemini CLI review on staged changes before every commit (when available).
- After running parallel agents or batch changes, run the full test suite and verify no regressions before committing.
- When fixing CSS/styling issues, apply fixes across ALL breakpoints (mobile, tablet, desktop) unless explicitly told otherwise.
- Update /docs when code changes affect documented behavior.

## Content & UI

- When making UI/content changes, ALWAYS preserve existing real content. Never replace live site content with placeholder or fabricated content. If unsure what content exists, read the current files first.

## Working Style

- Prefer action over exploration. When asked to fix bugs, start implementing fixes quickly rather than spending extended time reading and planning. If exploration exceeds 5 minutes without a code change, pause and confirm approach with the user.
