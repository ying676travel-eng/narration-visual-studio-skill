# Agent 安装指南 · 只注册一套 Skill

此文档给收到发行仓库首页链接的编程 Agent。用户只需提供链接；下载、依赖安装和验证由 Agent 执行。用户字幕与作品留在本机。

## 安装目标

本仓库唯一需要注册的 Agent Skill 是 `narration-visual-studio-v3/SKILL.md`。必须把该**完整子目录**一起安装：`references/`、`scripts/`、`styles/`、`licenses/`、`package.json` 和 `package-lock.json` 都在其中。不要只复制 `SKILL.md`，也不要把仓库根目录当作 Skill 目录。

1. 检查 Node.js 22+、npm、Python 3 和 Google Chrome；仅用户要导出 MP4 时再检查 FFmpeg/FFprobe。缺失时按当前系统正常安装或说明限制，不要求 API Key。
2. 按当前 Agent 的**官方 Skill 安装机制**下载并注册 `narration-visual-studio-v3`。对 Codex，优先调用自带 `$skill-installer`，指定仓库 `ying676travel-eng/narration-visual-studio-skill` 与路径 `narration-visual-studio-v3`。默认目标是 `$CODEX_HOME/skills/narration-visual-studio-v3`，未设置 `CODEX_HOME` 时是 `~/.codex/skills/narration-visual-studio-v3`。目标已存在时先检查本地改动，不直接覆盖。
3. 在已安装的 V3 Skill 目录执行 `npm ci`，取得锁定的 **HyperFrames CLI/runtime 0.8.185、GSAP 3.14.2、Playwright 1.61.1、sharp 0.35.5**。这些是 Node 运行依赖，不会因此注册新的 Agent Skill。Python 基础脚本只使用标准库。
4. 执行 `npm test`，并用 `npm run hf -- doctor --json` 逐项核对当前流程需要的 Node、Chrome；语音、音乐、Docker 属可选项，不能只看 doctor 总体布尔值。确认七个 `styles/<name>/frame.md`、`upstream/FRAME.md`、`upstream/frame-showcase.html` 都存在。
5. 确认当前 Agent 能识别 `narration-visual-studio-v3`。Codex 安装后通常在下一轮对话看到 `$narration-visual-studio-v3`；当前对话的 Skill 列表未必立即刷新。报告安装位置、依赖和七套风格检查结果。

**只注册这一个 Skill。**不要执行 `hyperframes skills update`、`npx skills add heygen-com/hyperframes`，也不要安装 `/hyperframes`、`/hyperframes-cli`、`/hyperframes-registry`、`/media-use`。V3 制作所需的技术约定已经在 [`references/hyperframes-runtime.md`](references/hyperframes-runtime.md) 中；遇到接口疑问，读取已安装 npm 包的 `dist/docs/`，或运行锁定版 `npm run hf -- docs <主题>` / `npm run hf -- <命令> --help`。不调用 `hyperframes init`：0.8.185 的 `init --help` 明示它会检查 Agent Skills，且 `--skip-skills` 暂时无效。新作品用现有 `scripts/new_project.py` 初始化。

## 其他 Agent 与常见问题

WorkBuddy、Claude Code、Cursor 等平台的 Skill 目录与发现方式可能不同；先查其官方机制，再安装完整 V3 子目录，不能照搬 Codex 路径。WorkBuddy 的独立新会话与新字幕作品尚待发行者外部验收，本说明不声称已验证兼容。

若提示找不到 `SKILL.md`，核对是否把仓库首页误当作安装路径；正确入口在子目录。若 `npm ci` 失败，先核对 Node 版本和网络。若浏览器检查失败，核对 Chrome 和 CLI 的具体错误。作品应写在用户工作区；从已安装 Skill 目录运行 HyperFrames 检查时，传入作品的绝对路径。不要把用户作品写进 Skill 目录，也不要触碰用户现有的其他 Skills。
