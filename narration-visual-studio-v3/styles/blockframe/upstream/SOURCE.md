# BlockFrame official Frame Pack source

- Repository: [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
- Pinned commit: `934c88bac8cf6dc37db07cecf3bd0b58314c9921`
- Original directory: `skills/hyperframes/assets/frame-presets/blockframe/`
- Files preserved byte-for-byte: [`FRAME.md`](./FRAME.md) and [`frame-showcase.html`](./frame-showcase.html)
- Repository license at the pinned commit: [Apache License 2.0](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/LICENSE)
- SHA-256: `FRAME.md` `ef8d9d47a209bed4ccc2d928c14a81cdaecb5129f5dc0cdc0dc40afc7ef92931`; `frame-showcase.html` `8d2e4963713928b353d0aa28c2c83fce415df81b66a500c192b602c0aaf4ddf2`.

The official showcase references Google Fonts and is retained solely as a design reference. The authored sample does not load it or request remote resources.

## Local font package

The official BlockFrame directory does not contain font binaries. This pack includes Latin WOFF2 files from the pinned [Fontsource 5.3.0 Inter package](https://www.jsdelivr.com/package/npm/@fontsource/inter?version=5.3.0) and [Space Grotesk package](https://www.jsdelivr.com/package/npm/@fontsource/space-grotesk?version=5.3.0): Inter 500/900 and Space Grotesk 600. Their OFL licenses come from the official [Google Fonts Inter](https://github.com/google/fonts/tree/main/ofl/inter) and [Space Grotesk](https://github.com/google/fonts/tree/main/ofl/spacegrotesk) directories. In the style pack the files are under `fonts/`; generated projects keep them under `assets/fonts/`.

Chinese glyphs are not present in those Latin subsets. The sample uses the local `PingFang SC`, `Hiragino Sans GB`, `Microsoft YaHei`, or `Noto Sans CJK SC` stack, with heavy weight for Chinese headlines. Chinese appearance depends on locally installed fonts; no system font is redistributed.
