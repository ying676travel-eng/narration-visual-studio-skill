# Editorial Forest official frame pack

- Source: https://github.com/heygen-com/hyperframes/tree/934c88bac8cf6dc37db07cecf3bd0b58314c9921/skills/hyperframes/assets/frame-presets/editorial-forest
- Commit: `934c88bac8cf6dc37db07cecf3bd0b58314c9921`; upstream repository license: Apache-2.0.
- `FRAME.md` and `frame-showcase.html` are unmodified copies from that commit. SHA-256: `ceeb2ab768367da1e1f3e1eca36ab9feeb3de3e4d15493319b0044c3d869329c` and `bb87b88b91184f4fee7f02eea63ed35d9d378fa89fad8988326e31e82a43dbb1`.
- The upstream preset does not bundle fonts. `../fonts/SourceSerif4-opsz-wght.ttf` and `../fonts/JetBrainsMono-wght.ttf` come from [Google Fonts' official open-source repository](https://github.com/google/fonts), `ofl/sourceserif4/` and `ofl/jetbrainsmono/`, with their SIL OFL license texts. Both are variable fonts; Source Serif 4 preserves the optical-size axis.
- The upstream CJK pair LXGW WenKai / Noto Serif SC is not bundled. The local output requests Songti SC / PingFang SC first, then generic serif / sans-serif fallback; these system families were unavailable in the current headless Chrome, so current proof uses generic CJK glyphs. No remote font request is required.
