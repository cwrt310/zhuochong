"""Register approved extracted rows using one scale per row; keep jump displacement."""
import json, sys, shutil
from pathlib import Path
from PIL import Image
sys.path.insert(0,'C:/Users/cwrt/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/scripts')
from extract_strip_frames import ROW_FRAME_COUNTS

run=Path(sys.argv[1]); target=run/'frames'; target.mkdir(exist_ok=True)
report=[]; manifests=[]
for state,count in ROW_FRAME_COUNTS.items():
    root=run/'qa'/'rows'/state/'frames'
    source=root/state
    files=sorted(source.glob('*.png'))
    if len(files)!=count: raise RuntimeError(f'{state}: {len(files)} != {count}')
    imgs=[Image.open(p).convert('RGBA') for p in files]
    bounds=[im.getbbox() for im in imgs]
    tallest=max(b[3]-b[1] for b in bounds)
    widest=max(b[2]-b[0] for b in bounds)
    source_ground=max(b[3] for b in bounds)
    source_top=min(b[1] for b in bounds)
    scale=min(170/tallest,176/widest,193/(source_ground-source_top),1)
    out=target/state; out.mkdir(exist_ok=True)
    for n,(im,b) in enumerate(zip(imgs,bounds)):
        crop=im.crop(b)
        crop=crop.resize((max(1,round(crop.width*scale)),max(1,round(crop.height*scale))),Image.Resampling.LANCZOS)
        y=198-round((source_ground-b[1])*scale)
        frame=Image.new('RGBA',(192,208))
        frame.alpha_composite(crop,((192-crop.width)//2,y))
        frame.save(out/f'{n:02d}.png')
    manifest=json.loads((root/'frames-manifest.json').read_text())
    manifests.extend(manifest['rows'])
    report.append({'state':state,'scale':scale,'source_ground':source_ground,'target_ground':198,'shared_scale':True,'preserves_vertical_displacement':True})
(target/'frames-manifest.json').write_text(json.dumps({'ok':True,'chroma_key':{'hex':'#00FF00','rgb':[0,255,0],'threshold':96},'rows':manifests},indent=2))
(run/'qa'/'standard-registration.json').write_text(json.dumps({'rows':report},indent=2))
print(json.dumps({'frames_root':str(target.resolve()),'rows':report},indent=2))
