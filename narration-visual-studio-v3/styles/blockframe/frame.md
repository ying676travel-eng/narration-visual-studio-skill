# BlockFrame style pack

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "blockframe",
  "bg": "#FFFDF5",
  "ink": "#000000",
  "accent": "#F7CB46",
  "muted": "#000000",
  "line": "#000000",
  "display_font": "'Inter', 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif",
  "body_font": "'Inter', 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif",
  "mono_font": "'Space Grotesk', 'SFMono-Regular', Menlo, Consolas, 'Noto Sans Mono CJK SC', monospace",
  "palette": {
    "white": "#FFFFFF",
    "pink": "#FE90E8",
    "blue": "#C0F7FE",
    "green": "#99E885",
    "yellow": "#F7CB46",
    "cream": "#FFDC8B"
  }
}
```
<!-- /style-pack-tokens:v1 -->

## Source and license

The complete official design authority is the pinned, preserved [`upstream/FRAME.md`](./upstream/FRAME.md), with the original [`showcase`](./upstream/frame-showcase.html) and [source, license, and font provenance](./upstream/SOURCE.md). The JSON block above is only the local machine-readable token contract; it does not replace the full official design rules. This pack includes licensed Inter and Space Grotesk Latin WOFF2 fonts under `fonts/`; generated projects carry their own copies under `assets/fonts/`. Chinese uses a local font stack as described in `SOURCE.md`.

## Identity

Bold neobrutalist graphics with poster energy. Use the exact candy palette, square corners, black borders, hard bottom-right shadows with zero blur, heavy uppercase Inter display, and compact Space Grotesk labels. A little tilt breaks a rigid grid. Strong geometry and color blocks should make the explained relationship visible, not merely decorate it.

## Token use

The JSON block above is the authoritative machine-readable contract. Its colors are exact upstream values. `bg` is the default off-white ground, `ink` and `line` alias the upstream black, and `accent` maps to the upstream yellow CTA/close-shadow role. `muted` aliases black because the source palette has no muted gray; create hierarchy through scale, pastel grounds, and spacing, not an invented gray. The complete five-pastel palette plus white is retained under `palette`. Select a ground for each composition and do not add a sixth pastel.

Use Inter 800–900 uppercase display, negative tracked; Inter 500 sentence-case body; Space Grotesk 600 uppercase labels with 0.08em tracking. At 1920×1080, the source display ramp is 2.1–5.0cqw and body is 0.95cqw; keep load-bearing text at or above 1.4cqw. Preserve the 4px border / 8px shadow and 3px / 4px coupling proportionally. Chinese-capable system fallbacks are local-only; do not introduce remote font loading.

## Composition and drawing

Use this language for sharp contrast, a sequence that can be read as a physical route, a strong before/after state, or a decisive close. Structures can include a poster-like title with a cutout motif, a stepped process that zigzags across the frame, a large split-ground comparison, or an inverted closer. Tilt selected graphic elements ±2°–12°, leaving the main reading axis clear. The showcase structures are studies, not fixed templates.

Draw with coarse SVG geometry, thick black outlines, flat fills, and hard shadow offsets. A starburst, stripe, or dot field should punctuate a meaningful corner or mark a state change; never obscure copy. Connector paths must connect actual nodes and encode the described order. Use yellow for a CTA and the special close-frame shadow. Do not turn every object into an identical bordered rectangle.

## Motion language

Use decisive, short moves: a block snaps into a named position, a thick path traces the route, or a pastel ground changes when the narrated state changes. Tilt can settle once as an object is introduced; it should not wobble continuously. Change one visual fact at a time so the audience can see what caused the next state. Hold the final arrangement long enough to read. All production states must be computable at any absolute time without relying on elapsed playback or random motion.

## Do / Don't

**Do**

- Couple 4px black borders with 8px hard shadows, and 3px borders with 4px shadows.
- Cycle the exact upstream pastel grounds to establish visual rhythm between frames.
- Use uppercase, heavy, negative-tracked Inter for display and Space Grotesk for compact uppercase labels.
- Give an element a meaningful reason to move: route, contrast, grouping, or state change.
- Use at least one intentional graphic puncture—tilt, stripe, dots, or starburst—when it supports the composition.
- Reserve yellow for the CTA and the distinctive closer treatment.

**Don't**

- Use rounded cards, blurred shadows, gradients, colored borders, or an unlisted pastel.
- Decouple the border weight from its hard-shadow offset or add a soft shadow behind it.
- Set display copy in sentence case or remove its negative tracking.
- Align every element mechanically or leave a decorative burst without a clear job.
- Fill every frame with equally loud blocks; preserve one clear focal point.
- Treat the whole narration as a poster headline or shrink the explanation to fit a shape.

## Showcase

The style pack keeps an older local `frame-showcase.html` with four seekable studies—poster statement, zigzag process, before/after split, and inverted close. The preserved official showcase under `upstream/` is the design reference; the local preview has no external scripts, fonts, or media.
