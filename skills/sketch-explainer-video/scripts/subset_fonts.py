# 收集工程里所有文字，把手写字体子集化为 woff2（改了任何画面文字后都要重跑）
# 默认用 macOS 自带手札体 Hannotate；非 macOS 用 --font 指定任意中文手写 TTF/OTF
import glob, sys, os
from fontTools.ttLib import TTCollection, TTFont
from fontTools import subset
HANNOTATE = glob.glob("/System/Library/AssetsV2/**/Hannotate.ttc", recursive=True)
font_arg = sys.argv[sys.argv.index("--font") + 1] if "--font" in sys.argv else None
text = set(chr(c) for c in range(0x20, 0x7f)) | set("，。、？！：；“”‘’（）《》·…—→←↑↓✓✗×≠＝+－％㎡≤≥①②③④⑤⑥⑦⑧⑨")
for p in ["user_script.txt", "index.html"] + glob.glob("compositions/**/*.html", recursive=True):
    if os.path.exists(p): text |= set(open(p, encoding="utf-8").read())
if font_arg:
    faces = [(TTFont(font_arg), "hand-regular"), (TTFont(font_arg), "hand-bold")]
elif HANNOTATE:
    col = TTCollection(HANNOTATE[0]); faces = [(col.fonts[0], "hand-regular"), (col.fonts[2], "hand-bold")]
else:
    sys.exit("找不到手札体 Hannotate.ttc，请用 --font 指定一个中文手写字体文件")
os.makedirs("assets/fonts", exist_ok=True)
for font, name in faces:
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]
    s = subset.Subsetter(opts); s.populate(text="".join(text)); s.subset(font)
    font.flavor = "woff2"; font.save(f"assets/fonts/{name}.woff2")
print("fonts subset:", len(text), "chars")
