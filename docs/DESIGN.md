# Landing page — design plan v2 (full redesign)

V1 rejected: dark canvas + acid-lime accent + condensed poster caps = the Claude/Anthropic cluster (their own tell-list, gate 2). V2 pivots completely: **light studio/agency build**, normal-case grotesque + serif italic accents, one vivid orange accent, GSAP-driven motion. DNA sources switch from Zentry to the Awwwards-clone shelf.

## Reference DNA (from D:/Skills/web-design-inspiration)

| Source | What we take |
|---|---|
| `04-Clone-Award-Winning/dennis-snellenberg-portfolio` (PP Neue Montreal) | light editorial surface, one-family grotesque at display sizes with tight tracking, pill buttons with invert hover + arrow nudge, rotating circular badge, quiet top bar |
| `04-Clone-Award-Winning/Obys-Clone-Gsap` | off-white + black + **signal orange `#FF4D00`** accent, GSAP text reveals, scroll choreography |
| `04-Clone-Award-Winning/k72-website` | big statement typography, section rhythm via rules and whitespace only |

Rejected tells (from our own checklist): cream+terracotta (Claude), dark+acid-lime (Claude cluster 2), Inter default, purple gradients, condensed all-caps posters, numbered eyebrows on non-sequences.

## Tokens

```
--bg:        #F0EFEB   bone (neutral, not warm-cream; paired with vivid orange = agency, not Claude)
--bg-2:      #E6E5DF   bone pressed (rows, code panels)
--ink:       #141311   neutral near-black (never #000)
--ink-60:    rgba(20,19,17,.60)
--rule:      rgba(20,19,17,.14)
--orange:    #FF4D00   signal accent (Obys) — CTAs, ticks, marquee, progress bar; ≤5% viewport
--paper-inv: #F0EFEB   text on dark sections
--dark:      #141311   dark section canvas
display+body:'Instrument Sans' (400/500/600) — one family, tight tracking at display sizes
serif accent:'Instrument Serif' italic — single emphasized words in headlines
mono:        'JetBrains Mono' — labels, commands, coordinates (400/700)
radius:      pills (999px) on buttons/badges; 0 on structural elements
grid:        container 1200px, 12-col feel via splits; gutters 24/32; section pad 128px
```

## Layout (in order)

1. **Topbar** — wordmark left, right: `GitHub ★` text link + `Get the skill` orange pill. Hairline bottom. Scroll progress hairline (orange) at very top.
2. **Hero (bone)** — kicker mono; headline 3 lines, line-masked GSAP reveal: `Turn any screenshot` / `into *pixel-perfect*` (serif italic orange word) / `front-end code.` Right column bottom-aligned: sub-copy + pill CTAs (`Get the skill ↓` orange, `Star on GitHub` outline). Bottom hairline meta row: 6-step workflow · 3 scripts · 58 gates · 1-file output. Rotating circular badge (SVG textPath, `SCROLL · EXPLORE · MEASURE ·`) pinned at hero right edge.
3. **Marquee (orange bg, ink text)** — `FETCH → ANALYZE → SLICE → TOKENS → BUILD → COMPARE → DELIVER`, CSS loop, hover pause.
4. **Problem (bone)** — editorial split rows: giant grotesque numerals 01/02 in outline, name + tell-list mono with orange keyword highlights. Closing statement with orange-highlighted rules.
5. **Workflow (dark, PINNED horizontal scroll — desktop GSAP scrub)** — six panels slide horizontally while pinned; each panel: huge index numeral, step name, 2-line description, mono command where real. Mobile/reduced-motion: plain vertical stack.
6. **Demo (bone)** — split: annotated SVG mock (crop brackets, lime→orange measurement tags) vs rebuilt token code panel (bone-2, mono). Figure gets scrub parallax (yPercent). Caption mono.
7. **Anti-slop (bone)** — two-col compact gates with orange ticks; then full-width statement set in huge serif italic: `The reference wins.` + supporting paragraph.
8. **Install (dark)** — 4 rows (pi / Claude Code / Codex / Gemini·ChatGPT) with pill copy buttons; row hover lifts background.
9. **Footer (dark)** — giant bottom-aligned wordmark `ui-slicing` (outlined), colophon row, license + links.

## Motion inventory (GSAP 3 + ScrollTrigger via cdnjs — the "gacor" set)

- Scroll progress hairline (orange) — scrub
- Hero: line-mask stagger reveal on load (600ms, 80ms stagger, expo.out)
- Section titles: yPercent clip reveal on enter, once
- Workflow: pinned horizontal translate scrub (desktop, `min-width: 960px`, pointer fine)
- Demo figure: yPercent parallax scrub
- Magnetic pull on pill buttons (pointer fine only, lerp back on leave)
- Circular badge: continuous rotation + scroll-velocity boost
- Marquee: CSS keyframe loop, pause on hover/focus
- Hovers: pill invert + arrow nudge, link underline slide-left, row background lift — instant, no bounce
- `prefers-reduced-motion` / no-JS: everything visible, no motion, native scroll; GSAP loaded with `if (!reduced)` guard

## Quality floor

Responsive 320–1920 no h-scroll (`overflow-x: clip` + inner wrappers), focus-visible rings (orange, instant), contrast ≥4.5:1 body / ≥3:1 large (orange used on dark for large/mono-bold only), landmarks + skip link, OG tags, inline SVG favicon. Verified via Edge headless at 1440 & 375 before delivery.
