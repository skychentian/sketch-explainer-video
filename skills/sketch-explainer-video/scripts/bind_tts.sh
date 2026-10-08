#!/bin/zsh
# 把使用者自己的 ListenHub API Key 写到本机。不回显，不进仓库。
# 用法：bash bind_tts.sh
# 或：LISTENHUB_API_KEY=密钥 bash bind_tts.sh
set -e
DEST="$HOME/.config/sketch-explainer-video/listenhub.key"
mkdir -p "${DEST:h}"
if [[ -n ${LISTENHUB_API_KEY:-} ]]; then
  KEY=$LISTENHUB_API_KEY
elif [[ -t 0 ]]; then
  echo "请粘贴 ListenHub API Key（输入时不显示），回车结束："
  read -rs KEY
  echo
else
  echo "没有读到密钥。请在终端运行这个脚本并粘贴 Key，或先 export LISTENHUB_API_KEY。"
  echo "申请地址：https://listenhub.ai/settings/api-keys"
  exit 2
fi
KEY=${KEY//[$'\n\r ']/}
[[ -n $KEY ]] || { echo "密钥是空的"; exit 2; }
umask 077
print -n -- "$KEY" > "$DEST"
chmod 600 "$DEST"
unset KEY LISTENHUB_API_KEY
echo "已绑定到本机（$DEST），权限 600。Key 不会出现在仓库或日志里。"
echo "请使用自己的 Key，不要用 listenhub auth login 代替。"
