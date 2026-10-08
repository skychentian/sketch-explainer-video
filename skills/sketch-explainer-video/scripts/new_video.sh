#!/bin/zsh
# 新建一条简笔画口播视频工程：配音 → 本地识别 → 逐字对齐 → 引擎就位
# 用法：
#   new_video.sh <工程目录> <口播文案.txt> [--speaker 音色ID] [--title 标题] [--audio 已有配音.mp3] [--tts-json 已有结果.json] [--font 手写字体]
# 不给 --audio / --tts-json 时，用使用者自己的 ListenHub API Key 合成（见 bind_tts.sh）
set -e
SKILL=${0:A:h:h}
DIR=$1; SCRIPT=$2; shift 2
SPEAKER=chat-girl-105-cn; TITLE=""; TTSJSON=""; AUDIO=""; FONT=""
while [[ $# -gt 0 ]]; do case $1 in
  --speaker) SPEAKER=$2; shift 2;; --title) TITLE=$2; shift 2;;
  --tts-json) TTSJSON=${2:A}; shift 2;; --audio) AUDIO=${2:A}; shift 2;; --font) FONT=$2; shift 2;;
  *) echo "未知参数 $1"; exit 1;; esac; done
[[ -f $SCRIPT ]] || { echo "找不到文案 $SCRIPT"; exit 1; }
SCRIPT=${SCRIPT:A}
[[ -e $DIR/index.html ]] && { echo "$DIR 已存在工程，换个目录"; exit 1; }
for b in ffmpeg ffprobe coli npx python3; do command -v $b >/dev/null || { echo "缺少命令 $b"; exit 1; }; done
if [[ -z $AUDIO && -z $TTSJSON ]]; then
  command -v listenhub >/dev/null || { echo "缺少 listenhub CLI"; exit 1; }
  if [[ -z ${LISTENHUB_API_KEY:-} ]]; then
    KEYFILE="$HOME/.config/sketch-explainer-video/listenhub.key"
    [[ -f $KEYFILE ]] && LISTENHUB_API_KEY="$(<"$KEYFILE")"
  fi
  if [[ -z ${LISTENHUB_API_KEY:-} ]]; then
    echo "还没有绑定 ListenHub API Key，这次没有调用配音。"
    echo "请使用者自己申请并绑定（不要把 Key 贴进对话，也不要改用 listenhub auth login）："
    echo "1. 打开 https://listenhub.ai/settings/api-keys 创建 API Key。"
    echo "2. 在自己的电脑执行：bash $SKILL/scripts/bind_tts.sh"
    echo "默认音色是晓曼 chat-girl-105-cn。已有 mp3 时加 --audio。说明见 references/tts.md。"
    exit 2
  fi
  export LISTENHUB_API_KEY
fi
VENV=~/.cache/sketch-explainer-video/venv
[[ -x $VENV/bin/python ]] || { python3 -m venv $VENV && $VENV/bin/pip -q install fonttools brotli pillow; }
PY=$VENV/bin/python
mkdir -p $DIR/assets/audio $DIR/assets/fonts && cd $DIR
grep -v '^[[:space:]]*$' $SCRIPT > user_script.txt
[[ -z $TITLE ]] && TITLE=$(head -c 30 user_script.txt | tr -d '\n')
NAME=${PWD:t}
printf '{\n  "id": "%s",\n  "name": "%s"\n}\n' $NAME $NAME > meta.json
printf '{\n  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",\n  "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}\n}\n' > hyperframes.json
# 1. 配音
if [[ -n $AUDIO ]]; then cp $AUDIO assets/audio/narration.mp3
else
  if [[ -z $TTSJSON ]]; then
    echo "→ ListenHub 合成配音（音色 $SPEAKER，使用已绑定的 API Key）…"
    listenhub openapi tts --text "$(cat user_script.txt)" --voice "$SPEAKER" --output assets/audio/narration.mp3 --format mp3
  else
    cp $TTSJSON assets/audio/tts.json
    URL=$(python3 -c "import json;print(json.load(open('assets/audio/tts.json'))['topicDetail']['audio']['data']['audioUrl'])")
    curl -sSL -o assets/audio/narration.mp3 "$URL"
  fi
fi
# 2. 本地识别（coli 并发会串结果 → 全局锁，批量时自动排队）
LOCK=/tmp/sketch-explainer-video-asr.lock
until mkdir $LOCK 2>/dev/null; do sleep 3; done
trap 'rmdir $LOCK 2>/dev/null' EXIT
echo "→ 本地识别…"
coli asr -j --language zh assets/audio/narration.mp3 > assets/audio/asr.json 2>/dev/null
rmdir $LOCK; trap - EXIT
# 3. 对齐 + 时间数据
$PY $SKILL/scripts/align.py
$PY $SKILL/scripts/make_timing.py
END=$(python3 -c "import re;print(re.search(r'VO_END=([0-9.]+)',open('assets/timing.js').read()).group(1))")
TOTAL=$(python3 -c "print(round($END+1.0,1))")
# 4. 引擎
sed "s/__TOTAL__/$TOTAL/g; s/__VOEND__/$END/g; s/__TITLE__/$TITLE/g" $SKILL/assets/engine.html > index.html
echo 'window.CAP_BREAKS = [];' > assets/cap_breaks.js
if [[ -n $FONT ]]; then $PY $SKILL/scripts/subset_fonts.py --font $FONT; else $PY $SKILL/scripts/subset_fonts.py; fi
echo "✓ 工程就绪：$PWD"
echo "  配音 ${END}s，成片 ${TOTAL}s。下一步：读 sentences.txt 切分镜，在 index.html 的 <!--SCENES--> 处写画面"
