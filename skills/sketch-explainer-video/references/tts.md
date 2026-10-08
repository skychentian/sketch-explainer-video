# 配音：使用者自己的 MiniMax Key

核对日期：2026-10-08。价格以各家当时的官方页面为准，改价后以控制台为准。

## 默认

`speech-2.8-turbo`，国内站 `https://api.minimax.cn/v1/t2a_v2`。

选它是因为这段流水线要的是「按原文朗读的中文旁白」，合成之后用本地识别对齐，不依赖厂商时间戳。Turbo 的中文自然度够做解说，而一段大约 600 字的口播大约 0.24 元。更好听时加 `--model speech-2.8-hd`，同一把 Key，大约 0.42 元。

官方价（https://platform.minimax.cn/docs/pricing/overview ）：

| 模型 | 单价 | 汉字怎么算 | 约合每千汉字 | 约 600 字 |
| --- | --- | --- | --- | --- |
| speech-2.8-turbo | 2.00 元/万计费字符 | 1 个汉字 = 2 个计费字符 | 0.40 元 | 0.24 元 |
| speech-2.8-hd | 3.50 元/万计费字符 | 同上 | 0.70 元 | 0.42 元 |

英文、标点、空格各算 1 个计费字符。同步接口单次少于 10000 字。

## 为什么不默认别的

| 方案 | 官方口径 | 约 600 个汉字 | 不作为默认的原因 |
| --- | --- | --- | --- |
| Fish Audio s2.1-pro | 15 美元 / 百万 UTF-8 字节（docs.fish.audio，2026-10-02）。汉字通常 3 字节 | 约 0.027 美元 | 单价更低，但要海外账号；免费模型只适合开发测试，不用于对外成片 |
| 豆包语音合成大模型 | 字数包页面：10 万字 22.50 元（火山引擎产品页标价 45 元）。1 个汉字算 1 个字符 | 约 0.14 元 | 音质同属第一档，但要单独建应用、配 AppId 和 Token，不是一把 Key 能绑上 |
| ListenHub OpenAPI | 10 分钟文字转语音约 40 积分（listenhub.ai 定价页）。积分换算人民币未在该页给出 | 看不清 | 旧版 skill 走的是登录账号。公开技能不再使用制作者的登录态 |

## 绑定

Key 只放两处之一：环境变量 `MINIMAX_API_KEY`，或 `~/.config/sketch-explainer-video/minimax.key`（`bind_tts.sh` 会写成权限 600）。

国际站 Key 配 `MINIMAX_API_HOST=https://api.minimax.io`。

没有 Key 时脚本直接退出，并打印申请步骤。不要为了试听去调用接口。

## 音色

默认温柔学姐 `Chinese (Mandarin)_Gentle_Senior`。新闻女声 `Chinese (Mandarin)_News_Anchor`。温润男声 `Chinese (Mandarin)_Gentleman`。

完整列表：https://platform.minimax.cn/docs/faq/system-voice-id

旧的 ListenHub 音色 ID（晓曼 `chat-girl-105-cn`、高晴、苏哲）不能再传给这个接口。
