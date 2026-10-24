# Code Editorial style pack

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "code-editorial",
  "bg": "#FAF9F5",
  "ink": "#141413",
  "accent": "#CC785C",
  "muted": "#1F1E1B",
  "line": "#DEDEDA",
  "display_font": "'EB Garamond', 'Songti SC', 'Noto Serif CJK SC', 'Source Han Serif SC', serif",
  "body_font": "'Inter', 'PingFang SC', 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif",
  "mono_font": "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, 'Noto Sans Mono CJK SC', monospace",
  "palette": {
    "tile": "#EFE9DE",
    "tile-strong": "#ECE3D4",
    "navy": "#181715",
    "navy-soft": "#1F1E1B",
    "navy-elev": "#252320",
    "syntax-teal": "#5DB8A6",
    "syntax-amber": "#E8A55A",
    "status-success": "#5DB872",
    "status-warn": "#C64545"
  }
}
```
<!-- /style-pack-tokens:v1 -->

## Read this first — 本地适配层

这个文件有**两个身份**，别混：

- 上面的 `json` 块是**机读契约**：`audit_project.load_tokens()` 和 `new_project.py` 依赖它，
  字段不可删改。它是调色板和字体栈的单一来源。
- 设计权威是**同目录 [`upstream/FRAME.md`](upstream/FRAME.md) 的完整原始规范**（HyperFrames 官方 preset，
  固定 commit `934c88b`），外加 [`upstream/frame-showcase.html`](upstream/frame-showcase.html) 的四种研究页。

动手顺序：① 通读 `upstream/FRAME.md` 全文（不只 token 段）→ ② 打开 `upstream/frame-showcase.html`
建立"什么算对"的基准 → ③ 读本文件后面的中文精简说明 → ④ 按
[`../../references/code-editorial-execution.md`](../../references/code-editorial-execution.md)
执行字号档位、构图选择、颜色配额、中文混排和字体验证 → ⑤ 再写 HTML。

字体在本目录 [`fonts/`](fonts/)：EB Garamond / Inter / JetBrains Mono 的 400 + 700 WOFF2 与 OFL 许可。
`new_project.py --style code-editorial` 会把它们复制到新项目的 `assets/fonts/`，
作品只引用自己目录下的相对路径，**不要**指向其他作品或远程字体服务。展示层按 400 排字。

本文件其余章节是中文精简说明，可能与原始规范有省略；冲突时以 `upstream/FRAME.md` 为准。
cartesian / blockframe 不受本适配层影响，仍按各自 `frame.md` 执行。

## Source and license

Adapted from HyperFrames' Code Editorial frame preset, [`FRAME.md`](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/skills/hyperframes/assets/frame-presets/code-editorial/FRAME.md), pinned to commit `934c88bac8cf6dc37db07cecf3bd0b58314c9921`. The source repository declares Apache-2.0; the verbatim copy lives in [`upstream/`](upstream/) with its own [SOURCE.md](upstream/SOURCE.md).

The WOFF2 files in [`fonts/`](fonts/) ship with the upstream preset under the SIL Open Font License; the licence texts sit beside them (`OFL-eb-garamond.txt`, `OFL-inter.txt`, `OFL-jetbrains-mono.txt`). Display is authored at weight 400; the 700 files are spare.

EB Garamond covers Latin glyphs only. No remote font request is made: Chinese resolves to the local Songti SC / PingFang SC stack listed in the token block, and a work must not claim the serif is setting its Chinese.

## Identity

A warm editorial register for technical ideas: cream paper, ink, one scarce terracotta coral moment, and a warm-navy surface when code itself is part of the explanation. EB Garamond carries sentence-case display and expressive italic; Inter carries readable explanation; JetBrains Mono signals index, code, and status. A low-contrast hairline and a warm half-step surface separate content without turning the frame into software chrome.

## Token use

The JSON block above is the authoritative machine-readable contract. The canonical color values are copied from the upstream preset. `bg`, `ink`, and `accent` map to `cream`, `ink`, and `coral`. `muted` aliases the exact `navy-soft` palette value for dark structural surfaces; do not use it as generic body text. `line` is upstream `#141413` ink at 12% composited over the default `#FAF9F5` cream ground, rounded to `#DEDEDA` for the six-digit token contract. On dark code surfaces, use the source's separate cream-at-14% hairline. The fixed syntax colors stay inside code illustrations and are not additional brand accents.

Use the exact upstream type roles: Inter body 1.5cqw / 1.5 line-height, Inter lead 2.08cqw, JetBrains Mono uppercase kicker 1.46cqw with 0.16em tracking, EB Garamond display 4.6–9.9cqw at weight 400 with the specified negative tracking. Keep important lines at or above 1.4cqw. Chinese fallback stacks are local-only; no CDN or `@import` font dependency is permitted.

## Composition and drawing

Choose a structure for the explained relationship: a full-bleed editorial statement for a conclusion, a deliberate two-register split for a change, a warm-navy code surface for a code mechanism, a typographic pull quote for a thesis, or an open sequence for a workflow. Use the dark surface because the code is evidence or mechanism, not as the default background. A scene may be dense when the reasoning needs it; a card grid is not the default.

The six frame treatments in `upstream/FRAME.md` are a **library, not a per-scene quota**. A deck may use three of them, or repeat one, or invent a content-specific diagram the preset never named. What must hold on every frame: the cream ground, the three type voices, hairline elevation, one coral moment, and one clear focal. If a page would still read the same after swapping its keywords, the composition is a template — change the structure, not the words.

Build the explanation progressively inside the frame: nodes reveal in speaking order, connectors draw on, or one object changes state (dashed → solid, grey → ink, scattered → gathered). The final revealed state must hold as a readable still. Prefer a diagram that could only belong to this content; decorative SVG that explains nothing should be deleted.

Code examples must be clearly marked as illustrative if they are not user-provided source. Use syntax colors only inside that surface: coral keywords, teal strings, amber numbers, and the documented status colors. An SVG connector should join real process stages and stop at the final explained state. Keep the coral spike `✱` as a single emphasis moment per frame; never color the headline or a whole body paragraph coral.

## Motion language

Reveal code in the same order the narration explains it: input, rule, result. A hairline may draw on to establish a section; the coral spike may scale from 0.92 to 1 on one emphasis beat and never spin. Use a clear transformation or focus change to explain technical cause and effect. After the reveal, hold a readable state. Avoid typewriter motion that prevents a viewer from seeing a complete line during speech. Production animation must be tied to absolute time and remain deterministic under arbitrary seeking.

## Do / Don't

**Do**

- Keep the ground warm cream; use tile surfaces for half-step grouping.
- Use EB Garamond 400, sentence case, and negative tracking for every display role.
- Use Inter for body and JetBrains Mono for the technical index, code, and compact labels.
- Keep coral to one accent moment in a frame and reserve it for the spike, a single link, or one callout.
- Reserve warm navy for a code/terminal surface; use a 1px low-alpha hairline for separation.
- Make source code truthful, or label a code drawing as illustrative.

**Don't**

- Use pure white, cool gray, pure black, or an unlisted brand hue as a general surface or text color.
- Turn every scene into a terminal window or a collection of code cards.
- Set a headline in sans, set labels in serif, or use uppercase/title-case EB Garamond display.
- Spend coral twice in one frame, or use it for body copy or a headline.
- Add a heavy shadow, glow, content gradient, tilt, or oversized UI chrome.
- Let a code reveal hide the line while the audience needs to read it.

## Showcase

Open `upstream/frame-showcase.html` locally. It contains four original studies—editorial statement, split comparison, mechanism/code surface, and pull quote—with independent seek controls. The controls set each scene to an exact illustrative state without remote assets or wall-clock animation. Use it as the visual bar, not as page templates. The local `frame-showcase.html` beside this file is an older condensed version kept for comparison.
