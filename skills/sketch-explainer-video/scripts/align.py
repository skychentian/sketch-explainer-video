# 把口播原文逐字对齐到本地识别的时间戳，输出 assets/audio/char_times.json
# 在视频工程目录里运行：python3 <skill>/scripts/align.py
import json, difflib, re
asr = json.load(open('assets/audio/asr.json'))
toks, ts = asr['tokens'], asr['timestamps']
ac, at = [], []
for i, (t, s) in enumerate(zip(toks, ts)):
    t = t.strip()
    nxt = ts[i + 1] if i + 1 < len(ts) else asr['duration']
    for j, c in enumerate(t):
        ac.append(c); at.append(s + (nxt - s) * j / max(len(t), 1))
src = open('user_script.txt').read().strip()
keep = lambda c: bool(re.match(r'[一-鿿A-Za-z0-9]', c))
sidx = [i for i, c in enumerate(src) if keep(c)]
sc = [src[i].lower() for i in sidx]
aidx = [i for i, c in enumerate(ac) if keep(c)]
acc = [ac[i].lower() for i in aidx]
sm = difflib.SequenceMatcher(None, sc, acc, autojunk=False)
times = [None] * len(sc)
for a, b, n in sm.get_matching_blocks():
    for k in range(n): times[a + k] = at[aidx[b + k]]
known = [i for i, t in enumerate(times) if t is not None]
for i in range(len(times)):
    if times[i] is None:  # 同音字等没对上的字：按前后已知字插值
        p = max([k for k in known if k < i], default=None); q = min([k for k in known if k > i], default=None)
        if p is None: times[i] = times[q]
        elif q is None: times[i] = times[p] + 0.2 * (i - p)
        else: times[i] = times[p] + (times[q] - times[p]) * (i - p) / (q - p)
json.dump([{'i': sidx[k], 'c': src[sidx[k]], 't': round(times[k], 3)} for k in range(len(sc))], open('assets/audio/char_times.json', 'w'), ensure_ascii=False)
matched = sum(n for *_, n in sm.get_matching_blocks())
print(f'matched {matched} / {len(sc)} ({matched / max(len(sc),1):.1%})')
