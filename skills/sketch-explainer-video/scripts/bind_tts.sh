#!/bin/bash
# 把使用者自己的 MiniMax 或豆包 API Key 写到本机。不回显，不进仓库。
# 用法：bash bind_tts.sh minimax
#       bash bind_tts.sh doubao
# 或：MINIMAX_API_KEY=密钥 bash bind_tts.sh minimax
#     DOUBAO_API_KEY=密钥 bash bind_tts.sh doubao
set -euo pipefail
PROV="${1:-}"
if [[ -z "$PROV" ]]; then
  if [[ -t 0 ]]; then
    printf '要绑定哪一家？输入 minimax 或 doubao：'
    read -r PROV
  else
    echo "请指定一家：bash bind_tts.sh minimax    或    bash bind_tts.sh doubao"
    exit 2
  fi
fi
case "$PROV" in
  minimax)
    ENVNAME=MINIMAX_API_KEY
    DEST="$HOME/.config/sketch-explainer-video/minimax.key"
    LABEL="MiniMax"
    HINT="申请地址：https://platform.minimax.cn （账户管理 → 接口密钥）"
    ;;
  doubao)
    ENVNAME=DOUBAO_API_KEY
    DEST="$HOME/.config/sketch-explainer-video/doubao.key"
    LABEL="豆包"
    HINT="申请地址：https://console.volcengine.com/speech/new （API Key，开通豆包语音合成模型2.0）"
    ;;
  *)
    echo "只支持 minimax 或 doubao。"
    exit 2
    ;;
esac
mkdir -p "$(dirname "$DEST")"
if [[ -n "${!ENVNAME:-}" ]]; then
  KEY="${!ENVNAME}"
elif [[ -t 0 ]]; then
  printf '请粘贴 %s API Key（输入时不显示），回车结束：\n' "$LABEL"
  read -rs KEY
  printf '\n'
else
  echo "没有读到密钥。请在终端运行这个脚本并粘贴 Key，或先 export ${ENVNAME}。"
  echo "$HINT"
  exit 2
fi
KEY="${KEY//[$'\n\r ']/}"
[[ -n "$KEY" ]] || { echo "密钥是空的"; exit 2; }
umask 077
printf '%s' "$KEY" > "$DEST"
chmod 600 "$DEST"
KEY=""
echo "已绑定 ${LABEL}。文件：${DEST} 。权限 600。Key 不会出现在仓库或日志里。"
if [[ "$PROV" == "minimax" ]]; then
  echo "国际站 Key 请再执行：export MINIMAX_API_HOST=https://api.minimax.io"
fi
