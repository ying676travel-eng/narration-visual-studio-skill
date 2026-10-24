# Cartesian style pack

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "cartesian",
  "bg": "#EDE8E0",
  "ink": "#1A1A1A",
  "accent": "#8A8178",
  "muted": "#5A5A5A",
  "line": "#B8B0A4",
  "display_font": "'Playfair Display', 'Songti SC', 'Noto Serif CJK SC', 'Source Han Serif SC', serif",
  "body_font": "'Inter', 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif",
  "mono_font": "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, 'Noto Sans Mono CJK SC', monospace",
  "palette": {
    "bg-secondary": "#E2DBD1",
    "text-primary": "#1A1A1A",
    "text-secondary": "#5A5A5A",
    "accent": "#8A8178",
    "line": "#B8B0A4",
    "white-overlay": "rgba(255,255,255,0.3)"
  }
}
```
<!-- /style-pack-tokens:v1 -->

## Source and license

The complete official design authority is [`upstream/FRAME.md`](upstream/FRAME.md), pinned to HyperFrames commit `934c88bac8cf6dc37db07cecf3bd0b58314c9921`. Inspect its [official showcase](upstream/frame-showcase.html) before designing a frame. [`upstream/SOURCE.md`](upstream/SOURCE.md) records paths, hashes, license and font provenance. This `frame.md` retains the JSON token contract for project scripts; its summaries do not replace the upstream rules.

The local [`fonts/`](fonts/) folder contains licensed Playfair Display 400 variable TTF, Inter 400 WOFF2, and JetBrains Mono 400 WOFF2 with individual OFL texts. Project generation packs these assets into `assets/fonts/`. These fonts cover Latin glyphs; Chinese headlines and body fall back to Songti SC / PingFang SC or the listed CJK alternatives. No online font request is required.

## Identity

Quiet museum-catalogue editorial on warm stone. Playfair Display 400 carries sentence-case display; Inter carries body copy and tracked labels. A single taupe hairline is the structural mark. Compass-drafted rings can sit behind content as atmosphere. Depth comes from type contrast, precise alignment, and negative space; the surface stays flat.

## Token use

The JSON block above is the authoritative machine-readable contract. Its five color values map directly to upstream `bg-primary`, `text-primary`, `accent`, `text-secondary`, and `line`. The additional `palette` entries preserve the other upstream colors. Use `bg` for the ground; `ink` for large display; `muted` for body; `accent` for restrained labels and numerals; `line` for all structural rules. Do not introduce another accent color.

Typography follows the upstream scale at 1920×1080: Inter body 1.0cqw / line-height 1.6; Inter labels 14px, medium, uppercase with 3px tracking; Playfair 400 display from 1.8cqw to 8.0cqw. Keep load-bearing text at or above 1.4cqw and size headlines to their length. CSS stacks are local-only and include Chinese fallbacks; do not add a CDN font link.

## Composition and drawing

Treat each scene as a composition decision, not a reusable page. Prefer a generous edge-anchored field for a thesis, a two-column editorial split for comparison, an open radial or orbital diagram for a system, and a single-rule rail for sequence. Use a quote-like centered composition only when the spoken idea merits a pause. The four showcase studies demonstrate alternatives; they are not required templates.

Draw with clean SVG paths, circles, and fine rules. Rings should be compass-like: one or two per frame, with solid and dashed construction arcs at 20–50% opacity. A connector must have meaningful endpoints and explain sequence, relation, or focus. Keep labels legible and subordinate; use the secondary stone only for a placeholder or a quiet region. Do not draw fake numbers or product UI.

## Motion language

Use a quiet reveal: reveal a phrase by clause, draw a line only when it traces an actual relation, and let a ring resolve around a focal point when the narration introduces a system or boundary. Motion should stop once it has explained the change. Favor long, deliberate drawing and short, precise emphasis; no perpetual drift. For production, every state must be derived from the absolute composition time so seeking forward, backward, or directly into the middle gives the same image.

## Do / Don't

**Do**

- Use the same 1px taupe hairline for dividers, timeline rails, and outlines.
- Keep Playfair at weight 400, ink, and sentence case; reserve uppercase tracking for small Inter labels.
- Keep a declarative frame spacious, with roughly 55–60% open field when the content allows it.
- Use asymmetric edge-anchored layouts for explanation and centered layouts for a deliberate quote or close.
- Limit compass-ring decoration to one or two elements behind the main content.
- Let scale, type contrast, and alignment carry emphasis before adding a shape.

**Don't**

- Add a bright/populist accent, gradient, shadow, thick border, or rounded rectangle.
- Bold Playfair, set a headline in taupe, or make body copy the same color as the large display.
- Pack a frame until it feels like a dashboard; sparsity is a deliberate part of the identity.
- Use an isolated line, ring, or dot that has no named anchor or explanatory job.
- Repeat the same centered headline layout for every scene.
- Make geometry larger than the idea it is meant to clarify.

## Showcase

Open the complete [official `upstream/frame-showcase.html`](upstream/frame-showcase.html) to judge typography, space and geometric restraint. An older condensed study remains in the style pack as `frame-showcase.html` for comparison; it is not the official source.
