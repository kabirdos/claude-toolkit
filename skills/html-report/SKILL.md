---
name: html-report
description: "Use when research, analysis, or synthesis results need to be presented as a polished, readable HTML report. Triggers after /research-orchestrator, /last30days, or any skill that produces structured findings. Also use when the user asks for a 'report', 'write-up', or 'summary page' of work done in the current session."
user-invocable: true
argument-hint: '/html-report ~/active/research-file.md "Title of Report"' or '/html-report --fresh'
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# HTML Report Generator

Converts structured research, analysis, or synthesis content into a polished, NYTimes-editorial-style HTML page. Designed to be called after other skills produce findings.

## Storage

Reports are saved to **`~/Documents/Claude Reports/`** — discoverable in Finder, indexed by Spotlight, never inside any git repo.

Filename format: `{slug}-{YYYY-MM-DD}.html`
Example: `youtube-pipeline-2026-04-02.html`

## Step 0: Check for `--fresh` Flag

If `--fresh` appears anywhere in the arguments, use the **Fresh Theme System** (see below) instead of the default editorial style. Strip `--fresh` from arguments before parsing the rest.

If `--fresh` is NOT present, use the default Newsreader/Inter editorial style defined in Step 3.

## Step 1: Determine Input

The skill accepts input in three ways (check in order):

1. **Argument path** — if the user passed a file path, read that file as the source content.
2. **Current session context** — if no path given, look for research/synthesis content already produced in this conversation (e.g., from /research-orchestrator, /last30days, or any analysis work). Use that directly.
3. **Ask** — if neither is available, use AskUserQuestion to ask what content should be in the report.

If a title was provided as the second argument, use it. Otherwise, infer the title from the content's main heading or topic.

## Step 2: Extract Structure

Parse the source content and identify these sections (not all will be present — include only what exists):

- **Title & subtitle** — the main topic and a one-line description
- **Executive summary** — the lead paragraph(s)
- **Key findings** — numbered or bulleted insights, with confidence levels if available
- **Diagrams/architecture** — pipeline flows, decision trees, system architecture
- **Tables/matrices** — comparison tables, decision matrices, cost breakdowns
- **Recommendations** — actionable takeaways
- **Timeline/roadmap** — phased implementation plans
- **Sources** — links grouped by category

## Step 3: Generate HTML

Create a single self-contained HTML file (no external dependencies except Google Fonts). The design follows these principles:

### Typography

- **Headline font:** Newsreader (Google Fonts) — large, editorial serif
- **Body font:** Newsreader for prose, Inter for labels/UI elements
- **Code font:** Source Code Pro for code blocks, file paths, tool names
- **Base font size:** 20px on desktop, 18px on mobile
- **Line height:** 1.7 for body text
- **Max column width:** 680px for prose, 900px for tables/diagrams

### Layout & Style

- **Light mode** — warm off-white background (#faf9f7), dark ink (#1a1a1a)
- **Masthead** with title, subtitle, date, and metadata
- **Section dividers** with thin borders between major sections
- **Dropcap** on the first paragraph of the executive summary
- **Pull quotes** for the single most important insight (bordered top and bottom)
- **Numbered findings** with colored confidence tags (green for HIGH, amber for MEDIUM)
- **Cost breakdowns** as card components with dotted-line rows
- **Roadmap/timeline** as a vertical dot-and-line timeline
- **Recommendation cards** in a 2-column grid
- **Source links** grouped by category, all clickable
- **Resource links** on all mentioned tools, plugins, products, YouTube videos, and external resources (see Resource Linking below)
- **Fade-up animations** on section load

### Resource Linking (always enabled)

Every mention of a tool, plugin, product, YouTube video, website, or external resource in the report MUST be a clickable `<a>` link to its canonical URL (homepage, OBS Forums page, GitHub repo, YouTube video, etc.). This applies everywhere — plugin cards, reference tables, prose paragraphs, recommendation cards, and video listings. Use `target="_blank"` on all external links.

**Where to link:**

- **Plugin/tool names** → official homepage, OBS Forums resource page, or GitHub repo
- **YouTube video titles** → the YouTube video URL
- **Product names** (Descript, CapCut, etc.) → the product homepage
- **X handles** → `https://x.com/{handle}`
- **Subreddit names** → `https://reddit.com/r/{sub}`
- **First mention of the primary subject** (e.g., "OBS Studio") → its official site

**Link styling:** Include CSS for links that fits the editorial style — subtle underlines with hover effects, inheriting color from their context (ink for headings, blue for prose, ink-light for table cells).

### Components to Use (select based on content)

**Always include:**

- Masthead (title, subtitle, date)
- Executive summary with dropcap

**Include if content has them:**

- Pipeline/flow diagram (horizontal stages with arrows)
- Findings list with confidence tags
- Decision matrix table
- Cost card
- Roadmap timeline
- Recommendation cards grid
- Source list grouped by category
- Pull quote (pick the single best insight)
- Code/architecture block (dark theme)

### CSS Variables

```css
:root {
  --serif: "Newsreader", Georgia, serif;
  --sans: "Inter", -apple-system, sans-serif;
  --mono: "Source Code Pro", monospace;
  --ink: #1a1a1a;
  --ink-light: #4a4a4a;
  --ink-muted: #888;
  --bg: #faf9f7;
  --bg-card: #fff;
  --accent: #c41e3a;
  --accent-light: #fdf0f2;
  --border: #e0ddd8;
  --border-light: #eeeae5;
  --blue: #1a5276;
  --blue-light: #eaf2f8;
  --green: #1e8449;
  --green-light: #eafaf1;
  --highlight: #fff3cd;
}
```

### Inline Linking (replaces separate Sources section)

**Do NOT include a "Sources" section at the end of the report.** Instead, every reference must be linked inline where it is mentioned. The report should read like a well-edited article where clicking any tool name, product, video, or resource takes you directly there.

- First mention of every tool/product in prose → wrap in `<a href="..." target="_blank">`
- Findings that cite a source → link the relevant noun, not a bare URL
- Tables listing tools → every tool name in the table is a link
- Recommendation cards mentioning a tool → link it
- If a source URL exists in the raw data, it MUST appear as an inline link somewhere in the HTML

**No bare URLs anywhere in the rendered page.** Every link is contextual text.

## Step 4: Save Source Markdown

If the report was generated from a markdown file (argument path or accumulation file):

1. Copy the source `.md` file to `~/Documents/Claude Reports/{slug}-{YYYY-MM-DD}.md`
2. This preserves the raw research alongside the formatted report

If the report was generated from session context (no file), write the synthesized content as a `.md` file with the same slug.

## Step 5: Save HTML & Open

1. Generate a URL-safe slug from the title (lowercase, hyphens, max 50 chars).
2. Write the HTML file to `~/Documents/Claude Reports/{slug}-{YYYY-MM-DD}.html`.
3. Run `open` to launch it in the user's default browser.
4. Report the file path to the user.

If a file with the same name already exists, append a counter: `-2`, `-3`, etc.

## Step 6: Confirm

Tell the user:

```
Report saved to:
  HTML: ~/Documents/Claude Reports/{filename}.html
  Source: ~/Documents/Claude Reports/{filename}.md
Opened in your browser.
```

## Usage Patterns

**After /research-orchestrator:**

```
/research-orchestrator "best vector databases for RAG"
... (research runs) ...
/html-report
```

The skill reads the research output from the session and generates the report.

**With a specific file:**

```
/html-report ~/active/research-2026-04-02-claude-native.md "Claude-Native YouTube Pipeline"
```

**After any analysis work:**

```
(user does a code review, architecture analysis, competitive analysis, etc.)
/html-report "Code Review: Authentication Module"
```

## Quality Checklist

Before writing the file, verify:

- [ ] Every mentioned tool, plugin, product, video, and resource is a clickable `<a>` link to its canonical URL (`target="_blank"`)
- [ ] All links are clickable `<a>` tags with `href`
- [ ] Tables are responsive (wrapped in overflow-x: auto div)
- [ ] Font imports load from Google Fonts CDN
- [ ] No external JS dependencies — CSS-only animations
- [ ] Mobile responsive (font size, grid collapse, table scroll)
- [ ] File is fully self-contained (inline CSS, no external stylesheets beyond fonts)
- [ ] Dropcap renders correctly on the first paragraph
- [ ] Report footer credits the source skill that generated the content

---

## Fresh Theme System (`--fresh`)

When `--fresh` is passed, **replace Step 3's default typography, colors, and layout** with a randomized combination selected from the pools below. All other steps (structure extraction, inline linking, saving, etc.) remain identical.

### How to Pick a Theme

Use the current date + report title to seed your choices. Pick **one option from each pool** — the combination should feel cohesive (don't pair a playful font with an austere color palette). Think of it as dressing a report: the "outfit" changes but the "person" (content structure) stays the same.

**Before generating CSS, state your choices in a brief comment to yourself:**

```
Theme: Fraunces + Outfit, terracotta accent, wide asymmetric layout, cool gray bg, soft rounded cards
```

### Pool 1: Font Pairings (pick one)

Each pair is: Display/Headline + Body/UI. All available on Google Fonts.

| #   | Headline            | Body              | Vibe                 |
| --- | ------------------- | ----------------- | -------------------- |
| 1   | Playfair Display    | Source Sans 3     | Classic editorial    |
| 2   | Fraunces            | Outfit            | Warm organic         |
| 3   | Lora                | Karla             | Bookish clean        |
| 4   | DM Serif Display    | DM Sans           | Modern contrast      |
| 5   | Instrument Serif    | Instrument Sans   | Refined contemporary |
| 6   | Libre Baskerville   | Nunito Sans       | Academic accessible  |
| 7   | Bricolage Grotesque | IBM Plex Sans     | Technical bold       |
| 8   | Young Serif         | Plus Jakarta Sans | Friendly editorial   |

Keep `Source Code Pro` or `JetBrains Mono` for code in all themes.

### Pool 2: Color Palettes (pick one)

Each palette defines: accent, accent-light, background, card, ink, and border tones.

| #   | Name       | Accent  | Background               | Feel                  |
| --- | ---------- | ------- | ------------------------ | --------------------- |
| 1   | Terracotta | #c45d3e | #faf6f2 (warm cream)     | Earthy, warm          |
| 2   | Indigo     | #3d5a99 | #f5f6fa (cool blue-gray) | Technical, calm       |
| 3   | Forest     | #2d6a4f | #f4f9f4 (pale green)     | Natural, fresh        |
| 4   | Slate      | #475569 | #f8fafc (cool white)     | Neutral, modern       |
| 5   | Plum       | #7c3aed | #faf5ff (lavender tint)  | Creative, bold        |
| 6   | Amber      | #b45309 | #fffbeb (warm yellow)    | Energetic, optimistic |
| 7   | Ink        | #1e293b | #ffffff (pure white)     | High-contrast, sharp  |
| 8   | Rose       | #be185d | #fff1f2 (blush)          | Distinctive, warm     |

Derive `accent-light`, `border`, `border-light`, `ink-light`, `ink-muted` from the chosen palette to maintain harmony. The `--green` (for HIGH tags) and `--highlight` (for MEDIUM tags) stay functional regardless of palette.

### Pool 3: Layout Mode (pick one)

| #   | Mode                | Description                                                                                                                                        |
| --- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Centered column** | Default — 680px prose, 900px wide sections. Classic editorial.                                                                                     |
| 2   | **Wide asymmetric** | 740px prose shifted left, 1000px for tables. Left-weighted with generous right margin. Masthead left-aligned.                                      |
| 3   | **Compact dense**   | 600px prose, tighter line-height (1.55), smaller base font (18px), more content per screen. Good for data-heavy reports.                           |
| 4   | **Magazine spread** | Prose sections alternate between left-aligned (60% width) and right-aligned. Pull quotes span full width. Findings use 2-column layout on desktop. |

### Pool 4: Background Treatment (pick one)

| #   | Treatment             | CSS                                                                                                                                                                 |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Solid**             | Just the palette background color. Clean.                                                                                                                           |
| 2   | **Subtle grain**      | Add a CSS noise texture overlay at low opacity: `background-image: url("data:image/svg+xml,...")` using an inline SVG noise pattern at 3-5% opacity.                |
| 3   | **Top gradient fade** | A 300px gradient from a slightly tinted version of the bg color to transparent at the top of the page. Adds depth to the masthead.                                  |
| 4   | **Paper texture**     | Subtle `box-shadow: inset 0 0 100px rgba(0,0,0,0.03)` on the body, plus faint border on the main content area to simulate a paper sheet floating on the background. |

### Pool 5: Component Styling (pick one)

| #   | Style                | Description                                                                                                                                  |
| --- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Soft rounded**     | `border-radius: 8px` on cards, 50% on badges. Softer shadows (`box-shadow: 0 1px 3px rgba(0,0,0,0.06)`). Gentle.                             |
| 2   | **Sharp editorial**  | `border-radius: 0`. No shadows. Heavy use of border-top/bottom rules. Pull quotes get thick left borders instead of top/bottom.              |
| 3   | **Minimal outlined** | `border-radius: 4px`. 1px borders only, no fills on cards (transparent bg). Tags are outlined instead of filled.                             |
| 4   | **Bold blocks**      | Cards have thick accent-colored left borders. Section headings get accent underlines. Tags are filled with accent color. High visual weight. |

### Readability Constraints (NEVER break these)

Regardless of theme choices, these rules are absolute:

- Base font size: 18px minimum, 22px maximum
- Line height: 1.55 minimum, 1.8 maximum
- Prose column: 580px minimum, 760px maximum
- Body text color contrast: WCAG AA minimum (4.5:1 against background)
- Links must be visually distinguishable from body text (color or underline)
- Tables must scroll horizontally on mobile
- All Google Fonts must load via `<link>` in `<head>`
- The page must be fully self-contained (no external JS/CSS beyond fonts)

### Example Fresh Invocations

```
/html-report --fresh
/html-report --fresh ~/active/research.md "Vector Database Comparison"
/html-report --fresh "Code Review: Auth Module"
```
