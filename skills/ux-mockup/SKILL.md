---
name: ux-mockup
description: Create interactive HTML mockups for UX design review with built-in feedback collection, version history, and clipboard export. Use when designing UI flows, page layouts, or component states that need visual review and iterative feedback. Triggers on "mockup", "UX design", "design review", "visual design", "UI mockup", "mock up the flow", "show me what it looks like", or any request to create visual designs for review before implementation.
---

# UX Mockup

Create self-contained HTML mockup pages for iterative UX design review. The mockup includes per-section feedback textareas, version history navigation, and one-click JSON clipboard export.

## Workflow

1. **Understand scope** — identify what states, pages, or components to mock up
2. **Generate mockup** — create a single HTML file using the shell template
3. **Open in browser** — `open <path>` so the user can review
4. **Collect feedback** — user fills in feedback textareas and copies JSON to clipboard
5. **Iterate in place** — update the same file, wrapping old content as a prior version
6. **Repeat** until approved

## Generating a Mockup

Use `assets/mockup-shell.html` as the structural reference. Build a single self-contained HTML file at `docs/mockups/<name>.html` with:

- **Sticky nav bar** — title + anchor links to each section + "Copy All Feedback" button
- **Sections** — one per state/page/component, each wrapped in `.mockup-section[data-section-id]`
- **Version containers** — design content inside `.version[data-version="1"]`
- **Feedback area** — textarea under each section
- **Version nav** — prev/next buttons (hidden until v2+ exists)
- **All CSS/JS inline** — no external dependencies

### Section structure

```html
<div class="mockup-section" data-section-id="state1" id="state1">
  <span class="section-label">State 1 — Description</span>
  <p class="section-desc">What this state shows and why.</p>

  <div class="version-container">
    <div class="version active" data-version="1">
      <!-- Actual design mockup content here -->
    </div>
  </div>

  <div class="version-nav">
    <button data-dir="prev" disabled>&larr; Prev</button>
    <span class="version-label">v1 of 1</span>
    <button data-dir="next" disabled>Next &rarr;</button>
  </div>

  <div class="feedback-area">
    <label for="fb-state1">Feedback</label>
    <textarea
      id="fb-state1"
      placeholder="Voice transcribe or type feedback for this section..."
    ></textarea>
    <div class="char-count"></div>
  </div>
</div>

<div class="section-divider"></div>
```

### Design note callouts

Use callouts to annotate design decisions:

```html
<div class="design-note">
  <strong>Change:</strong> Description of what changed.
</div>
<div class="design-note future">
  <strong>Future:</strong> Planned but not in scope.
</div>
<div class="design-note info">
  <strong>Note:</strong> Context for reviewers.
</div>
```

## Iterating on Feedback

When the user provides feedback (either pasted JSON or verbal), update the SAME HTML file:

1. **For each section with changes**, wrap the existing `.version` div content as-is and add a new `.version` div with incremented `data-version`
2. **Set the new version as `active`**, remove `active` from old versions
3. **Do NOT create a new file** — always edit in place so the user can refresh
4. The version-nav JS auto-detects multiple versions and shows prev/next buttons

### Version iteration example

Before (v1 only):

```html
<div class="version-container">
  <div class="version active" data-version="1">
    <!-- original design -->
  </div>
</div>
```

After iteration (v1 + v2):

```html
<div class="version-container">
  <div class="version" data-version="1">
    <!-- original design preserved -->
  </div>
  <div class="version active" data-version="2">
    <!-- updated design -->
  </div>
</div>
```

The user can flip between v1 and v2 using the prev/next buttons on that section.

## Feedback JSON Format

When the user clicks "Copy All Feedback", this JSON is copied to clipboard:

```json
{
  "mockup": "Page Title",
  "timestamp": "2026-02-18T...",
  "sections": {
    "state1": {
      "feedback": "The button should be larger...",
      "viewing_version": 2,
      "total_versions": 2
    },
    "state4": {
      "feedback": "Arrow should point left...",
      "viewing_version": 1,
      "total_versions": 1
    }
  }
}
```

Parse this to understand which sections have feedback and which version the user was viewing when they wrote it.

## Styling Guidelines

- Match the project's visual style when possible (read existing CSS/Tailwind config)
- Use project colors and fonts if available
- Fall back to clean, neutral styling from the shell template
- Keep mockups realistic — use real-looking content, not lorem ipsum
- Use `.wide` class on sections that need more horizontal space (dashboards, tables)

## Key Rules

- **One file, always** — never create multiple mockup files for the same feature
- **Edit in place** — user refreshes browser to see changes, no new pages
- **Preserve versions** — never delete old version content, wrap it
- **Self-contained** — all CSS and JS inline, no CDN dependencies except fonts
- **Feedback areas always present** — every section gets a textarea
- **Open after generating** — always run `open <path>` after creating or updating
