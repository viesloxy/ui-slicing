# Anti-slop checklist — run before delivery

Two rules order everything below:

1. **Fidelity first.** If the reference itself uses something on the "tell" list, matching it is correct — those items are only tells when *invented*. Mark nothing, fix nothing, explain nothing: just replicate.
2. **Never inject.** Anything not visible in the reference does not enter the build. When in doubt, leave it out.

## A. Fidelity gates (compare output vs reference bands)

- [ ] Every section from the analysis exists, in order, nothing silently dropped
- [ ] Colors match the extracted palette (backgrounds exact; accents within a hair of the sampled hex)
- [ ] Gradients match direction + stops sampled from the image
- [ ] Fonts match identified faces (or closest substitutes from the table); weights and sizes within ~1 px of measured
- [ ] Spacing within ~5% of measured values; off-scale exact values preserved, not rounded to a convenient scale
- [ ] Radii, borders, shadows, icon style, image treatments match
- [ ] All readable text reproduced verbatim; unreadable text marked ASSUMED; no invented metrics/testimonials/logos
- [ ] Placeholder assets carry the exact aspect ratio, radius, and treatment of the originals

## B. Injection tells — must NOT appear unless the reference shows them

- Swapping the reference font for Inter/Roboto/system defaults
- Purple→blue (or cyan→magenta) gradients; `background-clip: text` gradient headlines
- Emoji used as feature/step/pricing icons; two icon libraries mixed on one page
- Aurora/mesh blobs or floating orbs added "for depth"
- Bounce/elastic easing; `transition: all`; uniform `hover:scale-105` on unrelated elements; focus rings that fade in
- Italic words inside upright headlines; ALL-CAPS eyebrow labels above every section; meta strings joined with middle dots (`A · B · C`); `→` appended to every link
- Card nested in card; thick colored side-stripe borders on cards
- Fabricated browser/phone chrome around screenshots; `loading="lazy"` on the hero/LCP image; autoplaying video without `muted playsinline`
- Invented stats ("+47% conversion", "trusted by 50,000+ teams"), fake testimonials, placeholder brand names (Acme, Nexus, Jane Doe)
- "Improving" the reference layout, copy, or palette without being asked

## C. Quality floor (applies even though the reference is static)

- [ ] No horizontal scroll at any width 320–1920 px (`overflow-x: clip` on html+body; `minmax(0,1fr)` for image grid tracks; `overflow-wrap: anywhere` on display headings)
- [ ] All four responsive sanity widths render correctly (320 / 375 / 768 / 1280)
- [ ] Every interactive element has default + hover + focus-visible + active + disabled states
- [ ] Input fields: `border-width` never changes between states (use color/outline); focus ring via `outline` + `outline-offset`; input height = adjacent button height; helper-text slot reserves `min-height: 1lh`; disabled = opacity + `cursor: not-allowed` + attribute, never opacity alone
- [ ] Contrast: body text ≥ 4.5:1, large text/icons/focus rings ≥ 3:1 — check text-on-new-background pairs (card text on swapped surface is the classic miss)
- [ ] Every animation/keyframe has a `prefers-reduced-motion` fallback; focus indicators appear instantly
- [ ] Prose lines 45–75 characters; `text-wrap: balance` on headings; body line-height 1.4–1.6
- [ ] Semantic tokens: no raw hex/rgb inline in components; everything references the tokens file

## D. Pre-delivery self-critique (score 1–5, revise anything below 3)

| Axis | Question |
|---|---|
| Fidelity | Side-by-side: does this look like the image, or like a cousin of it? |
| Hierarchy | Is primary/secondary/tertiary as readable as in the reference? |
| Execution | Rule weights, alignment, text-wrap, focus rings, contrast — all in spec? |
| Specificity | Does it look like THIS design, or any design? |
| Restraint | Nothing added beyond the reference? Nothing "helpfully" decorated? |
| Detail parity | Do the small parts (inputs, footers, captions) match as hard as the hero? |

Derived and distilled from: Anthropic `frontend-design` & `web-artifacts-builder` skills; Hallmark anti-slop skill (Nutlope); v0, Bolt, and Same.dev production system prompts; Refactoring UI.
