---
name: bug-fix
description: Test-driven bug fixing — reproduce with a failing test first, then implement the minimal fix, iterate until all tests pass, and create a PR
user-invocable: true
disable-model-invocation: true
---

# /bug-fix — Test-Driven Bug Fix

Fix bugs properly: reproduce first with a failing test, then implement the minimal fix, verify everything passes, and ship it.

## Usage

- `/bug-fix the login redirect loops infinitely after OAuth callback` — describe the bug, get a TDD fix
- `/bug-fix ISSUE-123` — if it looks like an issue number, try `gh issue view 123` for context
- `/bug-fix` — with no description, ask the user to describe the bug

## Steps

### 1. Understand the Bug

If an issue number was provided:

- Run `gh issue view <number>` to get the full description
- Extract the reproduction steps, expected vs actual behavior

If a text description was provided:

- Parse it for: what's broken, when it happens, expected behavior

If nothing was provided:

- Ask: "Describe the bug — what happens, what should happen, and any steps to reproduce."

### 2. Create a Feature Branch

```bash
git checkout -b fix/<short-kebab-description>
```

Use the bug description to create a meaningful branch name (e.g., `fix/login-redirect-loop`).

### 3. Investigate the Root Cause

Before writing any code, locate the problem:

- Search for relevant files using Grep/Glob based on the bug description
- Read the suspect code
- Form a hypothesis about the root cause

**IMPORTANT:** Keep investigation under 5 minutes. If you haven't found the root cause by then, state your best hypothesis and proceed to step 4. Don't rabbit-hole.

### 4. Write the Failing Test

Write a test that:

- Reproduces the exact bug scenario
- Asserts the EXPECTED (correct) behavior
- Currently FAILS because the bug exists

Place the test in the appropriate test file following the project's conventions:

- Look at existing test files for patterns (Vitest, Jest, Playwright, etc.)
- Match the test style and location of nearby tests
- Use a descriptive test name: `it('should redirect to dashboard after OAuth callback, not loop')`

Run the test to confirm it fails:

```bash
# Use whatever test command the project uses
npm test -- --grep "your test name"
# or
npx vitest run path/to/test.ts
# or
npx jest path/to/test.ts
```

If the test passes (bug not reproduced):

- Re-examine your understanding of the bug
- Adjust the test to better capture the failure condition
- If you still can't reproduce it, tell the user and ask for more context

### 5. Implement the Minimal Fix

Write the smallest possible code change that makes the failing test pass:

- Fix the root cause, not the symptom
- Don't refactor surrounding code
- Don't add features
- Don't "improve" things that aren't broken

### 6. Verify

Run the full test suite (not just the new test):

```bash
npm test
# or whatever the project's test command is
```

**If tests fail:**

- If YOUR new test fails: adjust the fix, try again
- If OTHER tests fail: you introduced a regression — fix it
- Loop until ALL tests pass (max 3 iterations, then ask user for help)

**If the project has type checking:**

```bash
npx tsc --noEmit
# or npm run typecheck
```

### 7. Commit and PR

Once all tests pass:

1. Stage the changes (test file + fix):

```bash
git add <specific-files>
```

2. Commit with conventional format:

```bash
git commit -m "fix: <description of what was broken and how it's fixed>"
```

3. Push and create PR:

```bash
git push -u origin fix/<branch-name>
gh pr create --title "fix: <short description>" --body "$(cat <<'EOF'
## Summary
- **Bug:** <what was broken>
- **Root cause:** <why it was broken>
- **Fix:** <what the fix does>

## Test plan
- [x] Added failing test that reproduces the bug
- [x] Implemented minimal fix
- [x] All existing tests still pass
- [ ] Manual verification: <steps to verify in browser/app>
EOF
)"
```

### 8. Report

```
Bug Fix Complete
────────────────
Bug:        <description>
Root cause: <what caused it>
Fix:        <what changed>
Test added: <test file and test name>
PR:         <PR URL>
Files:      <list of modified files>
```
