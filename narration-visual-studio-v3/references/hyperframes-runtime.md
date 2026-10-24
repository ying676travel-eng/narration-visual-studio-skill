# HyperFrames 运行约定 · V3 固定版本

本文件只记录 Narration Visual Studio V3 制作讲解画面需要的运行接口。内容依据 npm 锁定的 **HyperFrames 0.8.185** 自带 `dist/docs/{compositions,data-attributes,gsap,rendering}.md`、该版本 CLI 的 `--help`，以及 [HyperFrames 官方核心文档](https://github.com/heygen-com/hyperframes/blob/main/packages/core/docs/core.md)。上游代码和文档采用 Apache-2.0，许可见 `../licenses/HyperFrames-Apache-2.0.txt`。这里是 V3 的窄范围适配说明，不是复制或安装 HyperFrames Agent Skills；接口有疑问时先查本地 `npm run hf -- <命令> --help` 或 `npm run hf -- docs <主题>`。

## 一部作品的 HTML 契约

- 用本 Skill 的 `scripts/new_project.py` 初始化作品，不调用 `hyperframes init`。锁定版 `init --help` 明示它会检查 AI Skills，`--skip-skills` 暂时无效；这与单 Skill 安装目标不符。
- `index.html` 放一个根节点：唯一的 `data-composition-id`（例如 `main`）、`data-width="1920"`、`data-height="1080"`、与字幕总时长一致的 `data-duration`、`data-fps="25"`。V3 的 `audit_project.py` 会核对尺寸、时长和场景数。
- 每页用独立、稳定 `id="scene-<scene_id>"` 的 `section.clip`，写绝对秒数 `data-start` 和本页秒数 `data-duration`；内部普通元素使用 `id="el-<scene_id>-<名称>"`，全页 DOM ID 唯一。场景须连续覆盖整段字幕；与 `scenes.json` 和原 cue ID 对齐。`data-track-index` 可用于 Studio 时间轴分组，不决定画面层级；前后遮挡由 CSS `z-index` 决定。
- `class="clip"` 是本项目的布局和检查约定。HyperFrames 依据时间属性管理 clip 的出现区间；不要再用 V2 `data-at`，也不要靠手工 `setTimeout` 推进场景。

## 一条可任意定位的动画时间线

在加载**本地** `assets/gsap.min.js` 后，为根节点创建一条暂停的 GSAP timeline，并以相同 ID 注册；动画位置使用从整片 0 秒算起的绝对秒数：

```html
<script src="./assets/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  tl.fromTo('#idea', { autoAlpha: 0, y: 24 },
    { autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 1.2);
  window.__timelines.main = tl;
</script>
```

`main` 必须与根节点 `data-composition-id` 一致。多页时继续把各元素的 tween 排进这条 timeline，按字幕语义安排 reveal；不建立额外会自行播放的 timeline。HyperFrames 负责运行和渲染时的时间定位，timeline 保持 `paused: true`。初态与终态明确、动作有限且可回退；避免独立 CSS 动画、随机数、常驻 RAF 或仅在顺序播放后才成立的 DOM 修改。画面在任意时间点都应由该时间点直接得到，同一时间从前后反复 seek 的截图必须一致。让最后一个解释状态留下可读停留。

直接打开 HTML 时，本项目还需提供本地预览控制：播放、暂停、前后定位以及 `window.nvs.seek(seconds)`。`browser_qa.mjs` 使用这个方法做往返定位、截图和确定性检查。预览驱动应把秒数限制在 `[0, data-duration]`，对同一时刻设置 GSAP 时间线，并按 `data-start`/`data-duration` 显示恰好一个场景；到片尾保留最后一页。若同一 HTML 也交给 HyperFrames 运行，应避免预览驱动与框架同时控制 clip（已有作品只在本地直接预览模式启用该驱动）。把只服务于直接打开 HTML 的 `requestAnimationFrame` 播放控制放在单独的本地 `assets/preview.js`，不要写进 `index.html` 的动画脚本；锁定版 `lint` 会把后者视为非确定性的渲染动画。

## 资源、检查与可选导出

字体、图像、脚本放作品自身 `assets/`，HTML 用相对路径；GSAP 从本 Skill 的 npm `node_modules/gsap/dist/gsap.min.js` 复制到作品 `assets/`，保留原文件的版权/许可标头。风格字体由 `new_project.py` 复制到作品 `assets/fonts/`。不依赖 CDN、原开发仓库、其他作品或外部 HyperFrames Agent Skill。HTML 正常制作不需要音轨；用户只要 HTML 时不导出 MP4。

在**已安装的 V3 Skill 目录**运行以下命令，`<作品绝对路径>` 指向用户工作区；先用命令的 `--help` 核对实际参数：

```bash
python3 scripts/check_project.py <作品绝对路径> --mode quick
python3 scripts/check_project.py <作品绝对路径> --mode full
npm run hf -- snapshot <作品绝对路径> --at 0,2,4
node scripts/browser_qa.mjs <作品绝对路径>
# 局部修复期间：node scripts/browser_qa.mjs <作品绝对路径> --scene <scene_id>
# 或：node scripts/browser_qa.mjs <作品绝对路径> --range 12:20
```

`check_project.py` 把完整的 audit、lint 和 check JSON 保存在作品 `review/checks/`，终端只显示问题摘要；`--mode check` 可在局部修复时做不带快照的浏览器检查。它不会清理 `.hyperframes`，同一作品的并发检查会串行执行；若 CLI 报 EEXIST，查看保存的 stderr 和具体路径后再处理，不反复盲跑。`lint` 检查结构，`check` 要真正运行浏览器（结果中的 `browserSkipped` 必须为 `false`），`snapshot` 和 `browser_qa.mjs` 提供真实画面证据。局部 QA 证据单独放在 `review/partial/`，不能代替最终全量 QA。检查每页开头、关键揭示、片尾、边界和反向 seek；脚本通过不能代替逐页视觉检查。单文件 V3 的嵌套 `section.clip` 可能收到 `nested_structure_needs_subcomposition` 建议性警告；若运行、画面与定位均通过，记录警告即可，不为了消除它重构已验收的场景结构。`npm run hf -- doctor --json` 用于核对本地环境，语音、音乐和 Docker 等可选项失败不等于本项目 HTML 流程失败。

仅用户要求静音 MP4 时，使用 `npm run hf -- render <作品绝对路径> --fps 25 -o <输出绝对路径>`；锁定版 CLI 的 `render --help` 明确接受 25fps。随后用 `scripts/verify_video.py` 与 `ffprobe` 核对 H.264、1920×1080、25fps、无音轨及一帧内的时长误差。V3 的语义分镜、视觉风格和无声约束优先于 HyperFrames 通用创作示例。
