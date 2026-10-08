#!/usr/bin/env python3
"""读取本机 MiniMax / 豆包 Key，并在没绑定时给出绑定步骤。绝不打印密钥。"""
import os
import sys
from pathlib import Path

HOME = Path.home() / ".config" / "sketch-explainer-video"
BIND = Path(__file__).resolve().parent / "bind_tts.sh"
OLD = {
    "chat-girl-105-cn": "晓曼",
    "gaoqing3-bfb5c88a": "高晴",
    "suzhe-45bbbe54": "苏哲",
}
DEFAULT_SPEAKER = {
    "minimax": "Chinese (Mandarin)_Gentle_Senior",
    "doubao": "zh_female_xiaohe_uranus_bigtts",
}


def env_name(provider):
    return "MINIMAX_API_KEY" if provider == "minimax" else "DOUBAO_API_KEY"


def load_key(provider):
    key = os.environ.get(env_name(provider), "").strip()
    if key:
        return key
    path = HOME / (provider + ".key")
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return ""


def resolve(provider):
    if provider in ("minimax", "doubao"):
        return provider if load_key(provider) else ""
    if load_key("minimax"):
        return "minimax"
    if load_key("doubao"):
        return "doubao"
    return ""


def guide(provider=""):
    text = """还没有绑定 MiniMax 或豆包，这次没有合成，也没有扣费。
请使用者自己申请并绑定其中一家。不要把 Key 贴进对话。

MiniMax（默认。两家都绑了时用这一家）
1. 打开 https://platform.minimax.cn ，进入「账户管理 → 接口密钥」，创建 API Key。
   国际站账号用 https://platform.minimax.io ，并设置 MINIMAX_API_HOST=https://api.minimax.io
2. 在自己的电脑执行：bash {bind} minimax

豆包语音（火山引擎新版控制台，同样是一把 API Key）
1. 打开 https://console.volcengine.com/speech/new ，创建 API Key，并开通「豆包语音合成模型2.0」。
2. 在自己的电脑执行：bash {bind} doubao

绑好后重新跑 new_video.sh。已有 mp3 时加 --audio，不要重新合成。
价格和音色见 references/tts.md。""".format(bind=BIND)
    if provider == "minimax":
        text += "\n\n这次指定了 MiniMax，但这台电脑上还没有 MiniMax Key。"
    elif provider == "doubao":
        text += "\n\n这次指定了豆包，但这台电脑上还没有豆包 Key。"
    return text


def reject_old(speaker):
    if speaker in OLD:
        print(
            "音色 {sid}（{name}）是 ListenHub 音色，线上这份 skill 不使用。\n"
            "请改用 MiniMax 音色，例如 Chinese (Mandarin)_Gentle_Senior；\n"
            "或豆包音色，例如 zh_female_xiaohe_uranus_bigtts。\n"
            "如果还没绑定 Key，先按 references/tts.md 绑定 MiniMax 或豆包。".format(
                sid=speaker, name=OLD[speaker]
            )
        )
        sys.exit(1)
