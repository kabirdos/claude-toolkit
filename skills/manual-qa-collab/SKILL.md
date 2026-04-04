---
name: manual-qa-collab
description: Collaborative manual QA testing using Playwright MCP browser automation. Walk through QA flows interactively — navigating, clicking, filling forms, taking screenshots, and reporting pass/fail per step. Pauses for human judgment on visual/subjective checks. Use when testing a deployed site against a QA checklist, running through user flows manually, verifying bug fixes in production, or doing pre-launch QA. Triggers on "QA test", "manual QA", "test the flows", "run through the checklist", "check the site", "verify the deploy", "test this in the browser", "walk through the app".
---

# Manual QA Collab

Collaborative QA testing via Playwright MCP. Automate navigation and interaction; pause for human judgment on visual and subjective checks.

## Setup

1. Confirm Playwright MCP tools are available (`browser_navigate`, `browser_snapshot`, `browser_click`, etc.). If not, inform the user.
2. Ask the user for:
   - **Target URL** (e.g. `https://appealmailer.com`)
   - **QA checklist location** (e.g. `docs/qa/checklist.html`) or ask them to describe the flows
   - **Scope**: all flows, specific flows, or only flows affected by recent changes
3. If a checklist HTML file exists, read it to extract flows and steps. Look for JavaScript arrays like `const FLOWS = [...]` containing `title` and `steps` fields.

## Workflow

For each flow:

1. **Announce** the flow name and number of steps
2. **Execute** each step:
   - `browser_snapshot` before every interaction (to get fresh element refs)
   - `browser_click`, `browser_fill_form`, `browser_type`, `browser_file_upload` as needed
   - `browser_wait_for` when waiting for async operations (AI responses, redirects, deploys)
   - `browser_take_screenshot` to capture evidence on failures or for visual checks
3. **Report** each step as PASS, FAIL, or NEEDS_REVIEW
4. For **subjective checks** (layout, design, content quality), take a screenshot and ask the user to confirm
5. For **destructive actions** (delete, payment), ask the user before proceeding
6. On **failure**, screenshot the current state, note the error, and ask whether to continue or stop

## Results Tracking

Maintain a running results table throughout the session:

```
| Flow | Step | Status | Notes |
|------|------|--------|-------|
```

At the end, output a final summary with pass/fail/skip counts per flow and overall.

## Rules

- Always `browser_snapshot` before clicking — never click stale refs
- Screenshot on any failure or unexpected state
- If a step requires authentication, navigate to the login page and ask the user to handle it
- Don't retry failed steps automatically — report and ask
- For file uploads, ask the user for the file path
- When testing recent code changes, focus on affected flows first
- If a step can't be automated (e.g. "check email inbox"), mark it SKIP with a note
- Save screenshots to a `qa-results/` directory with descriptive filenames

## Playwright MCP Patterns

See `references/playwright-patterns.md` for common interaction patterns.
