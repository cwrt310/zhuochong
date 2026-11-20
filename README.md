# -haocai

## 小巴桌宠

原生 v2 桌宠文件位于 [`work/xiaoba/native`](work/xiaoba/native)：`pet.json` 和 `spritesheet.webp`。图集为 8 列 × 11 行，单格 192×208，包含九种动画状态及十六个注视方向。

Windows 上运行 `work/安装小巴.ps1`，会将小巴复制到当前用户的 `.codex/pets/xiaoba`（设置了 `CODEX_HOME` 时使用该目录），并在 `config.toml` 中选中、显示小巴。首次安装时脚本会备份原配置为 `config.before-xiaoba.toml`，后续运行不会覆盖这份备份。安装后如未立即显示，在 Codex 的 Settings > Pets 中刷新。

[`outputs/xiaoba/completed-contact.png`](outputs/xiaoba/completed-contact.png) 是九种动作的总览，可用 `python work/render_xiaoba_contact.py work/xiaoba/native/spritesheet.webp outputs/xiaoba/completed-contact.png` 重新生成。图集边缘的绿色残影和检查成果动作中的多余碎片已经修复。用户要求直接安装和提交，本项目尚未执行最终完整图集质量校验。
