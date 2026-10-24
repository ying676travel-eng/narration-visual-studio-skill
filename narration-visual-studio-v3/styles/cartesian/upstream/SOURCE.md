# Cartesian 官方 Frame Pack 来源

- 仓库：[heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
- 固定提交：`934c88bac8cf6dc37db07cecf3bd0b58314c9921`
- 上游目录：`skills/hyperframes/assets/frame-presets/cartesian/`
- 上游仓库许可：[Apache-2.0](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/LICENSE)；`FRAME.md` 和 `frame-showcase.html` 是固定提交的未改动副本，设计依据以 `FRAME.md` 为准。展示页仅供视觉参照。
- 本地核对 SHA-256：`FRAME.md` = `3dc6a31813a333b2a7a1509ddbd3b4dabbbd7e12e6479b6cff10d69c185fec95`；`frame-showcase.html` = `d7867cee5e07c4f22345c566071f2ce0261b3fccca111a94dfbec5fde64f3e55`。

## 字体

- `../fonts/PlayfairDisplay-wght.ttf`：Google Fonts 官方 [Playfair Display 目录](https://github.com/google/fonts/tree/main/ofl/playfairdisplay) 的可变正体，用于英文展示，SIL OFL 1.1，许可见 `../fonts/OFL-playfair-display.txt`。固定落地文件，不走在线字体服务。CSS 将字重限定为 400。
- `../fonts/Inter-400.woff2`、`../fonts/JetBrainsMono-400.woff2`：来自同一固定 HyperFrames 提交的 Code Editorial preset 字体包，分别遵循旁边的 `OFL-inter.txt`、`OFL-jetbrains-mono.txt`。Inter 用于英文正文与标签；JetBrains Mono 仅保留机读 token 的本地字体角色，Cartesian 的视觉规范不要求等宽字体上屏。
- Playfair Display / Inter / JetBrains Mono 的文件不含汉字。中文展示用本机 `Songti SC` 优先，正文用 `PingFang SC` 优先，其他系统走 `Noto Serif CJK SC` / `Noto Sans CJK SC` 等回退。中文回退不是打包字形，跨系统字形可能变化；浏览器截图需单独核查。
- 本次落地字体 SHA-256：Playfair = `c40f2293766a503bc70cce9e512ef844a4ccb7cbcde792fe2ea31d191917d8d6`；Inter = `8909904ab6c872eb994093482a88a28eca2cd95912d7b6fecd72103b0dc07edc`；JetBrains Mono = `14425ba9c695763c1547f48a206b7aa60350a33ae23de09f0407877f3fcd89eb`。

## 分工

`FRAME.md` 是完整官方规范；上一级 `../frame.md` 的 JSON 块是本项目脚本读取的适配契约。新项目应同时保留规范副本及自带字体资产。
