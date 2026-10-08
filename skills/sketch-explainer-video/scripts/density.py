# 量截图：每个画面结束帧里，字幕带以上内容最低铺到哪（px）。<1000px = 下半屏大片空白
# 用法（工程目录）：python density.py 12.6,19.0,...   参数是各画面“结束前 0.4 秒”的时间
import sys, glob, re
from PIL import Image
want = [float(t) for t in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
files = {float(re.search(r'at-([\d.]+)s', p).group(1)): p for p in glob.glob('snapshots/frame-*.png')}
def bottom(p):
    im = Image.open(p).convert('L'); w, h = im.size; sc = h / 1920; px = im.load()
    for y in range(int(1500 * sc), 0, -2):
        if sum(1 for x in range(0, w, 3) if px[x, y] < 110) >= 3: return y / sc
    return 0
bad = []
for t in (want or sorted(files)):
    p = min(files.items(), key=lambda kv: abs(kv[0] - t))[1] if files else None
    if not p: continue
    b = bottom(p)
    if b < 1000: bad.append((t, b))
for t, b in bad: print(f'  ✗ {t:.1f}s 结束帧内容只铺到 {b:.0f}px（下半屏空）→ 放大主视觉/加图形/把内容往下铺到 1100–1400px')
n = len(want or files)
print(f'画面密度：{n - len(bad)}/{n} 帧达标' + ('' if not bad else '，空的帧要改'))
sys.exit(1 if len(bad) > max(1, n // 6) else 0)
