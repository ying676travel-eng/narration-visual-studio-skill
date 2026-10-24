# Cobalt Grid official Frame Pack source

- Repository: [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
- Pinned commit: `934c88bac8cf6dc37db07cecf3bd0b58314c9921`
- Original directory: `skills/hyperframes/assets/frame-presets/cobalt-grid/`
- Preserved byte-for-byte in the style pack: [`FRAME.md`](./FRAME.md) and [official `frame-showcase.html`](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/skills/hyperframes/assets/frame-presets/cobalt-grid/frame-showcase.html)
- Repository license: [Apache License 2.0](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/LICENSE)
- SHA-256: `FRAME.md` `62a6c9e6e5188cc29b9c0098e9bb8e72c23f152d9a99dd92c58139d26b69b19f`; `frame-showcase.html` `b135214cd2e310273a01e3f72b2828149f022803954a22a13cbf27aa1c2f518a`.

The upstream showcase loads Google Fonts and is kept as a design reference. The authored sample uses local assets only.

## Fonts

The upstream preset does not include font binaries. Latin WOFF2 files come from pinned Fontsource 5.3.0 packages: [Newsreader](https://www.jsdelivr.com/package/npm/@fontsource/newsreader?version=5.3.0) 400, [Hanken Grotesk](https://www.jsdelivr.com/package/npm/@fontsource/hanken-grotesk?version=5.3.0) 400/600, and [DM Mono](https://www.jsdelivr.com/package/npm/@fontsource/dm-mono?version=5.3.0) 400. Their OFL license files are from the corresponding official Google Fonts directories: [Newsreader](https://github.com/google/fonts/tree/main/ofl/newsreader), [Hanken Grotesk](https://github.com/google/fonts/tree/main/ofl/hankengrotesk), [DM Mono](https://github.com/google/fonts/tree/main/ofl/dmmono). In the style pack the binaries and licenses are under `fonts/`; generated projects copy them to `assets/fonts/`.

Latin subsets have no Chinese glyphs. The sample uses local Songti SC / STSong / Noto Serif CJK SC for Chinese display, and PingFang SC / Hiragino Sans GB / Microsoft YaHei / Noto Sans CJK SC for Chinese body. No Chinese system font is redistributed. The exact CJK shape can vary between systems.
