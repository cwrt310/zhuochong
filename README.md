# -zhuochpng

## 小巴桌宠

原生 v2 桌宠文件位于 [`work/xiaoba/native`](work/xiaoba/native)：`pet.json` 和 `spritesheet.webp`。图集为 8 列 × 11 行，单格 192×208，包含九种动画状态及十六个注视方向。

Windows 上运行 `work/安装小巴.ps1`，会将小巴复制到当前用户的 `.codex/pets/xiaoba`（设置了 `CODEX_HOME` 时使用该目录），并在 `config.toml` 中选中、显示小巴。首次安装时脚本会备份原配置为 `config.before-xiaoba.toml`，后续运行不会覆盖这份备份。安装后如未立即显示，在 Codex 的 Settings > Pets 中刷新。

请先下载并解压整个仓库，保留 `work/Update-XiaobaConfig.ps1`、安装脚本与 `work/xiaoba/native/` 的相对位置，然后在仓库根目录运行：

```powershell
& '.\work\安装小巴.ps1'
```

分享给别人时，可以从仓库主页的 **Code → Download ZIP** 下载当前版本，将 ZIP 发给对方并让对方完整解压。`outputs/小巴-全部素材与工程-20261022.zip` 是早期素材备份，不包含后来完成的原生安装文件和这次更新的安装脚本。

安装脚本支持带注释或引号的 `[desktop]` 表、缩进和带引号的设置项，以及没有末尾换行的配置。其他设置和多行字符串会保留；重复安装不会重写相同配置。配置通过同目录临时文件替换，首次备份仍保留。如果配置使用根级 `desktop.xxx` 或内联表写法，脚本会在复制宠物前提示改为 `[desktop]` 表；重复表、重复设置项及不支持的多行目标值也会停止安装。

开发者可用 Python 3.11+ 运行安装回归测试：`python -m unittest discover -s tests -v`。测试只操作临时目录，用 `tomllib` 检查配置结果，并检查首次备份与重复安装行为。默认使用 Windows PowerShell 5.1；设置 `XIAOBA_TEST_POWERSHELL=pwsh` 可切换 PowerShell 7。测试进程单独使用 `-ExecutionPolicy Bypass` 来执行临时复制的本项目脚本，不修改系统执行策略。安装本身不依赖 Python。

[`outputs/xiaoba/completed-contact.png`](outputs/xiaoba/completed-contact.png) 是九种动作的总览，可用 `python work/render_xiaoba_contact.py work/xiaoba/native/spritesheet.webp outputs/xiaoba/completed-contact.png` 重新生成。图集边缘的绿色残影和检查成果动作中的多余碎片已经修复。用户要求直接安装和提交，本项目尚未执行最终完整图集质量校验。
