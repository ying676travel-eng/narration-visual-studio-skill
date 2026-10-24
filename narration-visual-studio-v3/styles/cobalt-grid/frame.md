# Cobalt Grid style pack

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "cobalt-grid",
  "bg": "#F0EBDE",
  "ink": "#1F2BE0",
  "accent": "#1F2BE0",
  "muted": "#5560E5",
  "line": "#1F2BE0",
  "display_font": "'Newsreader', 'Songti SC', 'STSong', 'Noto Serif CJK SC', serif",
  "body_font": "'Hanken Grotesk', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif",
  "mono_font": "'DM Mono', 'SFMono-Regular', Menlo, Consolas, monospace",
  "palette": {"paper": "#F0EBDE", "paper_2": "#E6E0CE", "ink_soft": "#5560E5", "grid": "rgba(31,43,224,0.10)", "ink_faint": "rgba(31,43,224,0.18)"}
}
```
<!-- /style-pack-tokens:v1 -->

## Design authority and assets

The complete official design rules are preserved in [`upstream/FRAME.md`](./upstream/FRAME.md). See the original [`frame-showcase.html`](upstream/frame-showcase.html) for composition studies and [`SOURCE.md`](./upstream/SOURCE.md) for license, hashes, and font provenance. The JSON above is only the machine-readable adapter for `load_tokens()`; use the full upstream source to design frames.

The original preset has only cream paper and electric cobalt ink. `accent` aliases cobalt because the machine schema requires it; it does **not** authorize a second accent color. `muted` is the specified softer cobalt. Keep the grid and the two hairlines visible on *every* frame. Use the exact editorial font roles: Newsreader 400 for Latin display, Hanken Grotesk for body/tracked labels, DM Mono for chrome. Local WOFF2 files live in this pack's `fonts/` and in a generated project's `assets/fonts/`; define `@font-face` from the project-relative paths. Chinese display falls back to local Songti SC or Noto Serif CJK SC at normal weight; Chinese body to a local sans stack. Do not treat a Latin font load as proof of Chinese glyph coverage.

Never add colored fills, shadows, rounded cards, dark gray text, or disable the graph grid. The pixel-glitch, QR-block, pixel-stack, ledger rows, and vertical catalogue labels are grammar pieces, not a fixed slide template. Numbers and comparisons must come from the actual script; empty slots remain empty until supported by the narration.
