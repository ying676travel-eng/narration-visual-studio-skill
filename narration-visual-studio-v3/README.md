# Narration Visual Studio V3 · Skill 内部使用说明

此目录是完整 Agent Skill。先读 [`SKILL.md`](SKILL.md) 和所选风格的 `styles/<name>/frame.md`、`upstream/FRAME.md`；安装入口与环境检查见本目录 [`AGENT_INSTALL.md`](AGENT_INSTALL.md)。新作品放在用户指定的工作区，不要写进已安装 Skill 目录。

七套官方风格：`cartesian`、`code-editorial`、`blockframe`、`broadside`、`cobalt-grid`、`daisy-days`、`editorial-forest`。每套自带完整官方 Frame Pack、showcase、来源说明和授权字体。`frame.md` 是脚本读取的 token 层，不能代替完整视觉规范。中文字体有系统回退，需在目标机器检查实际画面。

## 固定依赖与官方指导

在本目录执行 `npm ci`；制作时阅读本目录 [`references/hyperframes-runtime.md`](references/hyperframes-runtime.md)。无需另装 HyperFrames Agent Skill。Node.js >=22；Python 3 基础脚本只需标准库；Chrome 用于浏览器验收和渲染；FFmpeg/FFprobe 仅在导出 MP4 时需要。`npm run hf -- doctor --json` 是环境诊断，须阅读逐项结果。`npm test` 运行内置基础测试。

## 制作与检查

以下为 Agent 调用示例，`<skill-dir>` 是本目录的实际安装路径，`<work-dir>` 是用户作品目录。用户只需给字幕和风格，无需手动运行命令。

```bash
python3 <skill-dir>/scripts/new_project.py <subtitle.srt> --out <work-dir>/my-episode --style editorial-forest
cd <skill-dir>
python3 scripts/audit_project.py <work-dir>/my-episode --out <work-dir>/my-episode/review/audit.json
npm run hf -- lint <work-dir>/my-episode --json
npm run hf -- check <work-dir>/my-episode --json --snapshots
node scripts/browser_qa.mjs <work-dir>/my-episode
```

`new_project.py` 只建立输入、风格资源与规划文件；Agent 还需完成整篇理解、分镜、原创画面、GSAP 时间线和逐页视觉检查。HTML 作品在 `<work-dir>/my-episode/index.html`，必须保留同目录 `assets/`。仅用户要求 MP4 时，运行 HyperFrames `render` 并用 `scripts/verify_video.py` 验证静音视频。

本目录内的 `scripts/` 是执行工具，`references/` 是创作与检查规则，`styles/` 是七套视觉包，`licenses/` 是随包第三方许可文本。不要上传用户字幕、作品或导入风格的私有素材。
