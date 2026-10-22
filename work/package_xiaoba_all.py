from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '小巴-全部素材与工程'
OUT = ROOT / 'outputs' / '小巴-全部素材与工程-20261022.zip'
entries = {}

def add_file(source, destination):
    source = Path(source)
    if not source.is_file():
        raise FileNotFoundError(source)
    if destination in entries:
        raise ValueError(f'Duplicate archive entry: {destination}')
    entries[destination] = source.read_bytes()

def add_tree(source, destination):
    source = Path(source)
    if not source.is_dir():
        raise FileNotFoundError(source)
    for path in sorted(source.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts:
            add_file(path, f'{destination}/{path.relative_to(source).as_posix()}')

add_tree(ROOT / 'outputs' / 'xiaoba', '01_预览与导出')
add_tree(ROOT / 'work' / 'xiaoba', '02_完整制作工程')
for path in sorted((ROOT / 'work').iterdir()):
    if path.is_file() and path.name != Path(__file__).name:
        if path.suffix.lower() == '.ps1':
            destination = f'03_辅助文件/未完成脚本草稿/{path.name}.txt'
        else:
            destination = f'03_辅助文件/{path.name}'
        add_file(path, destination)
add_file(Path(__file__), '03_辅助文件/package_xiaoba_all.py')

generated_root = Path('C:/Users/cwrt/.codex/generated_images')
history = {
    '01_主造型': '01a14f74-11c3-7eb1-a56f-abf730e8d295',
    '02_待机及修订历史': '01a14f88-be7c-7323-a3e4-1d08b9e957da',
    '03_旧版挥手': '01a14f88-ed05-7111-a642-0048f60d984c',
    '04_跳跃候选_未验收': '01a14f92-30eb-7ac2-bc0b-e10750b4eda5',
    '05_等待候选_未验收': '01a14f92-e594-7af2-8472-9546b9c1f06d',
    '06_新版挥手': '01a14f99-28f4-7772-82d6-ed77763ffa1f',
}
history_files = []
for label, directory in history.items():
    folder = generated_root / directory
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    for path in sorted(folder.rglob('*')):
        if path.is_file() and path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}:
            name = f'04_生成原图与历史版本/{label}/{path.relative_to(folder).as_posix()}'
            add_file(path, name)
            history_files.append({'category': label, 'file': name, 'generation_id': directory})

pipelines = {
    'hatch-pet_本次实际使用的提取与检查脚本': Path('C:/Users/cwrt/.codex/skills/hatch-pet/scripts'),
    'work-pets_0.1.6_完整验证工具': Path('C:/Users/cwrt/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/scripts'),
}
for label, source in pipelines.items():
    if not source.is_dir():
        raise FileNotFoundError(source)
    for path in sorted(source.glob('*.py')):
        add_file(path, f'05_提取组装与校验工具/{label}/{path.name}')

readme = '''# 小巴 · 全部素材与制作工程

打包日期：2026-10-22（北京时间）

这是现有全部素材、已生成动作及历史版本、制作工程、提示词、透明帧、预览和检查报告的汇总包。
**当前不是可直接启动的桌宠安装包，尚未安装到任何桌宠应用。**

## 收到后先看这些

- `01_预览与导出/waving-v2.gif`：当前推荐的新版挥手。
- `01_预览与导出/waving-comparison.gif`：左旧版、右新版的动作对比。
- `01_预览与导出/waving-v2-frames.png`：新版四帧检查图。
- `01_预览与导出/waving-v2-strip.png`：透明背景的四帧素材条，每帧 192×208。
- `01_预览与导出/idle-preview.gif`：待机眨眼预览。
- `01_预览与导出/main-look.png`：去掉绿幕后的主造型。
- `01_预览与导出/reference.jpg`：用户提供的原始参考图。

GIF 可直接作为文件发送或用图片查看器打开。ZIP 需要先解压；解压本身不会安装桌宠。

## 制作状态

| 项目 | 状态 |
| --- | --- |
| 主造型 | 已生成并采用，以右侧白发蓝眼角色为主要参考 |
| 待机 | 六帧；基础提取和结构检查通过 |
| 新版挥手 | 四帧；同一只手挥动、另一只手持球，配合笑容、眨眼和歪头；基础检查和独立顺序帧视觉复查通过 |
| 旧版挥手 | 保留用于对比；用户认为太呆，且曾出现挥手的手换边，不是推荐版本 |
| 跳跃、等待 | 已生成候选原图，尚未完成提取与验收 |
| 向右跑 | 多次生成遇到网络错误，未产出可用原图 |
| 向左跑、受挫、工作、检查成果 | 已有提示词和布局模板，尚无完成的动作图 |
| 四个方向锚点、十六个注视方向 | 已有规划、提示词和布局模板，尚未生成 |
| 完整精灵图、原生安装包 | 尚未完成 |

用户最新要求是先把挥手做好，其他动作暂缓。新版挥手整体是温柔的小幅挥手。
新版独立视觉复查基于顺序帧图，没有独立评估实际播放节奏；GIF 导出已核对含四帧，时长依次 140、140、140、280 毫秒。
单个动作的基础检查通过，不代表完整桌宠已完成最终验证。

## 目录说明

1. `01_预览与导出`：方便直接查看、发送和使用的素材，以及原有设计说明。
2. `02_完整制作工程`：本次制作工程完整副本。`decoded` 是已采用/候选动作原图；`qa` 包含透明帧、检查报告和过程笔记；`prompts` 包含已用及尚未执行的提示词；`references` 包含参考图与布局模板。
3. `03_辅助文件`：过程辅助脚本、对比图和制作说明。安装脚本只是未完成草稿，按 `.ps1.txt` 保存供阅读；它缺少最终验证包，不能作为成品安装程序使用。
4. `04_生成原图与历史版本`：与小巴相关、仍然存在的所有生成原图，包括未选中的修订版。历史版本可能有裁切、姿态过近等问题，应以新版挥手和已采用主造型为准。
5. `05_提取组装与校验工具`：本次相关的原版 Python 工具，供懂制作流程的人继续加工；不是桌宠运行程序。
6. `文件清单_SHA256.json`：包内文件清单、大小和 SHA-256；`生成原图索引.json` 标明各组生成原图。

工程报告和辅助脚本保留了制作时的本机路径，其他电脑继续制作时需改成解压后的实际路径。
现有旧 ZIP 的内容已作为预览/工程文件纳入，未重复嵌套旧压缩包。

## 后续制作参考

最新采用的挥手提示词是 `02_完整制作工程/prompts/waving-polish-v2-two-ref.md`。
对应参考为 `references/canonical-base-compact.png` 和 `references/layout-guides/waving.png`，原始参考图也完整保留。
图片由内置 imagegen 生成；透明背景、布局和 GIF 则使用确定性的图像处理完成。

后续如需制作原生 v2 桌宠，规划规格为 1536×2288、8 列×11 行、单格 192×208，需补齐各状态和方向并完成整体检查。不能把当前四帧 GIF 当成完整精灵图直接导入。
提取与检查脚本需要 Python 和 Pillow；额外视频预览辅助脚本还会用到 numpy、OpenCV。素材本身查看不需要这些依赖。

此包只汇总小巴的制作文件，没有包含账号凭据、应用配置或聊天数据库。
'''
entries['先读我.md'] = readme.encode('utf-8')
entries['生成原图索引.json'] = json.dumps(history_files, ensure_ascii=False, indent=2).encode('utf-8')

manifest = [
    {'file': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    for name, data in sorted(entries.items())
]
entries['文件清单_SHA256.json'] = json.dumps(
    {'package': PREFIX, 'date': '2026-10-22', 'files': manifest},
    ensure_ascii=False, indent=2,
).encode('utf-8')

OUT.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for name, data in sorted(entries.items()):
        archive.writestr(f'{PREFIX}/{name}', data)

with zipfile.ZipFile(OUT) as archive:
    if archive.testzip() is not None:
        raise RuntimeError('ZIP integrity check failed')
    expected = {f'{PREFIX}/{name}' for name in entries}
    if set(archive.namelist()) != expected:
        raise RuntimeError('Archive file list mismatch')
    for record in manifest:
        actual = archive.read(f'{PREFIX}/{record["file"]}')
        if hashlib.sha256(actual).hexdigest() != record['sha256']:
            raise RuntimeError(f'Hash mismatch: {record["file"]}')

result = {
    'ok': True,
    'archive': str(OUT),
    'files': len(entries),
    'generated_history_images': len(history_files),
    'bytes': OUT.stat().st_size,
    'megabytes': round(OUT.stat().st_size / 1024 / 1024, 2),
    'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
    'checks': ['ZIP CRC', 'complete entry list', 'all file SHA-256 hashes'],
}
(ROOT / 'outputs' / '小巴-全部素材与工程-打包校验.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8',
)
print(json.dumps(result, ensure_ascii=False, indent=2))
