# Broadside 官方 Frame Pack 来源

- 仓库：[heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
- 固定提交：`934c88bac8cf6dc37db07cecf3bd0b58314c9921`
- 上游目录：`skills/hyperframes/assets/frame-presets/broadside/`
- 许可：[Apache-2.0](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/LICENSE)
- `FRAME.md` 和 `frame-showcase.html` 是固定提交的完整、未修改副本。SHA-256 分别为 `3af0a1e5e61bece19841671672d7732082f03d5699b713475e90323a21dbcc89` 和 `8d23a2cbeb898568a5626b38ffc864236fb4a09930d59b17c34c45f34c8e4161`。

## 字体与中文

- Barlow Regular 400 / Black 900：Google Fonts 官方 [Barlow 目录](https://github.com/google/fonts/tree/main/ofl/barlow)，SIL OFL 1.1；本地文件 `../fonts/Barlow-Regular.ttf`、`../fonts/Barlow-Black.ttf`，许可 `../fonts/OFL-barlow.txt`。SHA-256 分别为 `95aa02c7c43096e0dd44d787ba6216864a67157e402adab59b35572e0c1577ea`、`fc4f74e8475b181003f7597450c62d630622b417e367a6842972b286c49f9440`。
- IBM Plex Mono Medium 500：Google Fonts 官方 [IBM Plex Mono 目录](https://github.com/google/fonts/tree/main/ofl/ibmplexmono)，SIL OFL 1.1；本地文件 `../fonts/IBMPlexMono-Medium.ttf`，许可 `../fonts/OFL-ibm-plex-mono.txt`，SHA-256 `a9b4c49bb299e05b5f6c481e7fb5e78943d2793249a0c8874ab574a2d1ea6755`。
- 上述字体只承担英文字形。中文展示本机优先 PingFang SC Heavy / Hiragino Sans GB W6，并明确按 900 粗度处理；正文用 PingFang SC Regular / Noto Sans CJK SC。本机外的字形可能不同。英文 lowercase 造型不能直接投射到汉字，黑橙双色、粗重字阶和负空间负责维持风格。
- 完整官方 showcase 自身链接 Google Fonts，仅供设计参照；生成短片只引用项目内字体和本机中文字体，没有在线字体请求。

`FRAME.md` 为视觉权威；上一级 `../frame.md` 只保留本项目脚本依赖的 JSON token 适配层。
