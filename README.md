# Narration Visual Studio V3 Skill

把带时间码的 SRT/VTT 口播字幕制作成 16:9 动态讲解画面：先理解整篇内容，再分镜、设计图解与动画，交付可播放、可定位的本地 HTML；需要时可另导出无声 MP4。制作由支持 Agent Skills 的编程 Agent 完成，不需要用户写代码，也不需要大模型 API Key。

**一句话安装：**把本仓库链接发给 Codex，并说“帮我安装这个 Skill，检查运行环境和依赖，安装后验证七套风格”。Agent 的操作步骤见 [AGENT_INSTALL.md](AGENT_INSTALL.md)。Skill 本体在 [`narration-visual-studio-v3/`](narration-visual-studio-v3/)，不是仓库根目录。

七套风格：Cartesian（几何留白）、Code Editorial（代码与编辑排版）、BlockFrame（粗重色块）、Broadside（海报排版）、Cobalt Grid（蓝色网格）、Daisy Days（明快圆润）、Editorial Forest（绿色编辑风格）。每套都有完整官方 Frame Pack、字体或回退说明、来源记录。

示例请求：

> 使用 Narration Visual Studio V3 Skill，把我提供的字幕制作成动态讲解画面。选择 Code Editorial 风格，输出可播放 HTML，不导出 MP4。

输入应带 SRT/VTT 时间码。Agent 会在用户指定的工作目录生成独立作品文件夹，其中 `index.html` 与 `assets/` 一起保留即可本地预览；`scenes.json`、策划文件和 `review/` 用于检查。播放/暂停、前后时间定位由 HTML 时间线支持。字幕和作品留在用户本机，不会上传到本仓库。

## 环境

- **HTML 制作与检查：**Node.js 22+、npm、Python 3、Google Chrome；Node 依赖由 Skill 内的锁文件固定，Agent 运行 `npm ci` 安装。Python 核心脚本只使用标准库。
- **无声 MP4（可选）：**另需 FFmpeg 与 FFprobe。Chrome 或 FFmpeg 缺失时，由 Agent 按系统条件安装或说明限制。
- **单 Skill 安装：**只注册 `narration-visual-studio-v3`；HyperFrames CLI 和 GSAP 由 `npm ci` 作为运行依赖安装，制作所需技术约定已收在 V3 内部。无需另装 HyperFrames Agent Skills。

常见问题：如果 Codex 没识别新 Skill，检查安装目标是否为 `~/.codex/skills/narration-visual-studio-v3/SKILL.md`（或 `$CODEX_HOME` 对应路径），再开始新一轮对话；如果 `npm ci` 失败，先核对 Node 版本和网络；如果 Chrome 检查失败，确认已安装 Chrome 并让 Agent 重跑检查。字体中的中文部分使用本机字体回退，跨系统字形可能不同。

第三方来源与许可见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。本仓库不包含私人字幕、既有作品或原开发仓库历史。
