# Code Editorial 执行方法 · 从规范到一页真实画面

本文件不重复规范，只记录**把官方规范真正落到画面**时的决策顺序、换算和已知坑。
设计权威永远是 [`../styles/code-editorial/upstream/FRAME.md`](../styles/code-editorial/upstream/FRAME.md)；
本文件是执行层补充。其他风格（cartesian / blockframe）不适用本文件的具体数值。

## 1 · 阅读顺序

1. 通读 `upstream/FRAME.md` 全文，不要只读 token 段。字号阶梯、Frame Treatment、Do/Don't、自检项都在散文里。
2. 打开 `upstream/frame-showcase.html` 看四种研究页实际长什么样，建立"什么算对"的视觉基准。
3. 再看 `frame.md` 的 ```json``` 块 —— 它只是 `load_tokens()` / `new_project.py` 的机读契约，不是设计说明。
4. 最后才写 HTML。跳过 1、2 直接看 token，做出来的一定是"配色对了但气质不对"。

## 2 · 容器法与字号换算

`#root`（或每个 `.clip`）设 `container-type: size`，所有版面尺寸用 `cqw`/`cqh`，**不用 `vw`**。
1920×1080 下 `1cqw = 19.2px`，`1cqh = 10.8px`。

| 角色 | 规范值 | 1920 下实际 | 用途 |
|---|---|---|---|
| `display-cover` | 9.9cqw / 0.98 / −0.028em | 190px | 封面、极短主张（≤3 词） |
| `display` | 7.3cqw / 1.02 / −0.022em | 140px | 观点句（4–6 词） |
| `headline` | 4.6cqw / 1.06 / −0.018em | 88px | 常规标题（7 词以上） |
| `quote-pull` | 5.0cqw / 1.12 斜体 | 96px | 引语、定义、立场 |
| `number-hero` | 9.4cqw / 0.95 | 180px | 真实数字（必须来自字幕） |
| `lead` | 2.08cqw / 1.5 | 40px | 一句导语 |
| `body` | 1.5cqw / 1.5 | 29px | 正文，**1.4cqw 是可读地板** |
| `card-title` | 2.3cqw / 1.25 / 500 | 44px | 卡片标题 |
| `kicker` | 1.46cqw / 0.16em 大写 mono | 28px | 眉标，带珊瑚 ✱ |
| `caption` / `mono-label` | 1.35cqw mono | 26px | 页码、状态、索引 |

标题按长度选档，不要靠 `font-size` 微调硬塞：≤3 词用 `display-cover`，4–6 词用 `display`，
7 词以上用 `headline`；整块宽度上限 `78cqw`。中文标题很少能到 9.9cqw —— 汉字同字号视觉重量
远大于拉丁字母，通常降一到两档才不闷。

## 3 · 每页先定"看什么"，再定"长什么样"

逐页用一句话写"看到这页结束时，观众应该理解___"，再从七种关系里选一种承载它：
主张 / 对比 / 因果 / 顺序 / 系统 / 证据 / 比喻。关系决定构图，**不是先挑 Treatment 再塞内容**。

六种 Frame Treatment（Cover / Statement / Code Surface / Number / Pull-quote / Closing）
是**可选库**，不是配额。一部片子可以不出现 Code Surface，也可以出现两次；一页也可以是
规范没写的自创图解 —— 只要守住三色层、hairline、单 coral 和字体角色。

判断标准很简单：把这页的关键词换掉以后，如果它和别的页看起来还是同一个骨架，那就是模板化，
需要换构图（左右分区 / 满幅 / 单焦点 / 密集分层 / 竖向序列）。

## 4 · 让图形真的解释内容

- **优先内容专属图解**：讲文件夹结构就画树，讲读写关系就画箭头方向，讲"SOP 打包"就画把散落步骤
  收进一个容器。不要用通用装饰件充当解释。
- **渐进构建**：同一画面按口播顺序长出，而不是一次全出。三种可靠做法：①节点逐个 `data-reveal`；
  ②连接线 `data-draw` 逐段描出；③同一对象换状态（虚线→实线、灰→墨、卡片→收进容器）。
- **收尾保持可读**：最后一个揭示之后画面必须稳定成一张能看懂的静态图，禁止背景持续运动抢注意力。
- **不造假**：没有的真实数据不画统计图、不写假文件名/假接口；示意性的代码面必须标 `示意`。

## 5 · 颜色配额

cream 打底，tile / tile-strong 做半档分组，ink 说话，**coral 每页只出现一次**（✱ 眉标、一个 callout、
或一条 1px 珊瑚线，三选一）。navy 只给代码/终端面，不当第四品牌色。teal/amber 只在代码面里当语法色。
不要把 coral 拿去写标题或整段正文 —— 这是最常见的走样。

高度上限：1px hairline（cream 上 ink@12%，navy 上 cream@14%）+ 最多一个极轻阴影；
不要重投影、发光、内容渐变、倾斜。圆角只用 6 / 8 / 12px 和 9999px 胶囊。

## 6 · 中文混排

- 中文不要交给裸 `serif` / `sans-serif`：展示层写 `"EB Garamond","Songti SC","Noto Serif CJK SC",serif`，
  正文写 `"Inter","PingFang SC","Noto Sans CJK SC",sans-serif`。EB Garamond 没有汉字，
  屏幕上看到的汉字一定来自回退字体，作品说明里不要写成"用了 Garamond 排中文"。
- 按语义断行（`把本地文件夹 / 接进项目空间`），不拆词、不留孤字、不人为拉字距。
- 汉字不要靠缩小字号塞进一行。超了就改短文案或换行，最小不低于 `1.4cqw`。

## 7 · 字体真实性验证（三重，缺一不算）

只看 CSS 或 `document.fonts.check()` 会被"声明了但没加载"骗过去。三个独立信号：

1. **网络**：监听 `response`，`*.woff2` 必须全部 200，无 404/无外网请求。
2. **FontFace**：`document.fonts` 里对应 family/weight 的 `status === 'loaded'`。
3. **实际字形**：用 canvas `measureText` 量同一串拉丁字符，加字体与纯 fallback 宽度必须不同；
   中文再用 `measureText` 确认命中的是回退字体而不是缺字方框。

## 8 · 已知布局坑（都踩过）

- `.split{height:100%}` 叠加 `top/bottom` 定位会把 `.body-area` 撑到 1080px，图形被挤没；
  去掉 `height:100%`，给 `flex` 子项加 `min-height:0`。
- 绝对定位子元素**不吃**父级 `padding`；要用 `margin` 或给容器留内层。
- HTML 节点与 SVG 连线坐标不同步：容器加 `aspect-ratio`，或 SVG 用 `preserveAspectRatio="none"`
  + 百分比坐标对齐 HTML 的百分比定位。
- 静态装饰 SVG（箭头、虚线）会从 0 秒就可见；要把它们包进 `<g data-reveal="对应秒数">`。
- `margin-top:auto` 只在 flex 父级有效；父级是 grid/block 时静默失效，改用 flex 列或显式间距。
- `cqw` 在非 `container-type` 祖先下会退化成视口单位，字体突然变得巨大或极小。

## 9 · 自检顺序

1. 缩到 1280×720 看轮廓：主视觉还认得出来吗？有没有三处同等抢眼？
2. 回 1920 看成组：标题、图形、说明是否在同一对齐轴？有没有重复结论和游离英文标注？
3. 逐页真截图，看每一个关键揭示时刻，而不是只看最终帧。
4. 最后才跑 `audit_project.py` / lint / seek 回归 —— 脚本通过不等于画面成立。
