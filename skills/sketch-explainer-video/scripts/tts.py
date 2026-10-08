#!/usr/bin/env python3
"""按已绑定的 MiniMax 或豆包 Key 把口播文案合成 mp3。绝不打印密钥。"""
import argparse
import base64
import json
import os
import sys
import uuid
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tts_bind

MINIMAX_PRIMARY = "https://api.minimax.cn"
MINIMAX_BACKUP = "https://api-bj.minimaxi.com"
DOUBAO_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"


def scrub(text, key):
    return text.replace(key, "***") if key else text


def post(url, headers, body):
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read()


def objects_from(raw):
    dec = json.JSONDecoder()
    i, n = 0, len(raw)
    while i < n:
        while i < n and raw[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        obj, i = dec.raw_decode(raw, i)
        yield obj


def assemble_doubao(raw):
    audio, usage, ended = bytearray(), None, False
    for obj in objects_from(raw):
        if not isinstance(obj, dict):
            continue
        try:
            code = int(obj.get("code"))
        except (TypeError, ValueError):
            continue
        if code == 0 and obj.get("data"):
            audio.extend(base64.b64decode(obj["data"]))
        elif code == 20000000:
            ended = True
            usage = (obj.get("usage") or {}).get("text_words")
        elif code != 0:
            return b"", None, False, obj.get("message") or str(code)
    if not ended or len(audio) < 1000:
        return b"", usage, ended, "豆包没有返回完整音频"
    return bytes(audio), usage, True, ""


def doubao_resource(speaker):
    forced = os.environ.get("DOUBAO_RESOURCE_ID", "").strip()
    if forced:
        return forced
    if "uranus" in speaker or "saturn" in speaker:
        return "seed-tts-2.0"
    return "seed-tts-1.0"


def write_audio(out, kind, audio):
    if kind == "url":
        urllib.request.urlretrieve(audio, out)
        return Path(out).read_bytes()
    Path(out).write_bytes(audio)
    return audio


def minimax_payload(host, key, body):
    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    return json.loads(post(host.rstrip("/") + "/v1/t2a_v2", headers, body))


def call_minimax(host, key, body):
    try:
        return minimax_payload(host, key, body), ""
    except urllib.error.HTTPError as e:
        detail = scrub(e.read().decode("utf-8", "replace")[:400], key)
        if e.code in (401, 403):
            sys.exit("MiniMax 拒绝了这把 Key（HTTP %s）。请核对后重新绑定。\n%s" % (e.code, detail))
        return None, "HTTP %s %s" % (e.code, detail)
    except Exception as e:
        return None, scrub(str(e), key)


def synthesize_minimax(text, speaker, model, out):
    key = tts_bind.load_key("minimax")
    body = {
        "model": model,
        "text": text,
        "stream": False,
        "language_boost": "Chinese",
        "output_format": "hex",
        "voice_setting": {"voice_id": speaker, "speed": 1, "vol": 1, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }
    host = os.environ.get("MINIMAX_API_HOST", MINIMAX_PRIMARY).strip() or MINIMAX_PRIMARY
    payload, err = call_minimax(host, key, body)
    if payload is None and host == MINIMAX_PRIMARY:
        payload, err = call_minimax(MINIMAX_BACKUP, key, body)
    if payload is None:
        sys.exit("MiniMax 请求失败：%s" % err)
    base = payload.get("base_resp") or {}
    if base.get("status_code") not in (0, None):
        sys.exit("MiniMax 合成失败：%s" % (base.get("status_msg") or base))
    audio = ((payload.get("data") or {}).get("audio") or "").strip()
    kind = "url" if audio.startswith("http://") or audio.startswith("https://") else "hex"
    data = audio if kind == "url" else bytes.fromhex(audio)
    data = write_audio(out, kind, data)
    if len(data) < 1000:
        sys.exit("MiniMax 没有返回有效音频")
    extra = payload.get("extra_info") or {}
    note = "✓ 配音已写入 %s（MiniMax %s / %s）" % (out, model, speaker)
    if extra.get("audio_length"):
        note += "，约 %.1fs" % (int(extra["audio_length"]) / 1000)
    if extra.get("usage_characters"):
        note += "，计费字符 %s" % extra["usage_characters"]
    print(note)


def synthesize_doubao(text, speaker, out):
    key = tts_bind.load_key("doubao")
    resource = doubao_resource(speaker)
    body = {
        "user": {"uid": "sketch-explainer"},
        "req_params": {
            "text": text,
            "speaker": speaker,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
                "speech_rate": 0,
                "loudness_rate": 0,
            },
        },
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": key,
        "X-Api-Resource-Id": resource,
        "X-Api-Request-Id": str(uuid.uuid4()),
    }
    try:
        raw = post(DOUBAO_URL, headers, body).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        detail = scrub(e.read().decode("utf-8", "replace")[:400], key)
        if e.code in (401, 403):
            sys.exit("豆包拒绝了这把 Key（HTTP %s）。请到火山引擎控制台核对后重新绑定。\n%s" % (e.code, detail))
        sys.exit("豆包请求失败：HTTP %s %s" % (e.code, detail))
    except Exception as e:
        sys.exit("豆包请求失败：%s" % scrub(str(e), key))
    try:
        audio, usage, _ended, err = assemble_doubao(raw)
    except (json.JSONDecodeError, ValueError):
        sys.exit("豆包返回的不是可解析的合成结果")
    if err:
        sys.exit("豆包合成失败：%s" % err)
    Path(out).write_bytes(audio)
    note = "✓ 配音已写入 %s（豆包 %s / %s）" % (out, resource, speaker)
    if usage:
        note += "，计费字符 %s" % usage
    print(note)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--provider", default="")
    p.add_argument("--text-file")
    p.add_argument("--out")
    p.add_argument("--speaker", default="")
    p.add_argument("--model", default="speech-2.8-turbo")
    args = p.parse_args()
    provider = args.provider.strip()
    if provider and provider not in ("minimax", "doubao"):
        sys.exit("provider 只能是 minimax 或 doubao")
    if args.speaker:
        tts_bind.reject_old(args.speaker)
    chosen = tts_bind.resolve(provider)
    if args.check:
        if not chosen:
            print(tts_bind.guide(provider))
            sys.exit(2)
        print(chosen)
        return
    if not chosen:
        print(tts_bind.guide(provider))
        sys.exit(2)
    speaker = args.speaker or tts_bind.DEFAULT_SPEAKER[chosen]
    text = Path(args.text_file).read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("文案是空的")
    if chosen == "minimax":
        if len(text) > 10000:
            sys.exit("文案 %s 字，超过 MiniMax 同步接口 10000 字上限，请拆开再做" % len(text))
        synthesize_minimax(text, speaker, args.model, args.out)
        return
    synthesize_doubao(text, speaker, args.out)


if __name__ == "__main__":
    main()
