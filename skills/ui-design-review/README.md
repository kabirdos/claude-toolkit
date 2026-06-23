# ui-design-review

> Acts as a stand-in UI designer — audits a spec or a live design against the principles in _Refactoring UI_, returns a prioritized list of fixes (each with its reasoning), then renders before→after mockups so you can see the change.

## Use this when...

- You have a **design or a spec and want a second pair of eyes** — "what would a designer change here?"
- You want fixes that come with the **why**, so you learn the principle, not just take the edit
- You're **pre-build** (a PRD/spec with no UI yet) and want the design decisions pressure-tested before anyone writes code
- You've **shipped a screen that feels off** but can't articulate what's wrong ("make this look more professional")
- You want the critique **made tangible** — before→after mockups, not just a wall of text

## What you say to Claude

```
Act as my UI designer and review the /dashboard page —
tell me what to fix and show me what it'd look like.
```

Claude captures the design (reads the spec, or screenshots the live/local page), audits it category by category against a distilled rule set from _Refactoring UI_, and writes a prioritized critique. Each finding follows a fixed shape — **Where / Now / Fix / Why** — sorted High → Medium → Low. Then it chains into [`ux-mockup`](../ux-mockup/README.md) to render the current state and the redesigned state side-by-side, with the reasoning carried in design-note callouts.

## Install

```bash
# From the claude-toolkit repo
./install.sh --skills ui-design-review             # into current project
./install.sh --global --skills ui-design-review    # into ~/.claude (all projects)
```

After install, Claude invokes this skill when you ask for a design critique — _"review/critique this design"_, _"audit this UI/spec"_, _"act as my UI designer"_, or _"what's wrong with this screen"_. You can also trigger it explicitly: _"use the ui-design-review skill to..."_.

New to skills? See the [main README](../../README.md#what-is-a-skill) for a one-minute primer.

## How it works

1. **Acquire** — figure out the input (written spec, live URL/dev server, or in-repo components) and capture it faithfully. Never critiques from a vague mental image: it reads the real spec text, screenshots the real rendered UI, or reads the real source.
2. **Audit** — walks every heuristic category in `references/design-heuristics.md`, flagging concrete violations tied to specific elements at both mobile and desktop widths.
3. **Report** — a prioritized critique (High → Medium → Low), each finding with a concrete fix _and_ its reasoning.
4. **Visualize** — chains into `ux-mockup` for before→after versions of the highest-impact screens.
5. **Iterate** — refines through the mockup's feedback loop, re-auditing the redesign before calling it done.

## The heuristics

`references/design-heuristics.md` is a distilled, auditable rule set drawn from _Refactoring UI_ (Adam Wathan & Steve Schoger), organized into ten sections **A–J** with stable IDs (A1, B7, F6, …) that every finding cites:

| Section | Covers                                                                      |
| ------- | --------------------------------------------------------------------------- |
| A       | Key principles — personality, systematization, spacing, mobile-first        |
| B       | Do — visual hierarchy, line-height, weight/contrast, scale, accessibility   |
| C       | Don't — ambiguous spacing, borders, line length, full-bleed, centered prose |
| D       | Tips & tricks — shadows, accent borders, overlap, text-on-image             |
| E       | Beware — real user content, empty states                                    |
| F       | Color — HSL, palette size, defined shades, grey temperature                 |
| G       | Depth & light — single light source, elevation/shadow system                |
| H       | Type — typeface choice, type scale, baseline alignment                      |
| I       | Process — feature-first, low-fidelity-first, don't design too much          |
| J       | Imagery — photo quality                                                     |

> **Editing note:** the section IDs (A1, B1, F6, …) are referenced from `SKILL.md` and cross-linked inside the reference. Keep IDs stable when editing — renumbering breaks the cross-links.

## Scope

It reviews **visual/interaction design and produces mockups** — it is not implementation. It stops at the approved mockup unless you ask to apply the changes to real code (then it hands off to [`frontend-design`](../frontend-design/README.md) or your component code). It also doesn't do copy editing, IA strategy, or code review — only where a design finding depends on them.

## See also

- [`ux-mockup`](../ux-mockup/README.md) — the visualization half; this skill chains into it for before→after mockups
- [`frontend-design`](../frontend-design/README.md) — for implementing the approved design once the critique converges
