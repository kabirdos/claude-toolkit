---
name: deploy-verify
description: Merge a PR and monitor the deployment end-to-end — watch the build, check for errors, self-heal failures, verify the deploy is clean
user-invocable: true
disable-model-invocation: true
---

# /deploy-verify — Merge, Monitor, Verify

One command to merge a PR and ensure the deployment succeeds. Monitors the build, checks for runtime errors, and auto-fixes failures.

## Usage

- `/deploy-verify` — merge the current branch's PR and monitor deployment
- `/deploy-verify 123` — merge PR #123 and monitor
- `/deploy-verify --check-only` — skip merge, just verify the latest deployment is healthy
- `/deploy-verify --no-fix` — monitor and report issues but don't auto-fix

## Steps

### 1. Identify the PR

- If a PR number was provided, use it
- Otherwise, run `gh pr list --head $(git branch --show-current)` to find the PR for the current branch
- If no PR found, tell the user and stop
- Show the PR title and status before proceeding

### 2. Pre-merge Checks

Run in parallel:

- `gh pr checks` — verify all CI checks pass
- `gh pr view --json mergeable` — verify the PR is mergeable

If checks are failing:

- Show which checks failed
- Ask the user if they want to proceed anyway or fix first
- Do NOT merge if checks are failing without explicit user approval

### 3. Merge (unless --check-only)

```bash
gh pr merge --squash --delete-branch
```

Use `--squash` by default for clean history. Tell the user the merge is done.

### 4. Monitor Deployment

After merging, the deployment pipeline starts. Monitor it:

**If Vercel project (check for vercel.json or .vercel/):**

- Run `vercel ls --limit 1` to get the latest deployment
- Poll `vercel inspect <deployment-url>` every 30 seconds (max 5 minutes) until state is READY or ERROR
- If the project doesn't have Vercel CLI configured, fall back to checking the deployment URL directly

**If no Vercel detected:**

- Ask the user what deployment system to check, or skip to verification

### 5. Build Failure Recovery (unless --no-fix)

If the build fails:

1. Read the build logs: `vercel logs <deployment-url>` or check CI output
2. Diagnose the root cause (common: Node version, missing env vars, type errors, dependency issues)
3. Show the diagnosis to the user
4. Ask: "Want me to fix this and push a follow-up commit?"
5. If yes:
   - Create a new branch: `git checkout -b fix/deploy-$(date +%s)`
   - Implement the fix
   - Commit with `fix: resolve deployment failure — [description]`
   - Push and create a new PR
   - Optionally re-run `/deploy-verify` on the fix PR

### 6. Runtime Verification

Once the deployment is live, verify it's healthy:

**Health checks (run in parallel):**

- Curl the main page and key routes, check for 200 status codes
- Look for error indicators in response bodies (500 errors, "Internal Server Error", etc.)
- If the project has a `/api/health` or similar endpoint, check it

**Sentry check (if SENTRY_AUTH_TOKEN is available):**

- Query Sentry API for new errors in the last 10 minutes
- If new errors found, show stack traces and offer to diagnose

**If runtime errors found (unless --no-fix):**

1. Show the error details
2. Diagnose from stack trace or error message
3. Ask if user wants an auto-fix
4. Same fix flow as build failure (new branch, fix, PR)

### 7. Report

Display a deployment summary:

```
Deployment Report
─────────────────
PR:        #123 — feat: add user authentication
Merged:    ✓ (squash merged, branch deleted)
Build:     ✓ READY (took 2m 15s)
Health:    ✓ All routes returning 200
Sentry:    ✓ No new errors (or: ⚠ 2 new errors found)
URL:       https://your-app.vercel.app
```

If any issues were found and fixed, include:

```
Auto-fixes applied:
  - fix/deploy-1234567: resolved Node 24.x compatibility issue → PR #125
```
