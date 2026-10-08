# 简笔画口播视频

把一段中文口播，做成米白点阵纸、黑色手写字、黄色荧光笔的竖屏解说视频（1080×1920）。字和图跟着配音一笔一笔出现。

配音不走制作者的账号。每个使用者自己去 MiniMax 申请 API Key，再在本机绑定。

## 安装

```bash
npx -y skills add skychentian/sketch-explainer-video -g --all
```

装好后，把口播文案交给 Agent，并说「按简笔画口播视频做」。

## 先绑定自己的配音 Key

1. 打开 https://platform.minimax.cn ，注册后进入「账户管理 → 接口密钥」，创建一把 Key。
2. 在自己的电脑上绑定。输入时不会显示，Key 只留在本机，不要贴进对话：

```bash
bash ~/.claude/skills/sketch-explainer-video/scripts/bind_tts.sh
```

如果 skill 装在别的目录，用那个目录里的 `scripts/bind_tts.sh`。

国际站账号（https://platform.minimax.io ）还要加一行：

```bash
export MINIMAX_API_HOST=https://api.minimax.io
```

## 默认用哪一家

默认模型是 MiniMax `speech-2.8-turbo`。

官方价是 2 元 / 万计费字符，1 个汉字算 2 个计费字符，大约 0.4 元 / 千汉字。一段约 600 字的口播大约 0.24 元。想要更好听，对 Agent 说用 `speech-2.8-hd`，大约 0.42 元。

Fish Audio 按字节算更便宜，豆包的字数包单价也更低，但一个要海外账号，一个要单独建应用。这个 skill 要的是「一把 Key 就能按原文朗读」。对照写在 `skills/sketch-explainer-video/references/tts.md`，价格核对日是 2026-10-08。

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
