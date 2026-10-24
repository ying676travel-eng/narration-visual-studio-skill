# Daisy Days 来源与字体

- 固定上游：heygen-com/hyperframes `934c88bac8cf6dc37db07cecf3bd0b58314c9921`，`skills/hyperframes/assets/frame-presets/daisy-days/`。
- `FRAME.md` 与 `frame-showcase.html` 为该提交原始全文，保留作设计依据；上游仓库许可请见 [LICENSE](https://github.com/heygen-com/hyperframes/blob/934c88bac8cf6dc37db07cecf3bd0b58314c9921/LICENSE)。官方 showcase 原页引用 Google Fonts，仅供参考；本地作品不能依赖该远端请求。
- [Fredoka 600 Latin WOFF2](https://fonts.gstatic.com/s/fredoka/v17/X7nP4b87HvSqjb_WIi2yDCRwoQ_k7367_B-i2yQag0-mac3OLyX8EemKttxNbikt.woff2)、[Quicksand Latin variable WOFF2](https://fonts.gstatic.com/s/quicksand/v37/6xKtdSZaM9iE8KbpRA_hK1QNYuDyPw.woff2)：Google Fonts 官方 CDN，授权分别见 [OFL-fredoka.txt](../fonts/OFL-fredoka.txt)、[OFL-quicksand.txt](../fonts/OFL-quicksand.txt)；许可证来自 Google Fonts 官方仓库。
- [ZCOOL KuaiLe TTF](https://github.com/google/fonts/blob/main/ofl/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf)：Google Fonts 官方仓库，授权见 [OFL-zcool-kuaile.txt](../fonts/OFL-zcool-kuaile.txt)。它仅用于中文展示字，圆润卡通形状更接近 Fredoka 的视觉角色。
- 官方规范在 Known Gaps 中建议 ZCOOL XiaoWei 作中文展示字、Yozai 作正文。这里为保留画面圆润感改用 ZCOOL KuaiLe 作展示字；正文用系统字体栈，不声称逐字还原原组合。跨机器中文正文形状会略变。
- `mono_font` 机读字段为现有工具契约；Daisy Days 不引入第三套等宽字体，若出现代码须另做可读性处理。
