# Analysis protocol — measuring a reference image

Numbers come from pixels, not habit. Work through this protocol after slicing; keep notes per section.

## 1. Scale & DPR

- Detect retina exports: nav bars, buttons, or body text that measure 2× plausible physical sizes (e.g., a 32 px-looking body text on a 2880 px-wide image) → the export is 2×. Divide all measurements by the DPR.
- After correction, sanity-anchors: body text 14–18 px, nav height 56–80 px, button height 36–48 px, desktop content max-width 1100–1320 px, mobile width 375–430 px.
- Design width assumption: if the image is cropped or unknown, state the assumption in the delivery notes.

## 2. Measuring technique

Crop tight regions and zoom (`--crop x,y,w,h --zoom 3`), then count pixels between visible edges. Measure:

| What | How |
|---|---|
| Font size | cap-height px ÷ 0.70 (sans) or ÷ 0.66 (many serifs). x-height ≈ 0.52 × font-size (sans). |
| Line-height | baseline-to-baseline distance in px ÷ font-size → unitless ratio (typically 1.2–1.6) |
| Letter-spacing | Visually classify: normal / slightly tight (−1 to −2%) / tight display (−2 to −4%) / wide uppercase label (+8 to +12%) |
| Paddings & gaps | Distance between element edges at 1× scale. Round to the nearest even number; exact values that repeat stay exact |
| Radius | Height of the corner curve in px (0, 2, 4, 6, 8, 12, 16, 24, or pill are the common real values) |
| Border | 1 px hairline vs 2 px. Color: sample it |
| Shadow | Look at the halo under cards: direction (y-offset), spread, darkness. If invisible, no shadow |
| Grid | Content left inset, column count, gutter width, and whether columns are equal |
| Gradient | Crop it, sample 3+ hex stops along the axis, note direction (to bottom-right, radial from corner, etc.) |

The palette from `slice_reference.py` gives exact hex + coverage %. Coverage tells you which color is background (largest %) vs ink vs accent (smallest, saturated).

## 3. Typography — identify, then substitute

Identify the real typeface by letterform features, reading from a zoomed crop:

- Serif or sans? Mono?
- Single-story vs double-story `a` and `g` (geometric sans have single-story `a`: Futura, Century Gothic)
- Terminal shapes: straight-cut (Inter, Roboto), angled (SF Pro), rounded (Nunito, Quicksand)
- Contrast: high thin-thick contrast = Didone/serif display (Playfair territory); even = grotesque
- Width: condensed / normal / wide
- Distinctive letters: `G` with spur? `R` with straight or curved leg? `t` with slanted top?

Common UI fonts to check first: Inter, SF Pro, Roboto, Open Sans, Lato, Montserrat, Poppins, DM Sans, Work Sans, Manrope, Plus Jakarta Sans, Sora, Space Grotesk, Archivo, IBM Plex Sans, Source Sans.

Substitution table (reference font → embeddable Google Font). Put the real name first in the stack so licensed installs use it:

| Reference face | Closest Google Font |
|---|---|
| SF Pro / -apple-system | `system-ui` stack, fallback `Inter` |
| Helvetica Neue | `Inter` |
| Proxima Nova | `Montserrat` |
| Gotham | `Montserrat` |
| Circular Std | `DM Sans` (alt: `Figtree`) |
| GT Walsheim | `Figtree` |
| Avenir / Avenir Next | `Nunito Sans` |
| Futura | `Jost` |
| DIN | `Barlow` (alt: `Archivo`) |
| Gilroy | `Poppins` (alt: `Raleway`) |
| Söhne / Basier | `Inter` |
| Neue Haas Grotesk | `Inter` (alt: `Archivo`) |
| Founders Grotesk | `Work Sans` |
| Didot / Didone display | `Playfair Display` |
| Baskerville | `Libre Baskerville` |
| Tiempos / Canela / modern text serif | `Source Serif 4` (alt: `Fraunces`) |
| Garamond / old-style serif | `EB Garamond` |
| Slab (Roboto Slab, Archer) | `Roboto Slab` |
| SF Mono / Menlo / code | `JetBrains Mono` (alt: `IBM Plex Mono`) |
| Condensed (Oswald, DIN Cond.) | `Oswald` (alt: `Barlow Condensed`) |

Rules: max 2 families + optional mono; load with correct weights only (the weights measured in step 2); never silently replace a distinctive display face with Inter.

## 4. Icon & image treatment

- Icon style: outline (stroke 1.5–2 px on a 24 px grid), filled, duotone, or 3D. Pick ONE library matching the style (Lucide/Feather = outline, Phosphor = both, Heroicons = outline+solid).
- Photo treatment: radius, border, duotone/overlay, aspect ratio (measure!), object position, grayscale or not.

## 5. Section inventory

After `--bands`, write the inventory table used for building:

```
band00 y0-58    nav       dark #141826, logo left, 4 links right, height 64px (DPR÷2)
band03 y159-231 headline  56px/1.1, weight 700, 2 lines, max-width 640px
band05 y274-317 CTA       bg #C85A28, radius 8, height 48, padding-x 32
...
```

Every band must map to a section in code; every section must trace back to a band.
