# 🎯 UI Slicing — pixel-perfect UI replication from any reference image

**[▶ Live landing page](https://viesloxy.github.io/ui-slicing/)** — the page itself is built by the workflow it documents.

An [Agent Skills](https://agentskills.io)-compatible skill + toolkit that turns a UI reference image — a Pinterest pin, a Dribbble shot, a SaaS screenshot, anything — into **pixel-faithful front-end code**, with a built-in **anti-AI-slop system** that keeps generated output from drifting into generic "AI look".

Works with: **Gemini · ChatGPT · Claude · Copilot · MiniMax · Grok** (chat — just attach the files) and **Cursor · Claude Code · Codex · Gemini CLI · VS Code · Copilot · pi · OpenCode · Cline · Kilo Code · Windsurf · Roo Code** + 40 more tools that read the [Agent Skills](https://agentskills.io/clients) standard.

---

## Why

AI-generated UI fails in two predictable ways:

1. **Generic defaults** — it builds what such a design *usually* looks like (Inter everywhere, purple gradients, 3-card grids) instead of what the image shows.
2. **Lazy approximation** — right structure, wrong numbers: spacing that "looks about right", colors that are close but not the color.

This skill attacks both: **measure, don't guess** and **the reference wins**.

## What's inside

```
ui-slicing/
├── SKILL.md                          # the 6-step workflow the agent follows
├── references/
│   ├── analysis-protocol.md          # measuring technique: px → tokens, font identification + substitution table
│   ├── anti-slop-checklist.md        # fidelity gates, injection tells, quality floor, self-critique
│   └── output-contract.md            # locked deliverable spec: one self-contained index.html
└── scripts/
    ├── fetch_reference.py            # download reference from URL (og:image → Pinterest/Dribbble/blog pages)
    ├── slice_reference.py            # analyze: dimensions, DPR, palette (hex + coverage), section detection; save zoomed band crops
    └── compare_screens.py            # side-by-side + diff heatmap + per-band diff score (fix worst bands first)
```

Requires [Pillow](https://pypi.org/project/Pillow/) for the scripts: `pip install Pillow`

## Install

### Generative AI — chat, no install

**Gemini · ChatGPT · Claude · Copilot · MiniMax · Grok** — attach `SKILL.md` + the `references/` folder together with your reference image, then ask: *"slice this UI"*. Paste the script contents too if the model can run code.

### Coding agents & IDEs — skills directory

```bash
cp -r ui-slicing ~/.agents/skills/
```

Works for any agent that reads the Agent Skills standard — **Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot, VS Code, Antigravity, Cline, Kilo Code, Kimi, Windsurf, Roo Code, TRAE, Kiro** and more. Native dirs also fine:

```bash
cp -r ui-slicing ~/.claude/skills/   # Claude Code
cp -r ui-slicing .cursor/skills/     # Cursor (project-level)
cp -r ui-slicing ~/.gemini/skills/   # Gemini CLI
cp -r ui-slicing ~/.codex/skills/    # Codex
```

### Agent harnesses — terminal-native

**pi · OpenCode · Amp · Goose · OpenHands** and others — the standard dir above works; pi also scans `~/.pi/agent/skills/`:

```bash
cp -r ui-slicing ~/.pi/agent/skills/
```

> 46+ tools support the Agent Skills standard — see the [client list](https://agentskills.io/clients). Path differs per tool; check your tool's docs.

## The workflow

```
0. ACQUIRE     fetch_reference.py pulls the image from a URL (or use a local file)
1. ANALYZE     slice_reference.py → palette, section boundaries, zoomed band crops
               the agent reads every crop before writing a single line of code
2. TOKENS      exact colors, identified fonts, measured spacing → tokens file first
3. PLAN        every section listed, measured, wireframed
4. BUILD       one section at a time, checked against its crop immediately
5. VERIFY      compare_screens.py → fix the highest-diff bands, repeat
6. DELIVER     deviations & assumptions reported explicitly, never silently
```

**Locked output contract** — every job delivers **one self-contained `index.html`** (inline CSS/JS, embedded design tokens, SVG placeholders) that previews instantly in Gemini Canvas, ChatGPT Canvas, Claude artifacts, or any browser. No "sometimes HTML, sometimes a Tailwind project" — one format, always. React only on explicit request.

Core rules baked into the skill:

- **The reference wins.** If the design uses three equal cards, Inter, or a centered hero — replicate it exactly. Slop is only when the AI *invents* these.
- **Measure, don't guess.** Every number comes from pixels, never from what such designs usually use.
- **Never inject.** No font swaps, no gradients/emoji/shadows absent from the reference.
- **No invented content.** Fake metrics and testimonials are slop.
- **Detail parity.** Input states, focus rings, empty states weigh as much as the hero.

## Example scripts usage

```bash
# download a reference from Pinterest / Dribbble / any page
python scripts/fetch_reference.py "https://pinterest.com/pin/xxxxxxx"

# analyze + slice into section crops
python scripts/slice_reference.py reference.png --outdir slices --bands

# zoom into one card / button / form
python scripts/slice_reference.py reference.png --crop 120,640,380,400 --zoom 3

# after building: compare your screenshot against the reference
python scripts/compare_screens.py reference.png output.png --outdir compare
```

## Sources

Distilled from production-grade material: Anthropic's `frontend-design` & `web-artifacts-builder` skills, the **Hallmark** anti-slop skill, leaked system prompts of **v0**, **Bolt** and **Same.dev**, community AI-tell catalogs, and *Refactoring UI*. Full list in [SOURCES.md](SOURCES.md).

## License

[MIT](LICENSE)
