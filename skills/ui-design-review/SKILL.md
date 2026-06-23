---
name: ui-design-review
description: Acts as a UI designer — reviews a written spec/PRD or a live design (URL, local dev server, or in-repo components), audits it against proven UI design principles, and returns a prioritized list of concrete fixes each with its reasoning, then uses the ux-mockup skill to visualize the suggestions as before→after mockups. Use when the user wants design feedback or a design critique, asks to "act as my UI designer", "review/critique this design", "audit this UI/spec", "suggest design fixes/improvements", "what would a designer change", "what's wrong with this screen", "make this look more professional", or "improve this page's design". Covers both pre-build specs and shipped/live interfaces.
---

# UI Design Review

Stand in for a UI designer: look at what's being built (a spec or a live design), say specifically what to fix and **why**, then show what the fixes look like as before→after mockups. The reasoning is as important as the fix — the user should learn the principle, not just take the change.

This skill pairs two halves:

1. **Critique** — audit against `references/design-heuristics.md` (a distilled, auditable rule set from _Refactoring UI_) and produce a prioritized, reasoned findings report.
2. **Visualize** — invoke the **ux-mockup** skill to render the current state and the redesigned state side by side, with the reasoning carried in design-note callouts.

## Workflow

1. **Acquire the design** — figure out the input type and get an accurate picture of it.
2. **Audit** — walk every heuristic category, flagging concrete violations tied to specific elements.
3. **Report** — write the prioritized critique (High → Medium → Low), each finding with fix + reasoning.
4. **Visualize** — chain into `ux-mockup` to show before→after for the highest-impact fixes.
5. **Iterate** — refine via the mockup's feedback loop until approved.

Always read `references/design-heuristics.md` before auditing — it is the rule set every finding cites.

## Step 1 — Acquire the design

Identify which of three inputs you're reviewing, and capture it faithfully. **Never critique from a vague mental image** — work from the real spec text, real rendered UI, or real source.

| Input                                     | How to acquire                                                                                                                                                                                                       |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Written spec / PRD / description**      | Read the file(s) or the pasted text in full. Audit the _proposed_ UI it describes; where the spec is silent on a design decision, treat that silence itself as a finding ("spec doesn't define empty/error states"). |
| **Live design** (URL or local dev server) | Capture the **actual rendered UI** — see capture strategies below. Audit what real users see, not the source's intent.                                                                                               |
| **In-repo components / code**             | Read the component source + the project's CSS/Tailwind config/design tokens. Audit the rendered result, reading styles to infer it; render it if a dev server is available.                                          |

### Capturing a live design (priority order)

1. **Screenshot via browser tooling** — preferred for live/local pages. Use the `testing-webapps` or `manual-qa-collab` skills (Playwright MCP / Claude for Chrome) to load the page and screenshot it at both mobile (~400px) and desktop widths, then look at the images. Visual review needs to _see_ the pixels.
2. **WebFetch** — for public URLs when no browser tooling is available: fetch the page, read the HTML/CSS structure. Weaker than a screenshot (no rendered pixels) — note that limitation in the report.
3. **Ask the user** — if the page is auth-gated or otherwise unreachable, ask for a screenshot (and, if possible, the DevTools "Copy outerHTML" so the mockup step can reproduce it exactly).

Capture **both viewports** when feasible — many findings (line length, full-bleed, fixed width, mobile-first) only surface at one width.

## Step 2 — Audit against the heuristics

Open `references/design-heuristics.md` and go category by category:

- **A. Key principles** — personality, systematization, spacing, mobile-first, columns, fresh thinking
- **B. Do** — visual hierarchy, fixed width, letter-spacing, line-height, weight/contrast, scale, accessibility, defaults
- **C. Don't** — labels, ambiguous spacing, borders, line length, full-bleed, centered prose, scaled assets
- **D. Tips & tricks** — shadows, accent borders, overlap, text-on-image, backgrounds
- **E. Beware** — user content, empty states
- **F. Color** — HSL, palette size, defined shades, saturation/lightness, grey temperature, grey-on-color text
- **G. Depth & light** — single light source, elevation/shadow system, depth without shadows
- **H. Type selection & setting** — typeface choice, type scale, baseline alignment, number/justify polish
- **I. Process** — feature-first, low-fidelity-first, don't-design-too-much (most relevant for specs / WIP)
- **J. Imagery** — photo quality

For each heuristic, look for a concrete violation in _this_ design. A real finding names the **exact element and location**, not a generic principle. Skip heuristics that genuinely don't apply — do not pad the report. Use the severity guidance at the end of the reference to rank findings.

Lead with hierarchy, contrast/accessibility, spacing, and line length — these move perceived quality the most and are the most common failures.

## Step 3 — Write the critique

Open with a 2–3 sentence **overall read**: the design's current personality/strengths and the single biggest opportunity. Then list findings, **sorted High → Medium → Low**, in this format:

```markdown
### [Severity] Short title · principle <ID>

- **Where:** the specific element / screen region
- **Now:** what it currently does (the violation)
- **Fix:** the concrete change to make
- **Why:** the reasoning — the principle + the user-facing impact
```

Example:

```markdown
### [High] No visual hierarchy in the dashboard header · principle B1

- **Where:** Top card row — "Revenue", "Users", "Churn" all 24px/600 in the same brand blue.
- **Now:** Three metrics compete equally; nothing signals which one matters.
- **Fix:** Make the primary metric (Revenue) larger and higher-contrast; drop the
  others to a grey label + dark value, no color. Reserve blue for the one CTA.
- **Why:** Hierarchy should be built with weight and color, not uniform size (B1).
  When everything shouts, the eye has no entry point and the screen reads as noise.
```

Rules for good critique:

- **Be specific and falsifiable.** "Improve spacing" is useless; "the section heading sits 16px from both the block above and below — tie it to the block it introduces (≤8px) and push 32px above" is actionable.
- **Reasoning-first.** Every fix states the _why_. The user is hiring a designer to learn judgment, not just receive edits.
- **Prioritize ruthlessly.** A wall of 30 nitpicks is worse than 6 high-impact fixes. Cap Low/polish items unless asked for a full sweep.
- **Respect intent and existing systems.** Don't impose a new personality (A1) or rebuild a working design system unless the user asks. Work within their fonts, colors, and brand. Flag a personality mismatch as a finding; don't unilaterally replace it.
- **Distinguish fact from taste.** Contrast ratios, line length, color-only meaning are near-objective. Personality and decorative choices are judgment calls — label them as such.

## Step 4 — Visualize with ux-mockup

Show what the suggestions look like by invoking the **ux-mockup** skill (via the Skill tool). This is the half that makes the critique tangible.

Hand ux-mockup a clear brief so it builds **before→after versions in one section** (its version-nav pattern), not separate pages:

- **v1 — "Current"**: the design as it is now.
  - Live design → use ux-mockup's **live-capture** mode (iframe or verbatim HTML) for pixel-accurate reproduction.
  - Spec/from-scratch → build a faithful rendering of what the spec describes today.
- **v2 — "Redesigned"**: the same screen with the **High** (and clear Medium) fixes applied. This version is the `active` one so the user sees the improvement first.
- If fixes trade off against each other or you want to show options, add **v3+** as alternatives.

**Carry the reasoning into the mockup.** Each version gets `design-note` callouts that name what changed and why, mirroring the report:

```html
<div class="design-note">
  <strong>Change (B1 · hierarchy):</strong> Revenue scaled up + darkened;
  secondary metrics demoted to grey labels. Blue now used only on the primary
  CTA so the eye lands on the one number that matters.
</div>
```

Scope the mockup to the **highest-impact screens** — one or two — not every finding. The mockup is a persuasion and review artifact; it should make the top fixes obvious at a glance. ux-mockup then drives the open-in-browser → collect-feedback → iterate-in-place loop.

## Step 5 — Iterate

Use ux-mockup's feedback loop: the user reviews, edits the per-section feedback, and copies the JSON back. Apply changes as new versions **in the same file** (ux-mockup handles the version mechanics). Re-audit the redesigned version against the heuristics before declaring it done — a fix for one principle can introduce a violation of another (e.g. raising contrast for B5 can break the personality A1 was holding).

## Scope notes

- This skill is **design critique + visualization**, not implementation. Stop at the approved mockup unless the user asks to apply changes to real code (then hand off to `frontend-design` / the project's component code).
- For a spec with no UI yet, the mockup's v1 is your faithful interpretation of the spec — label it as such so the user can correct misreadings before reviewing the redesign.
- It reviews **visual/interaction design**, not copy editing, IA strategy, or code quality — mention those only when a design finding depends on them.
