#!/bin/zsh
# 在工程目录运行：渲染成片到 renders/video.mp4 并核对音视频流与时长
set -e
npx -y hyperframes@0.8.117 render --quality high --output renders/video.mp4 > render.log 2>&1 || { tail -20 render.log; exit 1; }
ROOT=$(grep -oE 'data-composition-id="main"[^>]*data-duration="[0-9.]+"' index.html | grep -oE '[0-9.]+"$' | tr -d '"')
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/video.mp4)
STREAMS=$(ffprobe -v error -show_entries stream=codec_name -of csv=p=0 renders/video.mp4 | tr '\n' ' ')
echo "✓ renders/video.mp4  时长 ${DUR}s（应为 ${ROOT}s） 流: $STREAMS"
[[ $STREAMS == *h264* && $STREAMS == *aac* ]] || { echo "✗ 缺视频或音频流"; exit 1; }
