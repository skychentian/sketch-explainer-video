#!/bin/zsh
# 把使用者自己的 MiniMax API Key 写到本机。不回显，不进仓库。
# 用法：bash bind_tts.sh
# 或：MINIMAX_API_KEY=密钥 bash bind_tts.sh
set -e
DEST="$HOME/.config/sketch-explainer-video/minimax.key"
mkdir -p "${DEST:h}"
if [[ -n ${MINIMAX_API_KEY:-} ]]; then
  KEY=$MINIMAX_API_KEY
elif [[ -t 0 ]]; then
  echo "请粘贴 MiniMax API Key（输入时不显示），回车结束："
  read -rs KEY
  echo
else
  echo "没有读到密钥。请在终端运行这个脚本并粘贴 Key，或先 export MINIMAX_API_KEY。"
  echo "申请地址：https://platform.minimax.cn （账户管理 → 接口密钥）"
  exit 2
fi
KEY=${KEY//[$'\n\r ']/}
[[ -n $KEY ]] || { echo "密钥是空的"; exit 2; }
umask 077
print -n -- "$KEY" > "$DEST"
chmod 600 "$DEST"
unset KEY MINIMAX_API_KEY
echo "已绑定到本机（$DEST），权限 600。Key 不会出现在仓库或日志里。"
echo "国际站 Key 请再执行：export MINIMAX_API_HOST=https://api.minimax.io"
