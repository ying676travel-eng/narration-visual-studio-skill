# Broadside · 本地风格适配

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "broadside",
  "bg": "#111111",
  "ink": "#F0ECE5",
  "accent": "#E85D26",
  "muted": "#888880",
  "line": "#282826",
  "display_font": "'Barlow', 'PingFang SC', 'Noto Sans CJK SC', sans-serif",
  "body_font": "'Barlow', 'PingFang SC', 'Noto Sans CJK SC', sans-serif",
  "mono_font": "'IBM Plex Mono', 'SFMono-Regular', 'Noto Sans Mono CJK SC', monospace",
  "palette": {
    "ink-black-alt": "#1A1A18",
    "cream": "#F0ECE5",
    "cream-muted": "#888880",
    "cream-hint": "#505048",
    "border-dark": "#282826",
    "ink-on-orange-muted": "rgba(17,17,17,0.75)",
    "ink-on-orange-hint": "rgba(17,17,17,0.55)",
    "ink-on-orange-faint": "rgba(17,17,17,0.40)",
    "ink-on-orange-border": "rgba(17,17,17,0.20)"
  }
}
```
<!-- /style-pack-tokens:v1 -->

设计权威是完整官方 [`upstream/FRAME.md`](upstream/FRAME.md)；先读原件并对照 [官方 showcase](upstream/frame-showcase.html)。[来源、许可和字体](upstream/SOURCE.md) 单独记录。上面的 JSON 只是 `load_tokens()` 所需机读适配层，不能替代官方完整规则。`bg` 等字段表示深色 register；橙色场要切换为 `accent` 作底、`#111111` 作字，不能把 `ink` 的奶油白用在橙底。

本地 [`fonts/`](fonts/) 包含 Barlow 400/900 与 IBM Plex Mono 500 及各自 OFL。新项目把它们复制至 `assets/fonts/`。中文使用本机粗黑体回退并在截图中核查；无在线字体依赖。

Broadside 是黑橙两档的海报式系统：深色场用奶油白大字、橙色单点强调；宣言场可用整版橙底配墨色字。英文展示为 Barlow 900 小写、负字距，一场一个绝对主角；Mono 只负责大写目录编号、眉题与小标签。中文没有大小写，应用足够粗的字重和宽阔留白，而非伪造字形效果。只用 1px 结构线；无圆角卡片、阴影、渐变、第二种亮色。段落关系可用一条线、一组对比或一次橙色场切换讲明，数字必须来自字幕。

本风格的三场以上 sample 仅是验证，官方六种 Frame Treatments 是可选构图库，不是页数配额。编写时必须按口播语义选择，不把同一 DOM 骨架换色复用。
