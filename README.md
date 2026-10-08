# 简笔画口播视频

把一段中文口播，做成米白点阵纸、黑色手写字、黄色荧光笔的竖屏解说视频（1080×1920）。字和图跟着配音一笔一笔出现。

配音仍用 ListenHub 的晓曼等音色，按原文朗读。每个使用者自己申请 API Key，再在本机绑定，不使用别人的登录账号。

## 安装

```bash
npx -y skills add skychentian/sketch-explainer-video -g --all
```

装好后，把口播文案交给 Agent，并说「按简笔画口播视频做」。

## 先绑定自己的配音 Key

1. 打开 https://listenhub.ai/settings/api-keys ，创建一把 API Key。
2. 在自己的电脑上绑定。输入时不会显示，Key 只留在本机，不要贴进对话：

```bash
bash ~/.claude/skills/sketch-explainer-video/scripts/bind_tts.sh
```

如果 skill 装在别的目录，用那个目录里的 `scripts/bind_tts.sh`。

不要用 `listenhub auth login` 代替。登录态用的是当前这台电脑上的账号，公开技能不走这条路。

默认音色是晓曼。官方定价页写的是 10 分钟文字转语音大约 40 积分，积分换成人民币的价格该页没有给出。和其他语音的单价对照在 `skills/sketch-explainer-video/references/tts.md`。

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
