# Landing page — design plan

Single self-contained page at `docs/` (GitHub Pages serves it at `viesloxy.github.io/ui-slicing/`). The page must practice what the skill preaches: measured tokens, one orchestrated motion moment, no slop. The memorable thing: **the page is a measuring instrument** — crosshair cursor, px readouts, crop brackets, section bands.

## Reference DNA (from D:/Skills/web-design-inspiration)

| Source | What we take |
|---|---|
| `04-Clone-Award-Winning/awwwards-zentry-clone` | palette trio: blue-tinted off-white `#DFDFF0`, violet `#5542FF`, acid lime `#EDFF67`; oversized condensed display caps |
| `04-Clone-Award-Winning/dennis-snellenberg-portfolio` | disciplined spacing rhythm, hairline rules, quiet footer colophon |
| `03-Situs-Legendaris/portfolio-2025` (davidhckh) | preloader-free instant load, mono micro-labels, dev-tool restraint |

Explicitly rejected (AI-slop clusters): purple→blue gradients, acid-green-on-black single-accent, centered-everything hero, 3-card icon grids, Inter everywhere, numbered eyebrows on non-sequences.

## Tokens

```
--ink:      #0F1014   (blue-tinted near-black; never #000)
--paper:    #E7E8EF   (blue-tinted off-white from Zentry DNA)
--paper-2:  #F2F2F7   (raised surface)
--violet:   #5542FF   (accent — links, CTAs, active marks; ≤5% of any viewport)
--lime:     #EDFF67   (measurement highlight ONLY — readouts, ticks; ≤2% of any viewport)
--rule:     rgba ink/paper 12–18% hairlines
display:    'Anton' (condensed poster caps)
body:       'Archivo' (400/500/700)
mono:       'JetBrains Mono' (px labels, code, coordinates)
spacing:    8px base grid; container 1200px; gutters 24/32
radius:     0 default (instrument edges), 2px on interactive only
```

## Layout (in order)

1. **Topbar** — wordmark `ui‑slicing`, right: version tag + GitHub link. Hairline bottom.
2. **Hero (dark)** — giant Anton caps: `SLICE ANY UI.` (filled) / `SHIP THE CODE.` (outlined stroke). Left-biased. Crosshair follows cursor with live px-coordinate readout (lime, mono). Crop brackets frame the headline. CTAs: `Get the skill` (violet solid) + `Star on GitHub` (hairline). Meta row: mono stats (6 steps · 3 scripts · 14 topics).
3. **Ticker** — mono marquee: `FETCH → ANALYZE → SLICE → TOKENS → BUILD → COMPARE →` pauses on hover.
4. **Problem (paper)** — "Generated UI fails two ways." Two spec rows (not cards): 01 Generic defaults / 02 Lazy approximation, each with tell-list in mono. Hairline separated.
5. **Workflow (paper)** — the real sequence 01–06: ACQUIRE/ANALYZE/TOKENS/BUILD/VERIFY/DELIVER. Left rail: huge numerals; right: step name + 2-line description + mono command where real. Sticky left title.
6. **Demo (dark)** — "See the slice." Left: inline-SVG mock reference (mini dashboard) framed by crop brackets with annotated px measurements (lime). Right: the matching rebuilt code (mono, syntax-tinted). Caption: measured, not guessed.
7. **Anti-slop (paper)** — "Slop is inventing. Not matching." Gates as checklist rows with violet tick marks; callout: **the reference wins**.
8. **Install (dark)** — per-platform rows: pi / Claude Code / Codex / Gemini & ChatGPT, mono install commands, copy button.
9. **Footer (dark)** — single-line colophon: `ui-slicing — MIT — distilled from v0 · Hallmark · Anthropic skills` + back-to-top. No link columns.

## Motion (one orchestrated moment, action-honest)

- Load: hero lines reveal once (clip-path, 600ms, stagger 80ms). Nothing else animates on load.
- Cursor crosshair + px readout in hero only; `pointer: fine` only; disabled with reduced-motion.
- Ticker marquee: CSS animation, pauses on hover/focus.
- Scroll reveals: none. Hover states: instant color/border shifts.
- All motion killed under `prefers-reduced-motion`.

## Quality floor

Responsive 320–1920 no h-scroll; focus-visible rings (violet, instant); contrast ≥4.5:1 body / ≥3:1 large; semantic landmarks; OG meta tags; favicon inline SVG data-URI.
