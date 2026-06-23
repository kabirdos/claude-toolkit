# Design Heuristics

The auditable rule set for UI design review. Distilled from **_Refactoring UI_** by
Adam Wathan & Steve Schoger (the `erikuus/good-ui` summary plus the full book). Each entry
is written as **Spot it → Fix → Why** so a finding can be raised concretely against a real element.

When auditing, walk every category. For each heuristic, look for a concrete violation in
the design under review, name the exact element and location, then state the fix and the
reasoning. Skip heuristics that don't apply rather than forcing a finding.

## Contents

- [A. Key principles](#a-key-principles) — personality, systems, space, elimination, mobile-first, columns, fresh thinking
- [B. Do](#b-do) — hierarchy, fixed width, letter-spacing, line-height, weight/contrast, scale, accessibility, defaults
- [C. Don't](#c-dont) — labels, ambiguous spacing, borders, line length, full-bleed, centered prose, scaled icons
- [D. Tips & tricks](#d-tips--tricks) — shadows, accent borders, overlap, text-on-image, backgrounds, fresh ideas
- [E. Beware](#e-beware) — user content, empty states
- [F. Color](#f-color) — HSL, palette size, defining shades, saturation/lightness, grey temperature, grey-on-color
- [G. Depth & light](#g-depth--light) — light source, elevation system, depth without shadows
- [H. Type selection & setting](#h-type-selection--setting) — choosing fonts, type scale, baseline alignment, number/justify polish
- [I. Process](#i-process) — feature-first, low-fidelity-first, don't design too much
- [J. Imagery](#j-imagery) — photo quality
- [Severity guidance](#severity-guidance)

---

## A. Key principles

### A1. Choose a personality

- **Spot it:** The design has no consistent voice — generic system font, default border radius, arbitrary brand color, inconsistent copy tone.
- **Fix:** Commit to a personality across four levers: **font** (elegant = serif/no radius; playful = rounded sans + large radius; neutral = humanist sans + medium radius), **border radius**, **color** (blue = safe/trustworthy, gold = sophisticated, pink/bright = fun), and **language** (formal vs. friendly). Make all four point the same direction.
- **Why:** Personality is what separates a memorable product from a forgettable template. Mixed signals (playful color + formal copy + sharp corners) read as unfinished.

### A2. Systematize everything

- **Spot it:** Values are hand-picked — spacing like 13px/17px/23px, one-off hex colors, ad-hoc shadows, font sizes that don't repeat.
- **Fix:** Define small fixed scales and pick only from them: spacing (e.g. 4/8/12/16/24/32/48/64), font size, font weight, line height, color (primary + a few accents + a grey ramp), shadow (sm/md/lg), border radius, border width, opacity. You needn't define every system up front — add each as the decision recurs. _(Beyond the book: encode the scales as design tokens / a Tailwind preset.)_
- **Why:** Constraints kill decision fatigue and guarantee visual rhythm. You should never debate 1px differences.

### A3. Start with too much space

- **Spot it:** Cramped layout, elements touching, no breathing room, content packed edge-to-edge.
- **Fix:** Give elements far more space than feels necessary, then remove until it looks right — not the reverse. Generous whitespace almost always reads as cleaner and more premium.
- **Why:** Adding space to a cramped design is harder than removing it from a roomy one. (Exception: genuinely information-dense tools — dashboards, data tables — can justify compact density.)

### A4. Design by elimination

- **Spot it:** A value was chosen once and never tested against neighbors.
- **Fix:** Guess a starting value (say 16px), then try the steps on either side (12px, 24px) and compare side by side before committing.
- **Why:** The best value is only obvious in contrast. This is the mechanic behind every other "pick from a scale" decision.

### A5. Think mobile first

- **Spot it:** Design only exists at desktop width; mobile is an afterthought with broken wrapping or overflow.
- **Fix:** Design the ~400px canvas first, get it right, then widen. The desktop version usually needs less change than expected.
- **Why:** Constraints force prioritization of what matters; widening a focused mobile layout is easier than cramming a desktop one.

### A6. Think in columns

- **Spot it:** A component that reads best at a narrow width has been stretched full-width and now feels unbalanced/sparse.
- **Fix:** Instead of widening, split into columns (e.g. label/value pairs side by side, or a two-up card grid).
- **Why:** Width has a natural readable maximum; columns use horizontal space without harming legibility.

### A7. Think outside the box

- **Spot it:** Stock components used literally — plain dropdown, plain table, vertical radio list — where the UI is important enough to deserve craft.
- **Fix:** Break dropdowns into sections/columns with supporting text + icons; merge non-sortable table columns to add hierarchy; replace important radio groups with selectable cards.
- **Why:** Default component shapes are starting points, not constraints. Thoughtful variation signals quality.

---

## B. Do

### B1. Use a visual hierarchy

- **Spot it:** Everything competes for attention — uniform size/weight/color, primary and secondary actions look identical, every link is colored, destructive actions styled as prominently as the primary CTA.
- **Fix:**
  - Highlight the few most important elements; let the rest recede.
  - Build hierarchy with **color and weight**, not size alone (over-relying on size makes primary text huge and secondary text tiny).
  - Buttons in a **pyramid of importance**: one primary (solid), secondary (outline/soft), tertiary (link-style). Give destructive actions a secondary/tertiary treatment unless they are the page's primary action — then apply the bold red styling at the confirmation step.
  - **De-emphasize links** that aren't primary actions: they stay discoverable without a color, so they don't compete.
- **Why:** Hierarchy is the single biggest lever on whether an interface feels designed or chaotic. It tells the eye where to go.

### B2. Use a fixed width

- **Spot it:** Sidebars, forms, or media that stretch/shrink fluidly with the viewport — sidebar eating space on wide screens, truncating on narrow ones.
- **Fix:** Give elements optimized for their content a fixed width (sidebars, forms, cards, inline images). Let the main content area absorb the flex instead.
- **Why:** Fluid widths push elements past their useful size in both directions, causing wasted space or awkward wrapping/truncation.

### B3. Use letter-spacing effectively

- **Spot it:** Headlines set in a default-tracked font look loose; all-caps text looks cramped and hard to read.
- **Fix:** Use a tight display font for headlines, or tighten tracking (negative letter-spacing) on large text. **Loosen** letter-spacing on all-caps runs.
- **Why:** Default tracking is tuned for body text; large and all-caps text need adjustment to look intentional and stay readable.

### B4. Contextualize line-height

- **Spot it:** A single line-height applied everywhere — large headings with airy gaps, small body text packed tight, wide paragraphs hard to track.
- **Fix:** Scale line-height **inversely with font size** (small text needs ~1.5+; large display text can use ~1.0). Scale it **with line length** (narrow columns ~1.5; very wide measures up to ~2.0).
- **Why:** Line-height's job is helping the eye find the next line — that need depends on both type size and how far the eye must travel.

### B5. Balance weight and contrast

- **Spot it:** Thin text that's too low-contrast to read, or bold text so dark it shouts; secondary text that's hard to distinguish from primary.
- **Fix:** Trade weight against contrast. To soften heavy text, lower its contrast (lighter grey). To keep thin/small text legible, raise its contrast. Use the pair together to express importance.
- **Why:** Weight and contrast are two dials on the same outcome (emphasis + legibility); tuning them together avoids both shouting and disappearing text.

### B6. Scale disproportionately

- **Spot it:** A component shrunk/grown by uniformly scaling every property (font, padding, radius all ×0.5), producing toy-like or bloated results across breakpoints.
- **Fix:** Adjust properties independently — at smaller sizes reduce font less than padding, keep radius sensible, etc.
- **Why:** Elements don't read well when every dimension scales by the same factor; fine-tuning per property fits each context.

### B7. Make accessible beautiful

- **Spot it:** Light text on saturated background (low contrast); meaning conveyed by color alone; status states distinguished only by hue.
- **Fix:** When contrast is failing, **flip it** — dark text on a light tint of the same hue instead of light text on a saturated fill. To lift a too-dark color into contrast range, **rotate its hue** toward a brighter one (and bump saturation) rather than just lightening it to grey. Pair color with **icons/shape** so it's not the only signal, and differentiate states with **contrast** rather than entirely different colors. Target WCAG AA (4.5:1 body, 3:1 large text).
- **Why:** Accessible choices (sufficient contrast, non-color cues) and attractive design are the same choices — high-contrast, icon-supported UI looks more polished, not less. See also [F4](#f4-keep-saturation-when-you-change-lightness) and [F6](#f6-dont-use-grey-text-on-colored-backgrounds).

### B8. Supercharge the defaults

- **Spot it:** Raw browser defaults left in place — disc bullets, plain blockquotes, default checkboxes/radios, default link styling.
- **Fix:** Replace default list bullets with custom markers/icons, style quotes, design custom selection controls, give links intentional treatment.
- **Why:** Default elements are an instant "unfinished" tell; small upgrades to them lift the whole page's perceived quality cheaply.

### B9. Separate visual hierarchy from document hierarchy

- **Spot it:** Headings sized purely by their semantic level — an `<h2>` section label rendered large and bold just because the markup says so.
- **Fix:** Choose markup for **semantics** and styling for **visual hierarchy** independently. Many semantic headings act as labels and should be styled small (sometimes even visually hidden); size each element by the attention it deserves, not its tag.
- **Why:** Letting document structure dictate visual size produces over-loud section titles and a flat, default-looking hierarchy.

---

## C. Don't

### C1. Avoid labels when possible

- **Spot it:** Every value carries a redundant label ("Phone: 555-1234", "Email: x@y.com") where format already signals meaning.
- **Fix:** Drop the label when the format is self-evident; fold clarifying words into the value ("$19/mo", "12 photos"); when a label is needed, **de-emphasize** it (smaller, lighter, lower contrast). **Exception:** information-dense spec pages where users scan for the label word ("depth", "weight").
- **Why:** Labels add noise. Removing or quieting them lets the actual data carry the hierarchy.

### C2. Avoid ambiguous spacing

- **Spot it:** A heading sits equidistant between the section it closes and the one it opens; list items spaced the same as the gap between groups; an icon floats between two labels; a field label equally close to the field above and below.
- **Fix:** Tie related elements together with **less** space and push unrelated ones apart with **more**. A heading belongs closer to the content it introduces; a label belongs closer to its own field.
- **Why:** Proximity communicates grouping. Ambiguous gaps make users guess what belongs to what.

### C3. Avoid too many borders

- **Spot it:** Boxes inside boxes, every element ringed with 1px lines, dividers everywhere — busy and boxy.
- **Fix:** Separate with **shadow, background color, or extra spacing** instead of borders. Reserve borders for where nothing else reads clearly.
- **Why:** Borders add visual weight and clutter fast; softer separators achieve the same grouping with less noise.

### C4. Avoid too long lines

- **Spot it:** Paragraph text running the full page width — well over ~75 characters per line.
- **Fix:** Constrain measure to **45–75 characters per line** (~`max-width: 65ch`). Limit paragraph width even when mixed with wide images/components.
- **Why:** Long lines make the eye lose its place returning to the next line; the 45–75 band is the readable sweet spot.

### C5. Don't fill the whole screen

- **Spot it:** Content stretched to every edge, elements made wide just because the viewport is wide, full-bleed everything.
- **Fix:** Constrain content to a comfortable max-width with margin around the edges; don't force a block full-width just because the nav is. Spreading things out hurts interpretation.
- **Why:** Unnecessary width makes scanning harder; a little edge space costs nothing and reads as composed.

### C6. Don't center long-form text

- **Spot it:** Multi-line paragraphs set center-aligned, creating ragged left edges the eye must re-find each line.
- **Fix:** Left-align body copy. Reserve centering for short runs (1–3 lines: headings, captions, CTAs).
- **Why:** A consistent left edge anchors the return sweep; centered prose forces the eye to hunt for each line's start.

### C7. Don't scale icons / screenshots

- **Spot it:** A small icon blown up large (blurry, thin, lost detail) or a full screenshot shrunk to fit (illegible).
- **Fix:** Use icons **drawn for the target size**, or enclose a small icon in a shape/badge instead of enlarging it. For screenshots, show a **cropped detail**, a **simplified illustration**, or a **smaller device frame** rather than scaling the whole thing down.
- **Why:** Scaling breaks the optical weight an asset was designed for — enlarged icons look flimsy, shrunk screenshots become noise.

---

## D. Tips & tricks

These are upgrades to reach for once the fundamentals (A–C) are sound.

### D1. Combine two shadows

- Layer a tight, dark shadow with a larger, softer one to model realistic depth instead of a single flat blur.

### D2. Add color with accent borders

- A short colored border (top of a card, left of an alert, under a headline, edge of a layout, side of an active menu item) injects brand color and signals state cheaply.

### D3. Overlap elements to create layers

- Overlap components (card over image, avatar over header, element spanning two sections) to add depth. Give overlapping images an "invisible border" (matching-color outline) so edges don't clash.

### D4. Make text stand out on an image background

- When text sits on a photo, match the treatment to the text: add a **black overlay** behind light text (or a **white overlay** behind dark text), **lower the image's contrast** while compensating brightness, **colorize** it (desaturate + multiply with a brand color), or add a soft **text shadow** — so text stays legible without a solid box.

### D5. Decorate your backgrounds

- Lift flat sections with a subtle background **color** change to distinguish them, a **gradient**, an **illustration**, or a **repeating pattern** (e.g. heropatterns.com).

### D6. Look for fresh ideas / decisions you wouldn't have made

- Borrow unexpected choices from polished products (dark datepicker, button nested inside an input, two-color headline). The best way to learn the details is to **recreate a great design from scratch** without peeking at devtools.

---

## E. Beware

### E1. Beware user-uploaded content

- **Spot it:** Layout assumes ideal images/text — avatars of varying aspect ratios, long names, light images bleeding into a white background.
- **Fix:** Constrain user images to **fixed containers** and center-crop overflow. Prevent background bleed with a subtle **inner shadow or semi-transparent inner border**. _(Beyond the book: plan for long/short user strings too — truncate, wrap, min/max widths.)_
- **Why:** Real user content is messy; designs that only work with perfect placeholder data break in production.

### E2. Beware empty states

- **Spot it:** First-run screens that are blank, or show tabs/filters/controls that do nothing because there's no data yet.
- **Fix:** Treat the empty state as a priority: lead with a clear **add/create CTA** and guidance. **Hide** tabs, filters, and secondary controls until content exists.
- **Why:** The empty state is often a user's first impression; a blank or cluttered-but-inert screen is confusing exactly when guidance matters most.

---

## F. Color

The summary repo barely touched color; this is where most "almost-good" UIs fall down.

### F1. Define color in HSL, not hex

- **Spot it:** Palette stored as opaque hex codes; lightening/darkening is guesswork.
- **Fix:** Author colors in **HSL** (hue / saturation / lightness). Tweak lightness and saturation as independent dials instead of nudging six hex digits.
- **Why:** HSL maps to how the eye reasons about color, so building shade ramps and adjusting contrast becomes predictable rather than trial-and-error.

### F2. You need more colors than you think

- **Spot it:** One "primary", one grey, maybe a red — then the design can't express disabled, hover, subtle backgrounds, borders, or multiple statuses.
- **Fix:** Build real palettes up front: **~8–10 shades per hue** (dark → light), a full **grey ramp** (often 8–10 steps), and **accent hues** for states (success/warning/error/info). A few base hues each expanded into a ramp.
- **Why:** Polished UIs lean on many close shades for borders, fills, hovers, and text levels; too few colors forces flat, undifferentiated surfaces.

### F3. Define your shades up front

- **Spot it:** Shades invented ad hoc with `darken()`/`lighten()` at call sites, producing muddy or inconsistent variants.
- **Fix:** Pick the **base** (mid) shade first, find the **darkest** and **lightest** edges, then fill the gaps to a fixed scale (e.g. 100–900). Choose from that fixed set thereafter.
- **Why:** A predefined ramp keeps every surface on-system and removes per-component color decisions — the color version of [A2](#a2-systematize-everything).

### F4. Keep saturation when you change lightness

- **Spot it:** Dark or light shades that look washed-out and grey because only lightness was changed.
- **Fix:** As a color gets **darker or lighter, increase its saturation** so it stays vivid. To make a color feel brighter/darker, also **rotate the hue** in small steps (no more than ~20–30°): toward the nearest **bright** hue — 60° yellow, 180° cyan, 300° magenta — to brighten, or toward the nearest **dark** hue — 0° red, 120° green, 240° blue — to darken, rather than only moving lightness.
- **Why:** Perceived brightness depends on hue, not just lightness; pure lightness changes drain saturation and produce lifeless ramps.

### F5. Greys don't have to be grey

- **Spot it:** Pure neutral `#888`-style greys that feel cold/clinical and clash with the brand.
- **Fix:** Give greys a **temperature** — a touch of blue for cool/professional, a touch of yellow/orange for warm/friendly — consistently across the grey ramp.
- **Why:** Tinted greys reinforce the chosen personality ([A1](#a1-choose-a-personality)); dead-neutral greys make an interface feel generic.

### F6. Don't use grey text on colored backgrounds

- **Spot it:** Grey (or white-at-low-opacity that goes muddy) secondary text sitting on a colored panel/button, looking dull and dirty.
- **Fix:** Pick a secondary color **based on the background hue** — same hue, adjusted saturation and lightness — instead of grey. (Reducing opacity works only over solid colors, not images.)
- **Why:** Grey only de-emphasizes against white; on a colored field it muddies. A hue-matched shade reads as intentional and stays legible. Pairs with [B1](#b1-use-a-visual-hierarchy)'s de-emphasis.

## G. Depth & light

### G1. Emulate a single, consistent light source

- **Spot it:** Shadows/highlights point in conflicting directions; inset and raised elements look the same; the UI feels flat or "off".
- **Fix:** Assume light from **directly above**. **Raised** elements get a slightly lighter top edge and a shadow **below**; **inset** elements (wells, pressed buttons, inputs) get a subtle **inner shadow at the top**. Keep the direction consistent everywhere.
- **Why:** The eye reads depth from a shared light source; consistency is what makes buttons look pressable and cards look lifted instead of pasted on.

### G2. Use shadows to convey elevation

- **Spot it:** Every shadow is the same, so a dropdown, a card, and a modal all sit at the same apparent height.
- **Fix:** Define an **elevation scale** (sm/md/lg/xl): closer-to-surface = small tight shadow, higher = larger softer shadow. Map components to elevations (button < card < dropdown < modal) and reuse them.
- **Why:** Larger, softer shadows read as "further off the page", giving a coherent z-axis that signals interactivity and layering.

### G3. Depth without shadows

- **Spot it:** A deliberately flat design that now reads as flat _and_ lifeless.
- **Fix:** Create depth with **color and contrast** instead of blur — a lighter top band vs. a darker base, or **solid offset shadows** (a hard, blur-less shadow in a darker shade of the element). Combine a tight dark shadow with a larger soft one for realism (see [D1](#d1-combine-two-shadows)).
- **Why:** Flat aesthetics can still express hierarchy and elevation; they just shift the work from blur to color and offset.

## H. Type selection & setting

### H1. Choose a good typeface

- **Spot it:** Default system font left unconsidered, or a quirky display font used for body text; a font with only one or two weights.
- **Fix:** Play it safe with a well-crafted **neutral sans-serif** unless the personality calls for more. Require **≥5 weights** so hierarchy has room. Optimize for **legibility at UI sizes** (taller x-height, open apertures). When unsure, borrow a typeface from a product whose design you admire.
- **Why:** Type is most of an interface's surface area; a quality, multi-weight, legible face does more for "looks designed" than almost any other single choice. Supports [A1](#a1-choose-a-personality).

### H2. Build a non-linear type scale

- **Spot it:** Font sizes picked ad hoc (15/17/22/29…), or a strict linear scale that yields too few small sizes and too many huge ones.
- **Fix:** Hand-pick a **fixed set of sizes** (e.g. 12/14/16/18/20/24/30/36/48/60/72) and only use those. Prefer **px/rem over em** so nested sizes don't compound unpredictably.
- **Why:** A curated, non-linear scale gives the right granularity where text actually lives (small/medium) and keeps headings deliberate — the type half of [A2](#a2-systematize-everything).

### H3. Align mixed-size text to the baseline

- **Spot it:** A large number beside small label text, vertically center-aligned, looking subtly misaligned.
- **Fix:** When different font sizes share a line (price + unit, metric + label), align them to the **baseline**, not the vertical center.
- **Why:** The baseline is the line the eye reads along; center-aligning mixed sizes makes the smaller text float.

### H4. Number & paragraph polish

- **Spot it:** Right-hand columns of numbers misaligned; justified body text with rivers of whitespace.
- **Fix:** **Right-align numbers** so digits line up by place value _(and, beyond the book, enable tabular/lining figures)_. Avoid justified text; if required, **enable hyphenation**.
- **Why:** Aligned digits are scannable and comparable; unhyphenated justification creates ugly gaps that hurt reading.

## I. Process

These govern _how_ a design gets made — relevant when reviewing a spec or a work-in-progress, not just a finished screen.

### I1. Start with a feature, not a layout

- **Spot it:** A spec/design that begins with nav, logo placement, and page chrome before any real functionality is designed.
- **Fix:** Design a concrete **feature** first (the actual job the screen does); let the navigation and shell emerge once there's something to navigate.
- **Why:** Chrome-first designs optimize the frame around an empty picture; feature-first keeps effort on what users came to do.

### I2. Work in low fidelity first

- **Spot it:** Color, gradients, and pixel-tweaking applied before spacing, hierarchy, and layout are settled.
- **Fix:** Rough it out in **grayscale** and with simple spacing first; add color and detail only once structure and hierarchy hold up. Define hierarchy with spacing, size, and contrast before introducing hue.
- **Why:** Committing to detail early anchors you to weak structure; low-fidelity-first keeps the big decisions cheap to change.

### I3. Don't design too much

- **Spot it:** A spec/mockup that tries to resolve every feature, interaction, and edge case in the abstract, or that shows UI implying functionality the team isn't ready to build.
- **Fix:** Work in **short cycles** — design and build the smallest useful version of a feature, then iterate as real needs surface. **Be a pessimist:** don't add buttons, links, or states that imply functionality you can't yet deliver. (For the non-ideal states a real screen still needs — empty, error, loading — see [E2](#e2-beware-empty-states).)
- **Why:** Designing too much up front burns effort on decisions that change once real content and constraints arrive, and implied-but-unbuilt features set expectations you'll have to break.

## J. Imagery

### J1. Use good photos

- **Spot it:** Cheap/amateur stock photography, inconsistent styling, or low-resolution images undermining an otherwise clean layout.
- **Fix:** Use **high-quality, consistently styled** photography (consistent lighting, color treatment, subject); crop and treat images uniformly. Hire a professional or use high-quality stock rather than placeholder images you'll later swap for weak phone shots. _(Beyond the book: when photography isn't available at all, prefer illustration or a solid/gradient treatment over weak stock.)_
- **Why:** One bad image drags down the perceived quality of everything around it; imagery is judged instantly.

---

## Severity guidance

Rank each finding so the report leads with what matters:

- **High** — hurts usability, readability, or accessibility, or makes the product look broken/unfinished: no visual hierarchy (B1), unreadable contrast (B5/B7), color-only meaning (B7), grey text on colored backgrounds (F6), line length far outside 45–75 (C4), ambiguous spacing that misleads grouping (C2), broken empty/user-content states (E1/E2), unreadable text over an image (D4).
- **Medium** — clearly looks worse but still usable: cramped spacing (A3), too many borders (C3), full-bleed layout (C5), centered long text (C6), scaled icons/screenshots (C7), unsystematized values (A2), thin/washed-out color ramps (F2/F3/F4), inconsistent light/elevation (G1/G2), poor or single-weight typeface (H1), raw defaults (B8), low-quality imagery (J1).
- **Low / polish** — refinements that elevate an already-sound design: letter-spacing (B3), grey temperature (F5), combined shadows (D1), depth-without-shadows (G3), baseline alignment (H3), number/justify polish (H4), accent borders (D2), overlap/layering (D3), background decoration (D5), fresh-idea borrowing (D6).

Always pair each finding with the **principle ID** (e.g. `B1`), the **specific element/location**, the **concrete fix**, and the **why**.
