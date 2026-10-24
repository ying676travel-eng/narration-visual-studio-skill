---
name: narration-visual-studio-v3
description: 将口播字幕制作成内容驱动的 16:9 动态讲解；先策划整篇叙事与页面，再设计视觉和语义动效；支持七套官方风格、可信本地风格导入、可定位 SVG/GSAP 动效、HyperFrames 本地检查和无声视频。
---

# Narration Visual Studio V3

## 开始前

读本 Skill 目录的 `README.md`、`references/deck-storytelling.md`、`references/creative-direction.md`、`references/motion-language.md`、`references/visual-qa.md`、`references/style-import.md`、`references/composition-system.md`、`references/hyperframes-runtime.md` 和选定风格 `styles/<name>/frame.md`。用户未指定时使用 cartesian。内置七套：cartesian、code-editorial、blockframe、broadside、cobalt-grid、daisy-days、editorial-forest。每套都必须通读自己的 `styles/<name>/upstream/FRAME.md` 全文、打开同目录官方 showcase 核对视觉，再按 `frame.md` 的本地字体与中文适配说明执行；JSON token 块不能替代完整规范。Code Editorial 另读 `references/code-editorial-execution.md`。导入风格须来自可信本地 HTML，并先按导入规范检查。用户授权整轮制作时，自主完成规划、设计、检查、修复和样片交付，不逐步寻求批准。内部检查通过不代表用户已完成视觉验收。

V1/V2 和旧案例只读。新作品放 `projects/<episode>/`。不要上传字幕或素材，不调用 publish/cloud/付费 API，不自动合并分支。不把没有时间码的文本说成精确同步作品。

## 制作闭环

1. **准备输入与环境。** 按本 Skill 目录的 `README.md` 安装固定 npm 运行依赖 `npm ci`；不额外安装 HyperFrames Agent Skills，核对 Node>=22、Python 3、Chrome；仅导出 MP4 时再核对 FFmpeg/FFprobe。`npm run hf -- doctor --json` 中可选语音/音乐/Docker不是本地渲染必需；逐项核对核心条件，不能只看 doctor 进程退出码。使用 `scripts/prepare_input.py` 规范化字幕，完整阅读原文及警告。选段须在 `source-map.md` 写明原始起止、偏移、cue ID；保留事实，重复录制不擅自合并。用 `scripts/new_project.py` 建独立作品目录并选定风格；导入风格时先运行 `inspect_reference.py` 生成独立风格目录，再把目录路径传给 `--style`。不要覆盖已有作品。用户用自然语言描述需求即可，由 Codex 执行，无需手动编辑源码。
2. **先策划整篇，再分页。** 从头到尾读完时间字幕，提炼整片要表达什么、章节如何推进、主要转折和结尾落点；在 `scene-plan.md` 开头用简短段落记录。随后按认知任务切页：话题或理解模型改变时通常换页；同一概念能在一幅画面中逐步建立或变化时，留在本页逐步揭示；一页承担过多不同问题时拆开，关键观点可短页。不要按字幕条数或固定页长平均切分。观点/转折约 6–12 秒、普通解释约 10–22 秒、复杂流程或比喻可更长，只作回看提示，不是配额。逐页写绝对起止、cue IDs、页面任务/信息收获、关系和关键揭示时刻，并用现有 `scenes.json` 字段保存机读分镜，不破坏既有字段契约。完整规则见 `references/deck-storytelling.md`。
3. **确定整片视觉节奏，设计每页。** 在 `visual-storyboard.md` 开头写所选风格、字体和配色角色、标题/留白/线条语言，以及整片如何交替使用大字、图形、疏密和不同表达方式。其后逐页标注主张、阅读焦点、构图、图形如何解释内容、精简屏幕文案、出现顺序与字幕对应关系、素材来源或“示意”标识。页面形式随任务改变，不设版式配额；保持同一设计语言，同时避免连续重复同一构图。风格包里的 Frame Treatments 是**可选库，不是逐页配额**：可以选用、重复或按内容创作专属图解，但每页都须遵守所选官方规范的地面色、字体角色、线条/边界和强调规则，不把 Code Editorial 的规则套给其他风格。若一页换掉关键词后仍与别的页同构，就是模板化，应换结构而不是换字。解释复杂概念时用渐进构建（节点按口播顺序长出、连接线描出、同一对象换状态），末帧必须稳定成可读静帧；没有解释功能的装饰 SVG 删掉。HTML/CSS Grid/Flex 优先搭页面骨架，SVG/CSS 绘制内容图形；整页 SVG 合适时仍可用。沿用 `references/creative-direction.md`、`references/composition-system.md` 与选定风格的约束。**既有作品只用于判断"哪些方法管用"，不得复制其 DOM、CSS、动画时序或中文文案。**
4. **先校准不同页面，再扩展。** 完整分镜和视觉方向写完后，挑 2–3 张要求明显不同的页面（如观点/大标题、复杂类比/流程、结构/对比）做成真实浏览器画面。检查字体、版式、主视觉尺度、内容专属图解和构图差异；若仍普通、凌乱或同质，先修正设计方法，再用于全片。这是内部迭代，不设正式 Gate，也不要求用户中途批示。
5. **实现同步画面。** 实现前阅读本 Skill 的 `references/hyperframes-runtime.md`，必要时用锁定版 CLI 的 `--help` 或 `docs` 核对接口；不读取外部 HyperFrames Skill。生成 `index.html`：独立根 `data-composition-id`、1920×1080、`data-duration`、`data-fps=25`；`section.clip` 使用 `data-start`/`data-duration`；唯一暂停的 GSAP timeline 注册到 `window.__timelines` 的同名键。元素时间由 GSAP 编排，不能使用 V2 `data-at` 当框架接口。正反 seek 都须稳定，素材本地化，无网络字体依赖。
6. **检查真实画面并修复。** 运行 `audit_project.py` → HyperFrames lint → `check --json --snapshots`（`browserSkipped=false`）→ snapshot → `browser_qa.mjs`。用浏览器截图或全页联系图逐页查看实际画面，并整体回看视觉节奏；检查每页的主要状态、场景开头、关键 reveal 后、结束和边界，1920×1080 与 1280×720、字体回退及随机往返 seek。看清遮挡、裁切、过小文字、风格漂移和语义错误；发现问题先修画面再重跑相关检查。**字体必须用三重证据确认真的生效**，不能只看 CSS 或 `document.fonts.check()`：① 监听网络响应，字体文件全部 200 且无外网请求；② `document.fonts` 中目标 family/weight 的 `status === 'loaded'`；③ 用 canvas `measureText` 对比加字体与纯 fallback 的实际宽度差异，中文另测回退字形。精简记录缺陷、修复和仍存在的问题。
7. **可选导出静音视频。** 仅用户要求 MP4 时，用固定版本 HyperFrames `render --fps 25` 本地导出；用 ffprobe 验证 H.264、1920×1080、25fps、无音轨、时长误差不超过 1 帧。交付审阅样片；技术检查通过不等于用户审美验收。
8. **交付可检查的作品。** 提供可直接查看的 HTML 和必要截图。结果记录与本轮范围相称，说明检查证据、素材真实性与未解决事项；不以过程文档数量替代成品质量。最终视觉验收由用户决定。

## V3.1 构图与图形底线

先确定唯一主视觉和阅读路径，再按语义组织标题区与图形区。统一内容安全边距、对齐轴、间距节奏和字体角色；中文按词义换行。删除重复结论、游离脚注、干扰文字的装饰和无意义连线。七种风格共用秩序原则，不共用固定版式。已有作品只修必要布局，保持字幕、时码和动画引擎。

屏幕是给观众看的解释，不是全文字幕。观点可用巨型排版；流程用空间路径；因果用建构或状态变化；系统用节点关系；复杂抽象概念用内容专属多部分 SVG。图形必须忠于口播：无真实数据不画假统计，无真实产品素材不造假 UI。动作解释内容，结束后保留可读状态，不用背景持续运动争夺焦点。

## 风格资源复用

风格包可自带授权资源（如 `styles/code-editorial/fonts/` 的 WOFF2 与 OFL 许可）。`new_project.py` 在创建项目时把它们复制到新项目的 `assets/fonts/`，因此作品**只引用自己目录下的相对路径**：不指向其他作品的字体，不请求远程字体服务，不把上一部成品的 CSS 当资源库。`@font-face` 一行一个文件，声明真实存在的字重；展示层按风格规范的推荐字重排字（Code Editorial 用 400）。

风格包的 `upstream/` 是设计权威原件（只读），`frame.md` 是机读 token 层，两者分工不可互换：用 YAML 原始规范覆盖 `frame.md` 会让 `load_tokens()` 与新项目初始化直接失效。

## 输出

`source.*`、`input.json`、`source-map.md`、`scene-plan.md`、`scenes.json`、`visual-storyboard.md`、`frame.md`、`index.html`、`meta.json`、`assets/`（含 `fonts/` 等本地资源）、`qa-report.md`、`review/`；视频放在 `renders/`（默认不入 Git）。选定的 `frame.md` 是该作品设计快照；未来换风格须重新创作构图，同时保持事实和字幕时间。
