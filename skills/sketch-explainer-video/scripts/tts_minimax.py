#!/usr/bin/env python3
"""用使用者自己的 MiniMax API Key 把口播文案合成 mp3。绝不打印密钥。"""
import argparse, json, os, sys, urllib.error, urllib.request
from pathlib import Path

KEY_FILE = Path.home() / ".config" / "sketch-explainer-video" / "minimax.key"
BIND = Path(__file__).resolve().parent / "bind_tts.sh"
PRIMARY = "https://api.minimax.cn"
BACKUP = "https://api-bj.minimaxi.com"
OLD_SPEAKERS = {
    "chat-girl-105-cn": "晓曼",
    "gaoqing3-bfb5c88a": "高晴",
    "suzhe-45bbbe54": "苏哲",
}

GUIDE = """
还没有绑定 MiniMax 配音 Key，这次没有合成，也没有扣费。
请使用者自己申请并绑定（不要把 Key 贴进对话）：

1. 打开 https://platform.minimax.cn 注册，进入「账户管理 → 接口密钥」，创建 API Key。
   国际站账号用 https://platform.minimax.io ，并另外设置：
   export MINIMAX_API_HOST=https://api.minimax.io
2. 在自己的电脑上绑定（输入时不显示，Key 只留在本机）：
   bash {bind}
   若 Key 已经在环境变量里：MINIMAX_API_KEY=你的密钥 bash {bind}
3. 绑好后重新跑 new_video.sh。

默认模型 speech-2.8-turbo（约 0.4 元/千汉字）。想要更好听：--model speech-2.8-hd。
已有 mp3 时加 --audio，不要重新合成。价格说明见 references/tts.md。
""".format(bind=BIND).strip()


def load_key():
    key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if key:
        return key
    if KEY_FILE.is_file():
        return KEY_FILE.read_text(encoding="utf-8").strip()
    return ""


def audio_from(payload):
    audio = ((payload.get("data") or {}).get("audio") or "").strip()
    if audio.startswith("http://") or audio.startswith("https://"):
        return "url", audio
    return "hex", bytes.fromhex(audio)


def post(host, key, body):
    req = urllib.request.Request(
        host.rstrip("/") + "/v1/t2a_v2",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--text-file", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--speaker", required=True)
    p.add_argument("--model", default="speech-2.8-turbo")
    args = p.parse_args()
    if args.speaker in OLD_SPEAKERS:
        sys.exit(
            f"音色 {args.speaker}（{OLD_SPEAKERS[args.speaker]}）是旧的 ListenHub 音色。\n"
            "请改用 MiniMax 音色，例如 Chinese (Mandarin)_Gentle_Senior"
        )
    text = Path(args.text_file).read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("文案是空的")
    if len(text) > 10000:
        sys.exit(f"文案 {len(text)} 字，超过 MiniMax 同步接口 10000 字上限，请拆开再做")
    key = load_key()
    if not key:
        sys.exit(GUIDE)
    body = {
        "model": args.model,
        "text": text,
        "stream": False,
        "language_boost": "Chinese",
        "output_format": "hex",
        "voice_setting": {"voice_id": args.speaker, "speed": 1, "vol": 1, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }
    host = os.environ.get("MINIMAX_API_HOST", PRIMARY).strip() or PRIMARY
    try:
        payload = post(host, key, body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        if e.code in (401, 403):
            sys.exit(f"MiniMax 拒绝了这把 Key（HTTP {e.code}）。请到开放平台核对密钥后重新绑定。\n{detail}")
        if host == PRIMARY:
            try:
                payload = post(BACKUP, key, body)
            except Exception as e2:
                sys.exit(f"MiniMax 请求失败：{e2}")
        else:
            sys.exit(f"MiniMax 请求失败：HTTP {e.code} {detail}")
    except Exception as e:
        if host == PRIMARY:
            try:
                payload = post(BACKUP, key, body)
            except Exception as e2:
                sys.exit(f"MiniMax 请求失败：{e2}")
        else:
            sys.exit(f"MiniMax 请求失败：{e}")
    base = payload.get("base_resp") or {}
    if base.get("status_code") not in (0, None):
        sys.exit(f"MiniMax 合成失败：{base.get('status_msg') or base}")
    kind, audio = audio_from(payload)
    if kind == "url":
        urllib.request.urlretrieve(audio, args.out)
    else:
        if len(audio) < 1000:
            sys.exit("MiniMax 没有返回有效音频")
        Path(args.out).write_bytes(audio)
    extra = payload.get("extra_info") or {}
    chars = extra.get("usage_characters")
    ms = extra.get("audio_length")
    note = f"✓ 配音已写入 {args.out}（{args.model} / {args.speaker}）"
    if ms:
        note += f"，约 {int(ms)/1000:.1f}s"
    if chars:
        note += f"，计费字符 {chars}"
    print(note)


if __name__ == "__main__":
    main()
