# Daisy Days · 本地适配

创作前必须通读 [官方完整 FRAME](upstream/FRAME.md)；[官方 showcase](upstream/frame-showcase.html) 是版面参照。本文件只保留项目初始化与审计需要的机读颜色、字体角色，以及中文和资源落地说明，不能替代原规范。

<!-- style-pack-tokens:v1 -->
```json
{
  "id": "daisy-days",
  "bg": "#F5F0E6",
  "ink": "#2D2D2D",
  "accent": "#F8635F",
  "muted": "#6B6B6B",
  "line": "#2D2D2D",
  "display_font": "Fredoka",
  "body_font": "Quicksand",
  "mono_font": "Quicksand"
}
```
<!-- /style-pack-tokens:v1 -->

完整调色板在原文。奶油底配一块粉彩主色；珊瑚色只点小标记。卡片是白底、炭黑 3px 轮廓、6px 无模糊硬阴影，圆角 20/28px。标题用 Fredoka 600，正文用 Quicksand 500/600；粉彩底的白色标题加硬文字阴影。每场围绕一个主要内容容器，边角放 3–7 个手绘雏菊、星星、太阳、云、彩虹，不把它简化成换色模板。

本地 [fonts/](fonts/) 含官方来源和 SIL OFL 许可。西文使用 Fredoka 与 Quicksand 的本地 WOFF2。中文标题使用授权的 ZCOOL KuaiLe 作为圆润适配，正文依次回退 PingFang SC、Hiragino Sans GB、Microsoft YaHei、Noto Sans CJK SC；这与原文建议的 ZCOOL XiaoWei / Yozai 组合不同，理由及限制见 [来源说明](upstream/SOURCE.md)。页面不得运行时请求 Google Fonts。
