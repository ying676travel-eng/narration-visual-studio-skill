# Agent 安装指南

此文档给收到仓库首页链接的编程 Agent。用户只需提供链接；检查、安装与验证由 Agent 执行。不要将私人字幕上传到 GitHub。

## 识别与位置

本仓库只有一套 Agent Skill：`narration-visual-studio-v3/SKILL.md`。同目录内的 `references/`、`scripts/`、`styles/`、`licenses/`、`package.json`、`package-lock.json` 必须一起安装。不要只复制 `SKILL.md`，也不要把仓库根目录当成 Skill 目录。不要复制原 Private 开发仓库。

## Codex（已核对）

1. 检查 `node --version`（>=22）、`npm --version`、`python3 --version`、Chrome；仅用户需要 MP4 时检查 `ffmpeg -version`、`ffprobe -version`。缺失时按系统和权限正常安装或向用户说明。不要索取 API Key。
2. 优先调用 Codex 自带的 `$skill-installer`，让它从 `ying676travel-eng/narration-visual-studio-skill` 的 `narration-visual-studio-v3` 子目录安装。该安装器支持 GitHub 仓库的 `--repo` + `--path`，默认目标为 `$CODEX_HOME/skills/narration-visual-studio-v3`（未设置 `CODEX_HOME` 时为 `~/.codex/skills/narration-visual-studio-v3`）。如果安装器不可用，可从当前 Public 仓库下载该子目录，完整放入同一目标目录；不要覆盖已有同名目录，先检查并备份。
3. 在**已安装的 Skill 目录**运行 `npm ci`。不要依赖原项目的 `node_modules`；它不随仓库分发。Node 依赖固定为 GSAP 3.14.2、HyperFrames 0.8.185、Playwright 1.61.1、sharp 0.35.5。
4. 安装下面的官方 HyperFrames 技术指导。若用户环境限制网络或第三方 Skills 安装，先说明阻碍，不能假称已安装。
5. 在 Skill 目录执行 `npm test` 和 `npm run hf -- doctor --json`；doctor 要逐项看本地 HTML/浏览器所需条件，不能只看退出码。核对七个 `styles/<name>/frame.md`、`upstream/FRAME.md`、`upstream/frame-showcase.html` 均存在。请在 Codex **下一轮对话**确认 `$narration-visual-studio-v3` 可见并可调用；当前对话的 Skill 列表未必即时刷新。
6. 向用户报告安装位置、依赖与风格检查结果。收到字幕后，再在用户选定的工作目录新建作品；不要把作品写进已安装 Skill 目录。

官方 Codex 安装器若报告“目标已存在”，不要删除原目录；先检查版本和本地改动，协商更新。若缺少 `SKILL.md`，通常是把仓库首页当作安装路径，应改为上述子目录。若 Node 版本不足，先升级 Node，再重试 `npm ci`。

## HyperFrames 技术指导

V3 制作流程原先要求阅读 HyperFrames Core、Animation、Creative 三套技术指导。HyperFrames 0.8.185 的官方安装命令现明确提示：这三个独立 Skill **已退役**，内容整合进 `/hyperframes` 的 `SKILL.md` 与 `references/`。不要把“找不到旧三个名字”误判为缺少能力。

**Codex：**优先用 Codex 自带的 `$skill-installer` 从官方仓库 `heygen-com/hyperframes` 的 `skills/hyperframes` 子目录安装到 `$CODEX_HOME/skills/hyperframes`。核对其中 `SKILL.md` 及 `references/` 可读。若已由 HyperFrames 插件提供同等官方文档，核对内容后可复用。

**其他支持的 Agent：**在用户的**作品工作目录**（不是 V3 Skill 安装目录）执行官方 HyperFrames CLI：

```bash
node <V3-skill-dir>/node_modules/hyperframes/bin/hyperframes.mjs skills update
```

该命令会按官方机制安装或更新 HyperFrames 当前核心 Skills（包括 `/hyperframes`），也可能更新工作目录里已有的 HyperFrames Skills。执行前检查目标目录和已有内容；之后确认当前 Agent 能发现 `/hyperframes/SKILL.md` 与相关 `references/`。如无法确定目标 Agent 的发现机制，按其官方说明安装，不猜路径。安装后再读 `/hyperframes` 的技术、动效和视觉参考文档，并核对实际 CLI `--help`。本发行包不复制或重新实现 HyperFrames。

## 其他 Agent

WorkBuddy、Claude Code、Cursor 等若支持 Agent Skills，请先让其检查自身的官方 Skill 发现与安装机制，再将**完整 Skill 子目录**放到该机制要求的位置，并验证 `SKILL.md` 被识别。不要把 Codex 的 `~/.codex/skills` 路径照搬给其他 Agent。HyperFrames CLI 官方支持多种 AI 工具的 Skills 安装，但本项目尚未在 WorkBuddy 的独立新会话中验证；该验收由发行者另行完成。无法确认安装目录或权限时，向用户明确报告，不猜测。

## 使用时的路径

Skill 代码和 Node 依赖位于已安装的 Skill 目录。作品目录位于用户工作区。Agent 可从工作区调用 `<skill-dir>/scripts/new_project.py` 创建作品；运行 HyperFrames、浏览器检查时，在 Skill 目录启动命令并给出作品的绝对路径。作品自身只引用其 `assets/` 下的本地资源，不依赖原 Private 仓库或本机旧样片。
