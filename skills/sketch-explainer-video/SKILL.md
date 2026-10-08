---
name: sketch-explainer-video
description: 把一段中文口播文案做成「简笔画手写风」竖屏解说视频（米白点阵纸、黑色手写字、黄色荧光笔、红色 ✓✗？、线条图标逐笔画出，MiniMax 或豆包按原文配音再逐字对齐，底部手写字幕，1080×1920 MP4）。只要用户说“简笔画视频/手绘风视频/白板动画/笔记风口播视频/把这段口播做成视频/按上次兔宝宝那种风格做视频/批量把脚本做成视频”，或给出口播稿+想要知识科普类竖屏短视频（抖音/视频号/小红书），都用这个 skill，即使没提“简笔画”三个字。配音必须用使用者自己的 MiniMax 或豆包 API Key。两家都没绑定就先停下来，引导对方绑定其中一家，不要索要 Key。支持换音色与多条批量并行。不用于：剪辑真人拍摄素材、数字人口播、PPT。
---

# 简笔画口播视频

成品长这样：每句话念到哪，画面就在哪一笔一笔写出来——字从左往右“写”出、关键词被荧光笔划过、图标逐笔画出、✓✗ 弹出；每个画面讲一个意思，随配音切换；底部一行手写字幕。参考图：`assets/style-ref.png`。

整个流程里**只有“设计画面”需要你动脑**，其余全部是脚本：配音、识别、逐字对齐、引擎、检查、渲染。照步骤走，别跳过检查。

## 前置条件（第一次用先确认）
- 使用者已经绑定 **MiniMax 或豆包** 其中一把 Key。两把都没有时**先停**，把下面的申请步骤告诉对方，让对方自己绑定。不要合成，不要索要 Key 原文
- `coli`（本地语音识别）、`ffmpeg`、`node/npx`、`python3`
- macOS：自动使用系统自带「手札体」；其他系统给 `--font 某中文手写字体.ttf`
- 首次运行会在 `~/.cache/sketch-explainer-video/venv` 装 fonttools
- 检查和渲染固定用 `hyperframes@0.8.117`

## 绑定配音

线上只引导绑定这两家，两家都没绑就停下来，把步骤交给对方自己做：

1. **MiniMax**（默认。两家都绑了时用这一家）：打开 https://platform.minimax.cn ，进入「账户管理 → 接口密钥」创建 API Key。国际站用 https://platform.minimax.io ，并设置 `MINIMAX_API_HOST=https://api.minimax.io`。然后执行 `bash <skill>/scripts/bind_tts.sh minimax`。
2. **豆包语音**：打开 https://console.volcengine.com/speech/new ，创建 API Key，并开通「豆包语音合成模型2.0」。然后执行 `bash <skill>/scripts/bind_tts.sh doubao`。

输入时不显示，Key 只留在本机，不要贴进对话。价格和音色见 `references/tts.md`。绑好后再建工程。已有 mp3 时用 `--audio`，不要重新合成。指定一家用 `--provider minimax` 或 `--provider doubao`。

## 流程

### 1. 建工程（配音 + 对齐一步到位）
```bash
<skill>/scripts/new_video.sh <工程目录> <口播文案.txt> --title "视频标题"
```
- 文案**一字不改**，存成 txt 传进去。脚本按原文朗读，再用本地识别对齐。
- 已有配音时不要重复生成：`--audio 已有.mp3`。
- 结束时看输出里的 `matched x/y`：≥95% 正常（没对上的多是同音字，不影响）；明显偏低说明配音和文案不是同一份。
- 产物：`sentences.txt`（每句开始秒数）、`assets/timing.js`、`index.html`（引擎已就位，留有 `<!--SCENES-->`）。

音色（`--speaker`）：MiniMax 默认温柔学姐 `Chinese (Mandarin)_Gentle_Senior`，也可换 `Chinese (Mandarin)_News_Anchor`、`Chinese (Mandarin)_Gentleman`。豆包默认小何 2.0 `zh_female_xiaohe_uranus_bigtts`，也可换 Vivi 2.0 `zh_female_vv_uranus_bigtts`、云舟 2.0 `zh_male_m191_uranus_bigtts`。不要传 ListenHub 的音色 ID。

### 2. 切分镜（写 STORYBOARD.md）
读 `sentences.txt`，把全片切成 **8–13 个画面**，每个 6–16 秒：
- 切点 = 某句开始时间 **− 0.15 秒**；第一个画面从 0 开始；最后一个画面结束于 index.html root 的 `data-duration`（= 配音结束 + 1 秒）；相邻画面首尾严格相接。
- 每个画面一句话能说清“这帧讲什么”，配一个主视觉。先写成表：`画面 | 起止秒 | 画面内容 | 锚定短语`。
- 长句（>16 秒）可以在句中切，切点取那个字的时间 − 0.15。

### 3. 写画面
先读 `references/components.md`（组件库：标题组、章节胶囊、链条、对比、≠、清单、步骤、日历、房间叠加、收尾、图标），再挑一个最接近的完整示例读一遍：
- `references/examples/event-overview.html` —— 事件始末 / 分章节讲事实
- `references/examples/relationship-chain.html` —— 谁和谁什么关系 / 供应链
- `references/examples/step-checklist.html` —— 几步法 / 实用清单

然后在 `index.html` 的 `<!--SCENES-->` 处插入所有 `<section>`。画面要**按这条口播自己设计**：示例只用来学写法，不要去翻本机其他视频工程复制它们的画面——别的工程对应的是别的口播和时间点，照抄会让锚点和节奏全错，也等于没做。**不要改 `<script>` 引擎**；需要新样式就在 `<style>` 末尾追加。

**动画怎么声明**（值是口播里的短语，引擎在 `data-from` 之后找它，念到那个字时开始动）：

| 属性 | 效果 | 放在 |
|---|---|---|
| `data-w` | 从左往右手写擦出 | 块元素，或带 `class="ib"` 的 span |
| `data-d` | 逐笔画出所有线条；`data-dur` 调每笔秒数 | `<svg>` |
| `data-h` | 荧光笔划过 | `class="hl"` 的元素 |
| `data-p` | 弹出（✓✗？≠、章节胶囊） | 带 `.ib` 的 span |
| `data-f` / `data-dim` | 淡入 / 变淡 | 任意块 |

值的写法：`"短语"` · `"短语|-0.4"`（提前 0.4 秒）· `"@0.2"`（画面开始后 0.2 秒）。

**画面原则（以及为什么）**
- **画面文字只能来自口播文案**，可以截短、可以把“没有任何一份”画成“0 份”，但不能加文案外的事实、数字、品牌判断——这类视频常涉及真实品牌和争议，画面多一句话就可能出事实错误。
- **逐个出现、跟着嘴走**：元素锚在它对应的那几个字上。一开场全摆出来的画面，观众会先看完再走神。
- **最后一个动画要在切走前 ≥0.5 秒播完**：否则荧光笔/✓ 刚出来就被下一帧切掉，等于没有。锚在句尾的东西最容易踩坑，往前挪。
- **内容只放 top 120–1480px**：下面是字幕带和抖音底部 UI。
- **画面要满、要有图**：内容纵向铺满 150–1400px（主视觉放大到画面宽度的 60–85%），每帧至少一个图形（图标 / 方框 / 对比 / 链条 / 示意图），不要只有几行小字挤在上半屏——手机上看，空一半的画面显得廉价、信息也不够。`check.py` 会拦下半屏空白的画面。
- **风格克制**：黑线 + 黄荧光 + 少量红；红色只给 ✓✗？≠、圈、警示词。不用 emoji、照片、logo、人像。
- 字幕：超过 16 字的句子要在 `assets/cap_breaks.js` 里给断点 `window.CAP_BREAKS = ["从这里另起一行的短语", …]`，断在词与词之间（冒号不是自动切分点，含冒号的长句尤其要加）。`check.py` 会把需要断的句子列出来。

### 4. 检查（反复跑到全过）
```bash
<skill>/scripts/verify.sh
```
它依次做：字体子集 → `check.py`（锚点是否存在、句尾动画是否被切、画面是否衔接、字幕是否超长、有没有压进字幕带）→ hyperframes lint/check → 截图（每个画面开始后 1.2 秒 + 结束前 0.4 秒）→ `density.py` 量每帧结束时内容铺到多低（<1000px 算下半屏空，空帧多了会失败）。
- `check.py` 和 `density.py` 的 ✗ 必须全部修掉：前者按引擎真实计时算，后者是量截图得出的，都不是建议。
- **打开 `snapshots/contact-sheet*.jpg` 亲眼逐张看**：重叠、出框、字折行挤到别的字上、图标认不出、画面大片空白。脚本发现不了“看不懂”，只有你看得出来。改完再跑 verify。
- lint 里 `nested_structure` / `track_too_dense` 警告可忽略。

### 5. 渲染与交付
```bash
<skill>/scripts/render.sh      # → renders/video.mp4，约 2–4 分钟
```
交付时说清：成片路径与时长、画面数、contact sheet 路径、自检修了什么、画面上哪些文字是你概括的（非原句）。

## 常见坑
| 现象 | 原因 → 做法 |
|---|---|
| 引擎报 phrase not found / check 报短语找不到 | 短语必须与文案逐字一致（含空格如 `9 月中旬`、全角标点）；且要在 `data-from` 之后出现 |
| 元素没有擦出效果 | `data-w` 放在了普通 inline span 上 → 加 `class="ib"` |
| 大字折成两行压到下面 | 缩小字号或加 `white-space:nowrap`，或拆成两个块 |
| 画面一开场全出现了 | 锚点短语在更早位置被匹配 → 换一个本画面内唯一的短语 |
| 多条视频同时建工程 | 可以并行，识别步骤脚本自带排队锁 |

## 批量做多条
见 `references/batch.md`：统一抓文案 → 并行生成配音 → 各自建工程 → 每条一个子任务写画面 → 统一验收 → 交付。
