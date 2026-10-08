# 生成 assets/timing.js（原文 + 每字开口时间 + 配音结束时间），并输出每句开始时间到 sentences.txt
import json, re, subprocess
src = open('user_script.txt').read().strip()
ct = json.load(open('assets/audio/char_times.json'))
arr = [None]*len(src)
for o in ct: arr[o['i']] = o['t']
end = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','assets/audio/narration.mp3']).strip())
open('assets/timing.js','w').write('window.VO_TEXT=%s;\nwindow.VO_T=%s;\nwindow.VO_END=%.3f;\n' % (json.dumps(src, ensure_ascii=False), json.dumps(arr), end))
lines = []
for m in re.finditer(r'[^。？！\n]+[。？！]?', src):
    seg = m.group().strip()
    if not seg: continue
    st = next((arr[k] for k in range(m.start(), len(src)) if arr[k] is not None), end)
    lines.append(f"{st:7.2f}  {seg}")
open('sentences.txt','w').write('\n'.join(lines)+f"\n{end:7.2f}  [配音结束]\n")
print('VO_END', end)
