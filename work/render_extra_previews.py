import sys, json
from pathlib import Path
from PIL import Image, ImageDraw
import cv2
import numpy as np

scripts = Path('C:/Users/cwrt/.codex/plugins/cache/openai-curated-remote/work-pets/0.1.6/skills/create-pet/scripts')
sys.path.insert(0, str(scripts))
from render_animation_previews import ROW_DURATIONS, save_preview

atlas_path, output_dir = map(Path, sys.argv[1:3])
out = output_dir
out.mkdir(parents=True, exist_ok=True)
atlas = Image.open(atlas_path).convert('RGBA')
def cell(r,c):
    return atlas.crop((192*c,208*r,192*(c+1),208*(r+1)))

frames_root = out / 'encoded-frames'
all_frames, durations = [], []
for row,(state,times) in enumerate(ROW_DURATIONS.items()):
    folder = frames_root / state
    folder.mkdir(parents=True, exist_ok=True)
    for col,ms in enumerate(times):
        fr=cell(row,col)
        fr.save(folder / f'{col:02d}.png')
        canvas=Image.new('RGB',(384,448),'#eef2fa')
        scaled=fr.resize((384,416),Image.Resampling.NEAREST)
        canvas.paste(scaled,(0,32),scaled)
        ImageDraw.Draw(canvas).text((12,10),f'{state}  frame {col+1}/{len(times)}', fill='#182644')
        all_frames.append(canvas)
        durations.append(ms)
save_preview(all_frames,durations,out/'all-states.gif')
writer=cv2.VideoWriter(str(out/'all-states.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),25,(384,448))
if not writer.isOpened(): raise RuntimeError('MP4 encoder unavailable')
for fr,ms in zip(all_frames,durations):
    bgr=cv2.cvtColor(np.array(fr),cv2.COLOR_RGB2BGR)
    for _ in range(max(1,round(ms/40))): writer.write(bgr)
writer.release()
transition=[cell(0,c) for c in range(6)]+[cell(4,c) for c in range(5)]+[cell(0,c) for c in range(6)]
save_preview(transition,ROW_DURATIONS['idle']+ROW_DURATIONS['jumping']+ROW_DURATIONS['idle'],out/'idle-jump-idle.gif')
save_preview([cell(9+i//8,i%8) for i in range(16)],[180]*16,out/'look-loop.gif')
stills=Image.new('RGB',(768,240),'#eef2fa')
for i,(r,c,label) in enumerate([(0,0,'idle'),(3,2,'wave'),(4,2,'jump peak'),(7,3,'working')]):
    fr=cell(r,c)
    stills.paste(fr,(i*192,32),fr)
    ImageDraw.Draw(stills).text((i*192+8,10),f'{label} r{r} f{c}',fill='#182644')
stills.save(out/'motion-stills.png')
print(json.dumps({'ok':True,'atlas':str(atlas_path.resolve()),'frames_root':str(frames_root.resolve()),'output_dir':str(out.resolve())}))
