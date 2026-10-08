# 画面组件库（复制后改文字与锚点即可）

画布 1080×1920。内容区 **top 120–1480px**，1540–1700px 是字幕带，不放任何东西。
每个画面外壳固定：
```html
<section id="s03" class="clip scene" data-start="19.47" data-duration="10.92" data-track-index="1" data-from="该画面第一句开头几个字"><div class="stage">
  …组件…
</div></section>
```
锚点写法：`data-w="口播短语"`、`data-w="短语|-0.4"`（提前 0.4 秒）、`data-w="@0.2"`（画面开始后 0.2 秒）。
一个画面放 1 个主视觉 + 2–4 个辅助元素，自上而下排，相邻块 top 间隔 ≥ 字号×1.5。

## 目录
1 标题组 · 2 章节胶囊 · 3 纵向链条 · 4 两栏对比 · 5 大字 ≠ 对比 · 6 打勾清单 · 7 编号步骤 · 8 图标说明行 · 9 日历红圈 · 10 房间叠加 · 11 收尾结论 · 12 图标库

## 1 标题组（小灰字 + 两行大字 + 荧光）
```html
<div class="a k" style="top:170px"><span class="ib" data-w="@0.15">最近大家都在刷</span></div>
<div class="a h" style="top:280px"><span class="ib" data-w="兔宝宝毛毛姐"><span class="hl" data-h="兔宝宝毛毛姐|0.9">兔宝宝毛毛姐</span></span></div>
<div class="a h" style="top:430px"><span class="ib" data-w="事件">事件</span></div>
```
大字 `.h` 112px 每行约 8 字；超过就把字号改小（`style="font-size:94px"`）或拆行。多行一定拆成多个 `.a` 块，不用 `<br>`。

## 2 章节胶囊（首先/其次/最后、第一步…）
```html
<div class="a fx" style="top:150px"><span class="chap" data-p="@0.1">① 柜子从哪来</span></div>
```
同一章节后续画面照抄这一行但**去掉 data-p**（静态显示）。

## 3 纵向链条（A —动作→ B）
```html
<div class="a col" style="top:370px">
  <div class="box t" data-w="与毛毛姐公司">毛毛姐的公司</div>
  <div class="fx s" style="gap:20px"><svg data-d="签合同" viewBox="0 0 20 46" style="width:60px;height:140px"><path class="i" d="M10 2v40M3 35l7 8 7-8"/></svg><span class="ib" data-w="签合同">签合同</span></div>
  <div class="box t" data-w="北京的装修公司"><span class="hl" data-h="北京的装修公司|0.9">北京装修公司</span></div>
</div>
```
延续上一帧的节点：把它照抄在顶部并加 `style="opacity:.45"`，不加动画。

## 4 两栏对比（左右各一组，✓ / ✗）
```html
<div class="a" style="top:520px;left:40px;right:40px;display:flex;justify-content:space-between;align-items:flex-start">
  <div class="col s c" style="width:470px;gap:20px"><span class="ib" data-w="左边短语">左标题</span><div class="box s" data-w="左边短语|0.4">左内容</div><span class="ib red" data-p="左边短语|0.8">✓</span></div>
  <div class="col s c" style="width:470px;gap:20px"><span class="ib" data-w="右边短语">右标题</span><div class="box s" data-w="右边短语|0.4">右内容</div><span class="ib red" data-p="右边短语|0.8">✗</span></div>
</div>
```

## 5 大字 ≠ 对比（全片核心认知，一条片子最多用 1–2 次）
```html
<div class="a h" style="top:290px;font-size:108px"><span class="ib" data-w="房间空气超标">房间空气超标</span></div>
<div class="a h red" data-layout-allow-overlap style="top:420px;font-size:180px;line-height:1.1"><span class="ib" data-p="不能直接等同">≠</span></div>
<div class="a h" style="top:620px;font-size:108px"><span class="ib" data-w="板材不合格"><span class="hl" data-h="板材不合格|0.8">板材不合格</span></span></div>
```

## 6 打勾清单
```html
<div class="a t col" style="top:440px;align-items:flex-start;gap:56px;left:150px">
  <div class="fx" style="gap:22px"><span class="ib red" data-p="公证拆除">✓</span><span class="ib" data-w="公证拆除">公证拆除</span></div>
  <div class="fx" style="gap:22px"><span class="ib red" data-p="公证取样">✓</span><span class="ib" data-w="公证取样">公证取样</span></div>
</div>
```
否定项把 ✓ 换 ✗。✓/✗ 必须锚在各自那一项的口播词上，逐条出现。

## 7 编号步骤（四步法 / 三件事总览）
```html
<div class="a fx" style="top:560px;gap:28px">
  <span class="ib" data-p="四步|0.2"><svg viewBox="0 0 40 40" style="width:110px;height:110px"><circle class="i" cx="20" cy="20" r="17"/><text x="20" y="27" font-size="20" text-anchor="middle">1</text></svg></span>
  <span class="ib" data-p="四步|0.4"><svg viewBox="0 0 40 40" style="width:110px;height:110px"><circle class="i" cx="20" cy="20" r="17"/><text x="20" y="27" font-size="20" text-anchor="middle">2</text></svg></span>
</div>
```
每一步单独成一帧时，用章节胶囊 `第一步 · 查门店` 作标题。

## 8 图标 + 说明行
```html
<div class="a fx s" style="top:720px;justify-content:flex-start;left:150px"><svg data-d="北京办公室" viewBox="0 0 60 60" style="width:130px;height:130px"><rect class="i" x="8" y="10" width="44" height="42" rx="3"/><path class="i" d="M30 10v42M8 30h44"/></svg><span class="ib" data-w="北京办公室">北京办公室 · 定制柜</span></div>
```

## 9 日历红圈（日期类结论）
```html
<div class="a" style="top:280px;left:216px;right:216px;height:605px">
  <svg data-d="这份权威|0.2" data-dur="0.5" viewBox="0 0 120 112" style="position:absolute;inset:0;width:648px;height:605px"><rect class="i" x="10" y="14" width="100" height="90" rx="6"/><path class="i" d="M10 36h100M34 6v16M86 6v16"/><text x="60" y="30" font-size="13" text-anchor="middle">10 月</text><text x="60" y="84" font-size="42" text-anchor="middle" font-weight="700">12</text></svg>
  <svg data-d="10 月 12 日|0.2" data-dur="0.8" viewBox="0 0 120 112" style="position:absolute;inset:0;width:648px;height:605px"><path class="r" d="M92 60c-2-16-18-24-34-23-18 1-32 12-32 28s16 26 34 25c18-1 32-10 32-26-1-6-4-10-8-13"/></svg>
</div>
```
先画日历、后画红圈 → 两个 svg 叠在一个定高容器里。

## 10 房间 + 逐个叠加的因素
```html
<div class="a" style="top:520px"><svg data-d="房间里" data-dur="0.6" viewBox="0 0 168 124" style="width:900px;height:664px"><path class="i" d="M6 40 84 4l78 36v80H6Z"/><rect class="i" x="22" y="56" width="40" height="56"/><path class="i" d="M42 56v56M22 76h40"/></svg></div>
<div class="a s" style="top:760px;left:auto;right:110px;width:340px;line-height:1.75">
  <div data-w="封边胶水">+ 封边胶水</div><div data-w="软装">+ 软装</div><div data-w="地板">+ 地板</div>
</div>
<div class="a t c red" style="top:1230px"><span class="ib" data-w="封闭空间">封闭空间 → 空气超标</span></div>
```

## 11 收尾结论（安抚 + 唯一观察点）
```html
<div class="a h" style="top:290px"><span class="ib" data-w="不用慌">不用慌</span></div>
<div class="a h" style="top:440px"><span class="ib" data-w="不用急着站队">不用站队</span></div>
<div class="a" style="top:800px"><svg data-d="分水岭" data-dur="1.0" viewBox="0 0 168 24" style="width:900px;height:129px"><path class="i" d="M4 12c30-8 50 8 80 0s50-8 80 0"/></svg></div>
<div class="a t c" style="top:1070px"><span class="ib" data-w="10 月 12 日前后"><span class="hl" data-h="检测数据">10.12 公证送检数据</span></span></div>
```

## 12 图标库（放进 `<svg data-d="…" viewBox=… style="width:…;height:…">`，class `i` 黑线 / `r` 红线）
| 图标 | viewBox | 内容 |
|---|---|---|
| 向下箭头 | 0 0 20 46 | `<path class="i" d="M10 2v40M3 35l7 8 7-8"/>` |
| 向右箭头 | 0 0 46 20 | `<path class="i" d="M2 10h40M35 3l8 7-8 7"/>` |
| 警告三角 | 0 0 50 50 | `<path class="r" d="M25 5 46 43H4Z"/><path class="r" d="M25 19v12M25 37v1"/>` |
| 放大镜 | 0 0 50 50 | `<circle class="i" cx="21" cy="21" r="14"/><path class="i" d="M31 31l13 13"/>` |
| 文档 | 0 0 40 50 | `<path class="i" d="M4 2h22l10 10v36H4Z M26 2v10h10 M10 22h20M10 30h20M10 38h14"/>` |
| 柜子 | 0 0 60 68 | `<rect class="i" x="6" y="4" width="48" height="60" rx="2"/><path class="i" d="M30 4v60M24 38v6M36 38v6"/>` |
| 房子 | 0 0 60 56 | `<path class="i" d="M4 24 30 4l26 20v30H4Z"/><path class="i" d="M12 34c6-4 10 4 16 0s10-4 16 0"/>` |
| 喇叭 | 0 0 50 50 | `<path class="i" d="M6 20h10l20-12v34L16 30H6Z M16 30l4 12"/>` |
| 小人 | 0 0 40 70 | `<circle class="i" cx="20" cy="12" r="9"/><path class="i" d="M20 21v24M20 28l-12 9M20 28l12 9M20 45l-10 20M20 45l10 20"/>` |
| 烧瓶 | 0 0 40 50 | `<path class="i" d="M15 4h10M17 4v16L5 44h30L23 20V4"/>` |
| 手机 | 0 0 34 56 | `<rect class="i" x="3" y="3" width="28" height="50" rx="5"/><path class="i" d="M13 45h8"/>` |
| 打勾圆 | 0 0 40 40 | `<circle class="r" cx="20" cy="20" r="17"/><path class="r" d="M11 20l6 7 12-14"/>` |

自己画新图标：只用直线/弧线，8–15 笔以内，线条不交叠成团；画完在截图里确认“一眼能认出是什么”，认不出就换成文字方框。
