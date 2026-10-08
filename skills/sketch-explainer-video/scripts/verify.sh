#!/bin/zsh
# 写完/改完画面后在工程目录运行：字体子集 → 静态检查 → hyperframes lint/check → 截图
# 截图取每个画面“开始后 1.2 秒”和“结束前 0.4 秒”，拼成 snapshots/contact-sheet*.jpg，必须亲眼看
set -e
SKILL=${0:A:h:h}; PY=~/.cache/sketch-explainer-video/venv/bin/python
[[ -f index.html && -f assets/timing.js ]] || { echo "请在视频工程目录里运行"; exit 1; }
echo "① 字体子集"; $PY $SKILL/scripts/subset_fonts.py ${FONT:+--font $FONT}
echo "② 静态检查"; python3 $SKILL/scripts/check.py || { echo "→ 先修上面的 ✗ 再继续"; exit 1; }
echo "③ lint"; npx -y hyperframes@0.8.117 lint 2>&1 | grep -E "error\(s\)|✗|error:" | grep -v nested_structure || true
LINTERR=$(npx -y hyperframes@0.8.117 lint 2>&1 | grep -oE "[0-9]+ error\(s\)" | head -1 | grep -oE "^[0-9]+")
[[ "$LINTERR" == "0" ]] || { echo "→ lint 有 error，先修"; exit 1; }
echo "④ check"; npx -y hyperframes@0.8.117 check 2>&1 | grep -E "Check passed|Check failed|error\(s\), [1-9]|content_overlap|text_box_overflow|✗" | head -20
TIMES=$(python3 - <<'PY'
import re
h=open('index.html',encoding='utf-8').read()
ts=[]
for m in re.finditer(r'<section[^>]*class="[^"]*scene[^"]*"[^>]*>',h):
    tag=m.group(0); s=float(re.search(r'data-start="([\d.]+)"',tag).group(1)); d=float(re.search(r'data-duration="([\d.]+)"',tag).group(1))
    ts += [round(min(s+1.2, s+d/2),2), round(s+d-0.4,2)]
print(','.join(str(t) for t in ts))
PY
)
echo "⑤ 截图 $TIMES"; rm -rf snapshots; npx -y hyperframes@0.8.117 snapshot --no-end --at $TIMES 2>&1 | grep -E "contact|rror" || true
ENDS=$(echo $TIMES | tr ',' '\n' | awk 'NR%2==0' | paste -sd, -)
echo "⑥ 画面密度"; $PY $SKILL/scripts/density.py $ENDS || { echo "→ 空白帧太多，先把画面铺满再渲染"; exit 1; }
ls snapshots/contact-sheet*.jpg 2>/dev/null && echo "→ 打开上面的 contact-sheet 逐张看：重叠/出框/压字幕/图标看不懂/开场有没有散落的小点"
