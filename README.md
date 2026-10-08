# 简笔画口播视频

把一段中文口播，做成米白点阵纸、黑色手写字、黄色荧光笔的竖屏解说视频（1080×1920）。字和图跟着配音一笔一笔出现。

配音不走制作者的账号。每个使用者自己绑定 **MiniMax** 或 **豆包** 的 API Key。两家都没绑定时，脚本会停下来，并写出申请步骤。

## 安装

```bash
npx -y skills add skychentian/sketch-explainer-video -g --all
```

装好后，把口播文案交给 Agent，并说「按简笔画口播视频做」。

## 先绑定自己的配音 Key

任选一家。输入时不会显示，Key 只留在本机，不要贴进对话。下面的路径换成你装好的 skill 目录里的 `scripts/bind_tts.sh`。

MiniMax（默认。两家都绑了时用这一家）：

1. 打开 https://platform.minimax.cn ，进入「账户管理 → 接口密钥」，创建一把 Key。
2. 绑定：`bash <skill>/scripts/bind_tts.sh minimax`
3. 国际站账号（https://platform.minimax.io ）再执行：`export MINIMAX_API_HOST=https://api.minimax.io`

豆包语音：

1. 打开 https://console.volcengine.com/speech/new ，创建 API Key，并开通「豆包语音合成模型2.0」。
2. 绑定：`bash <skill>/scripts/bind_tts.sh doubao`

Claude 装到默认位置时，`<skill>` 一般是 `~/.claude/skills/sketch-explainer-video`。别的 Agent 用它实际安装到的那个目录。

默认模型是 MiniMax `speech-2.8-turbo`。官方价 2 元 / 万计费字符，1 个汉字算 2 个计费字符，大约 0.4 元 / 千汉字。一段约 600 字大约 0.24 元。想更好听，对 Agent 说用 `speech-2.8-hd`，大约 0.42 元。豆包按控制台里的「语音合成2.0字符版」计费，产品页字数包曾标 10 万字 22.50 元。对照写在 `skills/sketch-explainer-video/references/tts.md`，价格核对日是 2026-10-08。

已经有 mp3 时直接交给 Agent，不要重新合成。

## 还需要本机有这些

- `coli`：本地语音识别，用来把配音和文案对齐
- `ffmpeg`
- `node` / `npx`
- `python3`
- macOS 用系统自带「手札体」。其他系统准备一个中文手写字体，交给 `--font`

画面检查和渲染使用 `hyperframes@0.8.117`。

## 边界

- 文案按原文字朗读，画面上的字也只能来自这段口播。
- 不剪真人素材，不做数字人，不做 PPT。
- Key 不会被写进这个仓库。
