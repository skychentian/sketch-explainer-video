# 画面静态检查：按引擎的真实计时规则核对 index.html，报出会出问题的地方
# 在视频工程目录里运行：python3 <skill>/scripts/check.py      退出码 1 = 有必须修的错误
import json, re, sys
from html.parser import HTMLParser

tj = open('assets/timing.js', encoding='utf-8').read()
TX = json.loads(re.search(r'window\.VO_TEXT=(".*?");\n', tj, re.S).group(1))
TT = json.loads(re.search(r'window\.VO_T=(\[.*?\]);', tj, re.S).group(1))
VO_END = float(re.search(r'window\.VO_END=([0-9.]+)', tj).group(1))
html = open('index.html', encoding='utf-8').read()
errors, warns = [], []
E = lambda m: errors.append(m)
W = lambda m: warns.append(m)

def T(p, frm):
    i = TX.find(p, frm)
    if i < 0: return None
    return next((TT[k] for k in range(i, len(TX)) if TT[k] is not None), VO_END)

class Node:
    def __init__(s, tag, attrs, parent):
        s.tag, s.a, s.parent, s.kids, s.text = tag, dict(attrs), parent, [], []
    def textContent(s):
        return ''.join(s.text) + ''.join(k.textContent() for k in s.kids)
    def walk(s):
        yield s
        for k in s.kids: yield from k.walk()


VOID = {'br', 'img', 'meta', 'link', 'input', 'hr', 'source'}
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = Node('root', [], None); s.cur = s.root
    def handle_starttag(s, tag, attrs):
        n = Node(tag, attrs, s.cur); s.cur.kids.append(n)
        if tag not in VOID and not s.get_starttag_text().endswith('/>'): s.cur = n
    def handle_endtag(s, tag):
        c = s.cur
        while c is not s.root and c.tag != tag: c = c.parent
        if c is not s.root: s.cur = c.parent
    def handle_data(s, d): s.cur.text.append(d)
    def handle_entityref(s, name): s.cur.text.append('&')
p = P(); p.feed(html)
nodes = list(p.root.walk())
root = next((n for n in nodes if n.a.get('data-composition-id') == 'main'), None)
ROOT_DUR = float(root.a['data-duration']) if root else 0
if root and abs(ROOT_DUR - round(VO_END + 1.0, 1)) > 0.06:
    W(f'root data-duration={ROOT_DUR}，建议 = 配音结束 {VO_END:.2f} + 1.0')
scenes = [n for n in nodes if n.tag == 'section' and 'scene' in n.a.get('class', '')]
if not scenes: E('index.html 里还没有任何 <section class="clip scene">'); 
scenes.sort(key=lambda n: float(n.a.get('data-start', 0)))
prev_end = 0.0
for sc in scenes:
    sid = sc.a.get('id', '?'); s0 = float(sc.a['data-start']); dur = float(sc.a['data-duration']); s1 = s0 + dur
    if abs(s0 - prev_end) > 0.02: E(f'{sid}: 开始 {s0} 与上一画面结束 {prev_end:.2f} 不衔接')
    prev_end = s1
    if dur > 17: W(f'{sid}: 画面 {dur:.1f}s 偏长，考虑拆分')
    frm_p = sc.a.get('data-from', '')
    frm = TX.find(frm_p) if frm_p else 0
    if frm_p and frm < 0: E(f'{sid}: data-from="{frm_p}" 在口播里找不到'); frm = 0
    last_end, last_desc = s0, ''
    for n in sc.walk():
        for key, base in (('data-w', None), ('data-f', .45), ('data-p', .5), ('data-h', .55), ('data-dim', .4), ('data-d', None)):
            if key not in n.a: continue
            v = n.a[key]
            if not v: t0 = s0 + .15
            elif v.startswith('@'): t0 = s0 + float(v[1:])
            else:
                ph, _, off = v.partition('|')
                t = T(ph, frm)
                if t is None: E(f'{sid}: {key}="{v}" 短语在 data-from 之后的口播里找不到'); continue
                t0 = t + (float(off) if off else 0)
            if key == 'data-w':
                d = min(1.6, max(.35, len(n.textContent().strip()) * .07)); end = t0 + d
                if n.tag == 'span' and 'ib' not in n.a.get('class', '').split() and 'box' not in n.a.get('class', ''):
                    E(f'{sid}: data-w 用在普通 <span> 上（擦出无效），加 class="ib"：{n.textContent().strip()[:12]}')
            elif key == 'data-d':
                per = float(n.a.get('data-dur', '.7'))
                cnt = sum(1 for k in n.walk() if k.tag in ('path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon'))
                texts = sum(1 for k in n.walk() if k.tag == 'text')
                end = t0 + max(0, cnt - 1) * per * .55 + per
                if texts: end = max(end, t0 + .4 + (texts - 1) * .3 + .4)
            else: end = t0 + base
            label = f'{key}="{v}"'
            if t0 > s1 - .05: E(f'{sid}: {label} 在画面结束后才开始（{t0:.2f}s > {s1:.2f}s），永远看不到')
            elif end > s1 - .5: E(f'{sid}: {label} 结束于 {end:.2f}s，离切走 {s1:.2f}s 不足 0.5 秒（会被切掉）→ 锚点前移')
            if end > last_end: last_end, last_desc = end, label
    for n in sc.walk():
        st = n.a.get('style', '')
        m = re.search(r'(?<![-\w])top:\s*(\d+)px', st)
        if m and int(m.group(1)) > 1480 and n.parent is not None and n.parent.tag == 'div' and 'stage' in n.parent.a.get('class', ''):
            E(f'{sid}: 有元素 top:{m.group(1)}px，压进了字幕带（内容须在 120–1480px）')
    if '<br' in ''.join(str(k.tag) for k in sc.walk() if k.tag == 'br'): W(f'{sid}: 用了 <br>，多行请拆成多个块')
    if not any(k.tag == 'svg' for k in sc.walk()) and not any('box' in k.a.get('class', '') for k in sc.walk()):
        W(f'{sid}: 整帧只有文字，没有图标/方框/示意图，考虑加一个图形主视觉')
if scenes:
    if abs(float(scenes[0].a['data-start'])) > .01: E('第一个画面必须从 0 开始')
    if ROOT_DUR and abs(prev_end - ROOT_DUR) > .06: E(f'最后画面结束于 {prev_end:.2f}s，应等于 root data-duration {ROOT_DUR}')
# 字幕：复刻引擎切分
bj = open('assets/cap_breaks.js', encoding='utf-8').read()
BREAKS = json.loads(re.search(r'=\s*(\[.*\])', bj, re.S).group(1))
chunks = []
for m in re.finditer(r'[^，。？！、\n]+[，。？！、]?', TX):
    raw = m.group()
    if not raw.strip(): continue
    cuts = sorted({0} | {raw.find(b) for b in BREAKS if raw.find(b) > 0}) + [len(raw)]
    chunks += [raw[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]
merged = []
for c in chunks:
    if merged and len(merged[-1]) + len(c) <= 14 and re.search(r'[，、]$', merged[-1]): merged[-1] += c
    else: merged.append(c)
width = lambda s: sum(.55 if ord(ch) < 128 else 1 for ch in s)
bad = [re.sub(r'[，。、]$', '', c).strip() for c in merged]
bad = [c for c in bad if width(c) > 17.5]
for c in bad: E(f'字幕超长（{width(c):.0f} 字宽）：「{c}」→ 在 assets/cap_breaks.js 加一个词边界断点')
print(f'画面 {len(scenes)} 个 · 字幕 {len(merged)} 行 · 配音 {VO_END:.2f}s · 成片 {ROOT_DUR}s')
for w in warns: print('  ⚠', w)
for e in errors: print('  ✗', e)
print('✓ 检查通过' if not errors else f'✗ {len(errors)} 个错误需要修')
sys.exit(1 if errors else 0)
