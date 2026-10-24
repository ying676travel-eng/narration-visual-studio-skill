# 上游原始规范 · HyperFrames Code Editorial Frame Pack

本目录是**设计权威原件**，只读。不要编辑；本风格包的本地适配写在上一级
[`../frame.md`](../frame.md)，实际执行方法见
[`../../../references/code-editorial-execution.md`](../../../references/code-editorial-execution.md)。

## 来源

- 仓库：https://github.com/heygen-com/hyperframes
- 固定 commit：`934c88bac8cf6dc37db07cecf3bd0b58314c9921`
- 上游路径：`skills/hyperframes/assets/frame-presets/code-editorial/`
- 许可：Apache-2.0（源仓库声明）

## 文件

| 文件 | 作用 |
|---|---|
| `FRAME.md` | 权威规范：token、两套字号阶梯、容器法、六种 Frame Treatment、Do/Don't、上屏前自检 |
| `frame-showcase.html` | 四种研究页的可视参考（视觉参考，不是逐页模板） |

## 字体

`../fonts/` 内是上游 preset 随包提供的授权字体，与 `FRAME.md` 的 Known Gaps 一致：

- `EBGaramond-400.woff2` / `EBGaramond-700.woff2` — SIL Open Font License（`OFL-eb-garamond.txt`）
- `Inter-400.woff2` / `Inter-700.woff2` — SIL Open Font License（`OFL-inter.txt`）
- `JetBrainsMono-400.woff2` / `JetBrainsMono-700.woff2` — SIL Open Font License（`OFL-jetbrains-mono.txt`）

展示层只按 400 字重排字（700 会上屏成过重的粗体，脱离风格）；700 文件保留备用。
EB Garamond 只覆盖拉丁字形，中文回退到本机 Songti SC（展示）/ PingFang SC（正文），
字体文件本身不含汉字，作品里不得声称含汉字。

## 与上一级 frame.md 的分工

- `FRAME.md`（本目录）：完整设计权威，AI 必须先通读再动手。
- `../frame.md`（上一级）：` ```json ` token 块是 `audit_project.load_tokens()` 与
  `new_project.py` 要求的机读契约，**不能**用 YAML 版 `FRAME.md` 覆盖它；其余章节是中文精简说明。
