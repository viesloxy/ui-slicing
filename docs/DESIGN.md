# Landing page — design plan v3 (second full redesign)

V2 rejected by owner: same skeleton as v1, the mono-micro-label system (kickers, tags, `01/02` numerals, ticker) reads generic; marquee unwanted; background flat; animations too tame; navbar/footer bland.

V3 = **Linear-2025 light aesthetic × Zentry motion**. Sources: live `linear.app` scrape (palette) + `Zentry-animated-website` (word-reveal 3D, perspective tilt, clip-path) + `dennis-snellenberg` (overlay menu, magnetic CTA).

## Scraped palette (live linear.app, 2025 theme)

```
--bg:      #E4E5E9   cool light gray (Linear base)
--panel:   #FFFFFF / rgba(255,255,255,.62)  glass cards + backdrop blur
--ink:     #0B0C0E   near-black
--muted:   #62666D
--pink:    #F79CE0   candy accent 1
--sky:     #55CDFF   candy accent 2
--peri:    #8FA4FF   candy accent 3
--peach:   #FFC47C   candy accent 4
accents appear as LARGE soft blurred radial glows behind glass, not as text/fill colors
--dark:    #08090A   install panel + footer canvas
```

Anti-slop guard: glows are multi-hue, heavily blurred, on LIGHT ground — not the dark pink→cyan aurora cluster; headline ink stays solid (no gradient text).

## Type system (mono labels abolished)

- Display: **Bricolage Grotesque** 600/700 — characterful grotesque, tight tracking
- Body: **Figtree** 400/500/600
- Accent: **Instrument Serif** italic — single emphasized words only
- No uppercase micro-labels anywhere. Section context carried by size/color, not tags.

## Structure & look

1. **Navbar** — floating glass capsule (max-width, rounded-full, blur, hairline): logo chip left, center links (Problem / Workflow / Demo / Install), CTA pill right. On scroll: capsule tightens, gains shadow. Mobile: logo + burger → **full-screen overlay menu**, giant staggered links + CTA + repo link.
2. **Hero (light + glows)** — two large blurred candy glows (pink top-left, sky bottom-right) slowly drifting (20s alternate). Centered column: H1 Bricolage 72-120px, 3 lines, word-by-word 3D reveal on load (rotateX, Zentry). Sub copy. CTA: solid ink pill + glass pill. Below: 3 floating glass mini-cards (mini code line, mini palette chips, mini crop-tag) each gently bobbing (6-8s ease alternate, staggered) with parallax on scroll.
3. **Problem** — two large glass cards side by side, each with its own glow (pink / sky) and **perspective tilt on pointer move** (Zentry bento tilt). Inside: heading + tell list as wrapped soft chips (not mono rows). Closing line big Figtree 500 with serif italic accents.
4. **Workflow** — pinned horizontal scroll retained (desktop GSAP scrub). White cards, radius 24, soft shadow; index as big Bricolage digits in candy colors (each step different accent); mobile: vertical stack.
5. **Demo** — glass panel split: annotated SVG mock + token code (light code block, ink text, candy token colors). Scroll parallax kept.
6. **Statement** — full-width, huge Bricolage: `The reference wins.` with pink hand-drawn-style SVG underline swipe (animated on enter). Supporting paragraph.
7. **Install** — full-bleed dark rounded panel (#08090A, radius 32, inside light page): 4 rows + copy buttons; subtle periwinkle glow in panel corner.
8. **Footer (dark, full-bleed)** — top: CTA row `Star on GitHub` pill + `Get the skill`; middle: giant Bricolage wordmark with pink→periwinkle soft glow behind (blur, not gradient text); bottom bar: © line + two links only.

## Motion inventory (GSAP + ScrollTrigger, cdnjs)

- Hero words: 3D flip-in stagger (rotateX -90 → 0, Zentry)
- Glow blobs: infinite slow drift (CSS), + scroll parallax (GSAP yPercent)
- Floating chips: bob loop + scroll parallax at different speeds
- Section headings: word-split scroll reveal (once, 88%)
- Cards: pointer tilt (perspective 700px, max 8deg) + shadow lift
- Workflow: pinned horizontal scrub + per-panel subtle rotateY entry
- Statement underline: scaleX swipe on enter
- Nav: shrink + shadow on scroll; overlay menu: clip-circle or slide + link stagger
- Magnetic CTA pills; scroll progress top (ink 2px)
- Reduced-motion / no-JS: everything static-visible, native scroll, menu = simple toggle

## Responsive floor

Breakpoints: 1200 (container), 960 (nav→burger, hero center, grids stack), 640 (type scale down, cards full). 375 verified by construction: no fixed-width elements, nowrap only inside `overflow-x:auto` min-width:0 boxes, glows `pointer-events:none` + `overflow:clip` wrappers. Live check at 492 (headless floor) + math for 375.
