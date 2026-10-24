# Third-party notices

本文件只说明本发行包**实际包含**或通过 `npm ci` 安装的第三方内容；不将 GSAP 误标为开源。各风格逐文件来源见 `styles/<name>/upstream/SOURCE.md`。

- **HyperFrames**：CLI/runtime 锁定 0.8.185，通过 npm 安装，包本体不随 Git 仓库分发。七套官方 Frame Pack 的 `upstream/FRAME.md` 与 `upstream/frame-showcase.html` 来自 [heygen-com/hyperframes 固定提交 `934c88b`](https://github.com/heygen-com/hyperframes/tree/934c88bac8cf6dc37db07cecf3bd0b58314c9921/skills/hyperframes/assets/frame-presets)，为 Apache-2.0。许可全文保存在 [`licenses/HyperFrames-Apache-2.0.txt`](licenses/HyperFrames-Apache-2.0.txt)。`frame.md` 是本项目的适配文档，不冒充上游原件。官方 `/hyperframes` Skill（已整合原 Core、Animation、Creative 指导）另行安装，不包含在本包。
- **GSAP**：3.14.2 由 npm 取得，不将其 JavaScript 文件提交到本仓库。使用 GSAP 核心 timeline API。其 npm 包标注 [Standard “no charge” license](https://gsap.com/standard-license/)；它不是 Apache/MIT 类开源许可。生成的本地作品若包含 GSAP 文件，需保留文件自带的许可/版权标头，并遵守 GSAP 当时适用的许可条件。
- **Playwright 1.61.1、sharp 0.35.5**：由 npm 取得，仅用于本地浏览器检查及截图处理，两个包均标注 Apache-2.0；其传递依赖及原生组件随 npm 安装并各有许可证。仓库不分发 `node_modules`。
- **字体**：七套风格在各自 `fonts/` 下含 24 个拉丁或指定中文字库文件，旁边保留相应 `OFL-*.txt`。Playfair Display、Inter、JetBrains Mono、EB Garamond、Space Grotesk、Barlow、IBM Plex Mono、Newsreader、Hanken Grotesk、DM Mono、Fredoka、Quicksand、ZCOOL KuaiLe、Source Serif 4 均按随包 [SIL Open Font License 1.1](https://openfontlicense.org/open-font-license-official-text/) 文本再分发。来源为 HyperFrames 上游、Google Fonts 或 Fontsource，详情与部分固定校验值见各 `SOURCE.md`。其他中文系统字体不打包；跨设备字形会变化。
- **展示页**：官方 HTML 展示页仅作为视觉参考；旧本地 showcase 为本项目风格示例。官方 showcase 可能包含在线字体链接，但生成作品的资源须本地化。

本仓库的原创 Skill 代码和文档尚未单独声明开源许可证；发行者允许按本仓库说明下载、安装和本机使用，但未另行授予第三方再分发或改作许可。该限制不改变以上第三方文件各自的许可证。
