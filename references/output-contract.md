# Output contract — locked

One deliverable, one format. No improvising. The output must render as a preview in any host (Gemini Canvas, ChatGPT Canvas, Claude artifacts, or a browser) with zero setup.

## The locked default: ONE self-contained `index.html`

Every slicing job delivers a **single HTML file** containing the complete design. Not "sometimes HTML, sometimes Tailwind, sometimes a project tree" — always this.

Structure:

```html
<!DOCTYPE html>
<html lang="...">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>...</title>
  <!-- Google Fonts <link> ONLY if the reference uses a non-system face; always with system fallbacks -->
  <style>
    /* 1. reset → 2. tokens (every measured value as CSS custom properties)
       → 3. base → 4. components → 5. sections in reference order */
  </style>
</head>
<body>
  <!-- sections top→bottom, same order as the reference bands -->
  <script> /* interactions only; page must be complete without JS */ </script>
</body>
</html>
```

Rules (all mandatory):

- **All CSS in one `<style>` block.** All JS inline. No CSS files, no JS files, no build step, no npm.
- **Tokens first in the stylesheet** — every measured color/size/radius/shadow as a custom property; components reference tokens only.
- **Fonts**: Google Fonts via `<link>` + fallback stack (`font-family: "Circular Std", "DM Sans", system-ui, sans-serif`). If the sandbox blocks external fonts, fallbacks keep the layout intact.
- **No external images, ever.** Photos/illustrations become inline SVG or data-URI placeholders with the exact measured aspect ratio, radius, and treatment. Icons: inline SVG (one style, matching the reference).
- **No `localStorage`/`sessionStorage`. No external API calls. No `alert()`. No `@import`.**
- External scripts allowed only from `cdnjs.cloudflare.com`, and only when genuinely required (chart lib, icon lib) — the default build needs none.
- Full responsive behavior inside this one file (320 → 1920 px, no horizontal scroll).
- The page must be complete without JS; JS only adds interaction present/implied in the reference.

## React variant — only on explicit request

Ship single-file HTML **unless the user explicitly asks for React**. When they do, match the host:

| Host | Deliver |
|---|---|
| Gemini / ChatGPT | Single HTML file running React 18 UMD + Babel standalone from CDN, one `<script type="text/babel">` component tree, Tailwind via CDN `<script>`, tokens in a `<style>` block |
| Claude (artifacts) | Single-file JSX artifact: default export, no required props, no localStorage, no `<form>`, external images none, icons via lucide-react |
| Local project explicitly requested | Vite + React + Tailwind scaffold — only when the user asks for a real codebase |

Never mix: don't emit Tailwind class soup inside the HTML default, don't emit a project tree when a single file previews fine. When the user says "modern stack" without specifics, use the React-via-CDN single file — same preview convenience, modern component code.

## Delivery behavior (why Gemini stopped at analysis)

- **Never stop after analysis.** Analysis, tokens, and the complete runnable file happen in the **same response**. The analysis section stays short (inventory table + key measurements) — it is scaffolding for the code, not the deliverable.
- If the file is too long for one message: stop mid-file at a clean boundary, say "continuing", and **finish the file in the next message unprompted**. The user should never have to ask twice.
- Open with the section inventory + token table (compact), then the full code block, then a short close: assumptions (marked ASSUMED), what to replace (`TODO: asset`), and "open the file / preview to view".
- If the host has a canvas/artifact system, emit the file so it opens there automatically — one complete HTML file triggers preview in Gemini Canvas, ChatGPT Canvas, and Claude artifacts alike.
- Offer iteration explicitly: "Tell me what's off vs the reference and I'll fix those bands."
