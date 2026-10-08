# 配音：绑定 MiniMax 或豆包

核对日期：2026-10-08。价格以各家当时的官方页面为准，改价后以控制台为准。

线上这份 skill 只引导绑定下面两家。两家都没有 Key 时，建工程会直接停下来，并打印申请步骤。不要把 Key 贴进对话，也不要为了试听去调用接口。

## 怎么绑

Key 只放两处之一：环境变量，或 `bind_tts.sh` 写成权限 600 的本机文件。

| 一家 | 申请 | 绑定 | 本机文件 | 环境变量 |
| --- | --- | --- | --- | --- |
| MiniMax | https://platform.minimax.cn 「账户管理 → 接口密钥」 | `bash <skill>/scripts/bind_tts.sh minimax` | `~/.config/sketch-explainer-video/minimax.key` | `MINIMAX_API_KEY` |
| 豆包 | https://console.volcengine.com/speech/new 创建 API Key，并开通「豆包语音合成模型2.0」 | `bash <skill>/scripts/bind_tts.sh doubao` | `~/.config/sketch-explainer-video/doubao.key` | `DOUBAO_API_KEY` |

两家都绑了时，默认用 MiniMax。只要豆包时，或想指定一家时，加 `--provider doubao` 或 `--provider minimax`。MiniMax 国际站 Key 再设置 `MINIMAX_API_HOST=https://api.minimax.io`。

已有 mp3 时用 `--audio`，不要重新合成。

## MiniMax

默认 `speech-2.8-turbo`，国内站 `https://api.minimax.cn/v1/t2a_v2`。

这段流水线要的是「按原文朗读的中文旁白」，合成之后用本地识别对齐。Turbo 的中文自然度够做解说。更好听时加 `--model speech-2.8-hd`，同一把 Key。

官方价（https://platform.minimax.cn/docs/pricing/overview ）：

| 模型 | 单价 | 汉字怎么算 | 约合每千汉字 | 约 600 字 |
| --- | --- | --- | --- | --- |
| speech-2.8-turbo | 2.00 元/万计费字符 | 1 个汉字 = 2 个计费字符 | 0.40 元 | 0.24 元 |
| speech-2.8-hd | 3.50 元/万计费字符 | 同上 | 0.70 元 | 0.42 元 |

同步接口单次少于 10000 字。

默认音色温柔学姐 `Chinese (Mandarin)_Gentle_Senior`。新闻女声 `Chinese (Mandarin)_News_Anchor`。温润男声 `Chinese (Mandarin)_Gentleman`。完整列表：https://platform.minimax.cn/docs/faq/system-voice-id

## 豆包

新版控制台用一把 API Key。请求头是 `X-Api-Key`，再加 `X-Api-Resource-Id: seed-tts-2.0`。这对应计费商品「语音合成2.0字符版」。接口是 `https://openspeech.bytedance.com/api/v3/tts/unidirectional`，按原文一次送入，返回分段的 base64 音频再拼成 mp3。

默认音色小何 2.0 `zh_female_xiaohe_uranus_bigtts`。Vivi 2.0 `zh_female_vv_uranus_bigtts`。云舟 2.0 `zh_male_m191_uranus_bigtts`。2.0 音色列表：https://www.volcengine.com/docs/6561/1257544

传 1.0 音色（名字里带 `moon` 或 `mars`）时，资源会改成 `seed-tts-1.0`。要用别的资源，设置 `DOUBAO_RESOURCE_ID`。

火山引擎产品页的「语音合成大模型」字数包标过 10 万字 22.50 元（原价 45 元），1 个汉字算 1 个字符，大约 0.14 元 / 600 字。新版 API Key 实际扣的是控制台里开通的那一档：资源包预付，或按合成字符后付费。新账号开通「豆包语音合成模型2.0」时，控制台写明有 2 万字符试用。后付费单价以控制台为准，不要把字数包标价当成 2.0 字符版的唯一账单。

## 不在绑定范围内

Fish Audio s2.1-pro 按字节大约 0.027 美元 / 600 个汉字，但要海外账号，免费模型只适合测试。这份 skill 不引导去绑 Fish，也不引导去绑 ListenHub。
