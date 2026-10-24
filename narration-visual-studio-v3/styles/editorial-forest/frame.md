# Editorial Forest · local V3 style adapter

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "editorial-forest",
  "bg": "#efe7d4",
  "ink": "#1a1a17",
  "accent": "#e89cb1",
  "muted": "#3a5a36",
  "line": "#2e4a2a",
  "display_font": "'Source Serif 4', 'Songti SC', 'Noto Serif CJK SC', serif",
  "body_font": "'Source Serif 4', 'Songti SC', 'Noto Serif CJK SC', serif",
  "mono_font": "'JetBrains Mono', 'PingFang SC', 'Noto Sans CJK SC', monospace",
  "palette": {"green":"#2e4a2a","green-deep":"#243a21","green-lite":"#3a5a36","pink":"#e89cb1","pink-deep":"#d27e96","cream":"#efe7d4","cream-2":"#e6dcc4","ink":"#1a1a17"}
}
```
<!-- /style-pack-tokens:v1 -->

Read the complete authoritative [`upstream/FRAME.md`](upstream/FRAME.md), then see the pinned official [showcase](upstream/frame-showcase.html). The JSON above is only for `load_tokens()` and project initialization; it is not the design specification. Provenance, file hashes and fonts are documented in [`upstream/SOURCE.md`](upstream/SOURCE.md).

Use Source Serif 4 variable weight 500 with its optical-size axis for display, 400 for body; JetBrains Mono 500 with upper-case tracking for editorial labels. Keep the forest green / dusty pink / oat cream triad, flat paper surfaces, 2px rules, 6/8px tile radii, a mono topbar on every frame, and a monogram circle only on cover/summary. No gradients, shadows, invented statistics or third typeface. The six frame treatments are a choice library, not a page quota. Compose for the meaning of the specific subtitle, with one focal per frame and reveal actions aligned to speech.

Local authorized fonts are in [`fonts/`](fonts/) and `new_project.py` copies them to each project's `assets/fonts/`. The fonts are Latin-focused. Chinese requests Songti SC / PingFang SC before generic fallbacks; current headless Chrome did not load these system families, so the proof uses generic CJK glyphs. This differs from the upstream LXGW WenKai / Noto Serif SC pairing and should be checked on each rendering machine. Do not request fonts from the network. Source Serif 4 and JetBrains Mono variable files and SIL OFL texts are included here.
