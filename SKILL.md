---
name: ui-slicing
description: Replicate UI pixel-faithfully from a reference image (Pinterest pin, Dribbble shot, screenshot, or any URL). Analyzes the image, extracts design tokens (colors, fonts, spacing, radii), slices it into section crops for close inspection, builds the front-end section by section, then verifies the result against the reference. Use when given a UI screenshot or design image to recreate as HTML/CSS or React code.
---

# UI Slicing — pixel-faithful rebuild from a reference image

Recreate the reference, not a "similar design". Fidelity is the product. Two failure modes kill output quality: (1) **generic AI defaults** — building what such a design *usually* looks like instead of what THIS image shows; (2) **lazy approximation** — right structure, wrong numbers. Both are slop.

## Workflow — follow in order, never skip analysis

### 0. Acquire the reference

- Local image path → use it directly.
- URL (`pinterest.com/pin/...`, `dribbble.com/shots/...`, any blog/portfolio page) → `python scripts/fetch_reference.py <url>`. It saves the image and prints the path + dimensions.
- If a site blocks scripted fetching, ask the user to save the image manually, then continue with the file.
- Long full-page screenshots are ideal — they slice cleanly.

### 1. Analyze before writing ANY code

```bash
python scripts/slice_reference.py reference.png --outdir slices --bands
```

Prints JSON: dimensions, likely DPR, dominant palette (hex + coverage %), and detected section boundaries (y-ranges). Each section is saved as a zoomed crop in `slices/`.

Then **read the original image AND every band crop**. Crops exist because full-page views lose detail; each crop shows nav, cards, forms at readable resolution. Zoom into anything ambiguous:

```bash
python scripts/slice_reference.py reference.png --crop 120,640,380,400 --out slices/card1.png --zoom 3
```

Record per section, before code:
- Background colors; any gradient (direction, stop colors — crop the gradient area and sample left/mid/right)
- Content max-width (distance from viewport edge), column count, gaps
- Text hierarchy: cap-height in px ≈ 0.70 × font-size; count distinct weights; note serif/sans/mono per role
- Spacing rhythm: measure paddings/gaps, find the common unit (usually 4 or 8 px), note off-scale exact values
- Radii, border widths, shadows (direction/softness), icon style (outline vs filled, stroke weight), image treatments (aspect, radius, overlay)

Assume image width = design width (1440/1920 desktop, 375/390 mobile) unless it's a 2× retina export — `likely_dpr` flags this; divide by 2 when so. See [references/analysis-protocol.md](references/analysis-protocol.md) for the full measuring technique and font identification.

### 2. Lock tokens first

Write `tokens.css` (or the theme config) before any component. Colors: exact hex from the analysis — do not "clean up" or "harmonize" them. Fonts: identify the reference typefaces and load the closest embeddable match (Google Fonts). Spacing: a named scale built from the measured unit. Every color and font-family in component code must reference a token — no inline improvisation mid-build.

### 3. Plan sections

List slices top → bottom with purpose + a one-line ASCII wireframe each, and which measurements drive them. Ambiguous areas (blurry text, cut-off content): choose the most plausible completion, mark it `<!-- ASSUMED: ... -->`, and tell the user at delivery.

### 4. Build section by section

- One section at a time; compare each against its band crop immediately, not at the end.
- Reproduce real text from the reference (read it from crops). Lorem only when genuinely unreadable — then mark it.
- Photos/illustrations can't be extracted: use placeholders with the exact aspect ratio, radius, and treatment; mark `<!-- TODO: asset -->`.
- A static reference still ships with states: hover, focus-visible, active, disabled, and `prefers-reduced-motion` support.
- Stack per user request: plain HTML+CSS is the default; React+Tailwind on request. When measured values miss the Tailwind scale, use arbitrary values (`p-[17px]`) — fidelity beats scale purity.
- Responsive: the reference shows one breakpoint. Extend sensibly (collapse columns, stack nav) instead of inventing a new design.

### 5. Verify against the reference

If a screenshot path exists (Playwright/Puppeteer/browser tooling available):

```bash
python scripts/compare_screens.py reference.png output.png --outdir compare
```

Read `compare/side.png` and `compare/diff.png`, fix the highest-diff bands first, re-screenshot, repeat until structure, spacing, and colors match. Without screenshots: deliver and ask the user to compare; iterate on their notes.

Final gate: run every check in [references/anti-slop-checklist.md](references/anti-slop-checklist.md).

### 6. Deliver

Ship code + tokens file + `slices/`. Report deviations and assumptions explicitly — never silently.

## Fidelity rules (the core)

1. **The reference wins.** If it uses three equal cards, purple, Inter, a centered hero — match it exactly. Those choices are only "slop" when the AI invents them; here they are the design. Never silently "improve" the reference.
2. **Measure, don't guess.** Every number — color, size, gap, radius — comes from the image or a crop, never from what such designs usually use.
3. **Never inject defaults.** No swapping fonts to favorites, no adding gradients/emoji/shadows/animations absent from the reference, no normalizing odd measured values to a convenient scale.
4. **No invented content.** Metrics, testimonials, and logos visible in the reference are reproduced as-is; unreadable text gets a neutral placeholder marked ASSUMED. Inventing "+47% conversion" is slop.
5. **Detail parity.** Input states, focus rings, transitions, empty states weigh as much as the hero — most rebuilt UIs die in the details, not the headline.

Deep-dive docs: [references/analysis-protocol.md](references/analysis-protocol.md) (measurement + font identification) · [references/anti-slop-checklist.md](references/anti-slop-checklist.md) (pre-delivery gates).
