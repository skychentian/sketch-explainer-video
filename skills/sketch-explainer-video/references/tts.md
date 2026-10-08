# 配音：使用者自己的 ListenHub API Key

线上这份 skill 继续用 ListenHub 的中文音色，按原文朗读。差别是每个使用者自己申请 Key，不使用别人的登录账号。

## 绑定

1. 打开 https://listenhub.ai/settings/api-keys ，创建 API Key。新注册账号有体验积分。
2. 运行 `scripts/bind_tts.sh`。Key 写到 `~/.config/sketch-explainer-video/listenhub.key`，权限 600。也可以只在当次命令前设置环境变量 `LISTENHUB_API_KEY`。
3. 没有 Key 时，建工程会停下来，并打印上面的步骤。不要改走 `listenhub auth login`。

默认音色仍是晓曼 `chat-girl-105-cn`。高晴 `gaoqing3-bfb5c88a`，苏哲 `suzhe-45bbbe54`。

合成走 `listenhub openapi tts`，把原文读成 mp3。已有 mp3 时用 `--audio`，不要重新合成。

## 积分

ListenHub 官方定价页写的是：10 分钟文字转语音大约 40 积分，新用户注册约 100 积分。该页没有给出积分换成人民币的价格，所以一条 2 分钟口播的钱数以账户里的积分流水为准。

https://listenhub.ai/docs/zh/openapi/pricing

## 和其他语音的对照

核对日期 2026-10-08。这条流水线最后仍用 ListenHub，是因为音色和「按原文朗读」已经接在现有流程上。若只比较单价，下面几家更低，但接入方式不是一把 ListenHub Key：

| 方案 | 官方口径 | 约 600 个汉字 |
| --- | --- | --- |
| MiniMax speech-2.8-turbo | 2 元/万计费字符，1 个汉字算 2 个计费字符 | 约 0.24 元 |
| MiniMax speech-2.8-hd | 3.5 元/万计费字符，汉字同样算 2 个 | 约 0.42 元 |
| Fish Audio s2.1-pro | 15 美元/百万 UTF-8 字节，汉字通常 3 字节 | 约 0.027 美元 |
| 豆包语音合成大模型 | 字数包页面 10 万字 22.50 元 | 约 0.14 元 |

Fish 的免费模型只适合开发测试。豆包要单独建应用，配的是 AppId 和 Token。
