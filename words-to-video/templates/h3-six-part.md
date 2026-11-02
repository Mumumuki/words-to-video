# 第八步｜H3 六段式提示词模板

- 项目：
- 段落：
- 时长：≤15 秒（与本平台单次生成 1:1）
- 风格卡 ID / 版本：
- 参考图映射：见本段填表包 `sheet.md`

> **六段式是一个字符串，不是六个独立输入框。** 六个字段名依次写在同一段文本里，格式为 `字段名:` 换行接内容。整体粘贴进 ComfyUI 的文本节点即可，不得拆成多份提交。
>
> 目标读者是模型，不是人。**具体名词优先于形容词**：写"黑色双排扣西装外套、袖口露出一截金色表带"，不写"衣着讲究、气质不凡"。

---

## 一、字段顺序（不可调换、不可省略）

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

缺任一字段，模型按残缺输入处理，锁定强度明显下降。**没有内容也要写，写 `N/A` 或"无"。**

> **`<Continuity>` 不是第七字段**，它是 `retention_analysis` 里的最后一行，写在那个字段内部。加行不改字段数——六个字段名的顺序与数量一律不动。

---

## 二、参考图顺序表（放在六段式之前，不属于提示词正文）

每段开头先列本段实际用到的图。**只列本段在用的**，未用到的槽位不写。

| 编号 | 资产 | 在本段的作用 |
|---|---|---|
| Picture 1 | 角色01-造型A | 男主外型 |
| Picture 2 | 场景01 | 空间全景 |

> 编号整集统一，见 `references/platforms/comfyui-minimax.md`。本表供人工核对，不粘贴进文本节点。

---

## 三、各字段写法

### 1. `subject_definitions`

每个角色一个 `<Subject N>`，每个场景一个 `<Subject N>`。编号与 Picture 一一对应。

**一个角色的标准写法（五项齐全）：**

```text
<Subject 1> is [姓名] — FACE from <Picture 1> ([发型、眼部、眼镜、妆容、配饰等固定面部特征]).
HAIR LOCKED as [具体发型，含否定项].
OUTFIT LOCKED as [拆成部件的服装描述：外套领型+袖长+扣型+下装版型与长度+袜/鞋，含颜色与材质].
EXPLICITLY NOT [参考图中不需要的服装] from <Picture 1> — the reference image's [该服装] must be FULLY IGNORED and REPLACED by the [锁定服装] above.
POSITION LOCKED: [具体位置，含与他人/物体的空间关系] [不移动则写明 NEVER leaves] .
VOICE: [音色描述] , [语速区间]. (S1)
```

**一个场景的标准写法：**

```text
<Subject 5> is the [场景名] in <Picture 5>: [关键空间元素列表，写清主要物件与门窗的相对位置关系].
The [核心空间锚点] is the central spatial reference, separating [人物A] ([方位]) from [人物B] ([方位]).
[时间与光位：白天自然光/夜间冷白顶灯/…]
```

**末尾补一行绑定关系，不可省：**

```text
<Picture 1> ref <Subject 1>'s face. <Picture 5> ref <Subject 5>.
```

**背景人物**用纯文字，不占 Subject 标签：

```text
Background customers are text-defined only, no reference image needed, do not occupy Subject or Picture labels.
```

> 为什么服装要拆成部件：参考图是半身，腰以下没有信息。只写"黑色套装"，模型会把下身自由发挥。写"黑色锥形西裤、九分长度、黑色低跟皮鞋"，它才有的可依。

### 2. `summary`

开头加 `[reference generation]` 前缀，随后：

1. **重申所有人物锁定**（大写关键词），一行一人；
2. **重申空间锚点**；
3. **按时间顺序概括每镜**：时间区间 + 核心动作 + 台词字数与语速。

```text
summary:
[reference generation] 15s [段落标题]. [姓名A] LOCKED: [服装简述]. NOT [参考图不需要的服装]. [姓名B] LOCKED: [服装+发型]. The [空间锚点] is always between them. 0-3s: [动作] + [台词 X 字, Y 字/秒]. 3-6s: ...
```

> 这一段是给模型的第二次提醒。第三次加固在 `detailed_description`。**三次都要写，不是冗余。**

### 3. `retention_analysis`

一人一行、一场景一行，标明保留了什么、替换了什么。**最后固定加一行 `<Continuity>`**，声明本段首帧接续上一段的哪一帧（首段写 `none`），写法见本节末。

```text
retention_analysis:
<Subject 1> (appears in Shot 1, Shot 3, Shot 5): fully_preserved - face from <Picture 1>; OUTFIT FULLY PRESERVED as [简述]; [被替换项] FULLY REPLACED; POSITION FULLY PRESERVED as [位置]; [动作/情绪] new.
<Subject 5> (all shots): fully_preserved - [场景简述], spatial layout consistent throughout.
<Picture 1-5>: fully_preserved.
<Continuity>: first frame continues the last frame of P01 (handoff/P01-last.png) — same outfit, same position, same light, same camera side.
```

**本段与上一段是两次生成，但必须接得上。** 承接写在 `retention_analysis` 末尾这一行 `<Continuity>`，**不写进 `detailed_description`**——不要在画面描述里写「接着上一段」「延续前面的画面」，模型手里没有上一段的画面，那种话是空指代。

- **首段**写 `<Continuity>: none — this is the opening segment.`
- **纯参考模式（L2）**：这一行是给人看的对齐声明，模型读不懂也无害；真正的承接靠 `subject_definitions` 完整重申服饰与位置、故事板首格与上段末格构图一致、出片后比对 `handoff/` 两帧。
- **首帧驱动（L1）**：这一行正是模型需要的锚点，同时把 `handoff/P01-last.png` 接进本段首帧槽。

> **两件事不要混**：服装、发型、位置在 `subject_definitions` 里**必须完整重申**（不许写"同前""照旧"）；而承接关系**必须显式声明**在 `<Continuity>` 里。前者防漂移，后者防接不上，不能用一个代替另一个。

### 4. `detailed_description`

**结构固定为四块，顺序不可变：**

**(a) 风格句（第一句必写）**

```text
The target video is in [风格名] style. Visual characteristics: [光线性质、对比度、色彩倾向、颗粒、肤质、景深、氛围].
```

古典项目写"素朴写实、暖灰低饱和、粗陶素木手作痕迹"；现代写"数字实拍、低照度、轻微高感噪点"；科幻写"工业压铸质感、冷白与低频光源、界面光"。**其余题材同构写：媒介 + 光源性质 + 材质痕迹三件，不堆形容词**（如年代戏＝"胶片实拍、单一白炽灯为主、铁与水泥的使用痕迹"）。取值一律来自风格卡，不新造。

**(b) 曝光与基调统一前缀（第二句必写）**

```text
Exposure unified across all shots — mid-grey baseline, shadows retain detail, no shot darker or greener than another.
```

这一句是防"六镜色温不统一"的唯一有效手段。**少了它，每镜各自的局部描述会把整体基调冲掉。**

**(c) 锁定重申（大写）**

```text
[姓名A] OUTFIT LOCKED THROUGHOUT: [服装简述]. EXPLICITLY NOT [不需要的服装]. [姓名B] LOCKED: [服装+发型]. [位置重申].
```

**(d) 逐镜描写**

每镜一行，**时间码必写**，镜头号与本段分镜表一致：

```text
[Shot 1] At 00:00.000, [景别与机位]. [画面内容，含 <Subject N> 的服装关键词重复、动作、姿态、可见环境细节]. [运镜：起幅→运动→落幅]. [若有台词：<Subject 1> (S1) says, [语速]字/秒, <d>[Chinese] [台词原文]。</d> [若有气口：(pause ~0.8s at ——)]]
```

硬规则：

- **Shot 数 = 本段分镜表的镜头数**，不按关键帧数算。一镜多帧时，该 Shot 的时间码跨越多帧区间，画面内容取该镜的整合描述。**本段 Shot 数至多 6**，且每个镜头切换点必须落在格分界线上（每镜至少占一格）——这是第七步规划时就定下的，本步不放大也不重排。
- 每个出现人物的镜头，**都要重复一次服装关键词**，不能只在开头写。
- 有台词的镜头，说话人必须是画面主体。要让别人入画，只能过肩或背景虚化，**动嘴的只能是说话人**。
- 时间码用 `MM:SS.mmm`，**从本段起始时间码起**（首段为 `00:00.000`，`P02` 起是它自己的起点），与本段分镜表逐镜对应；全片时间码连续不归零，不按段落重算。
- 最后一镜以画面描述收尾，不写"段落到此结束"之类的收束语。

### 5. `overall_soundscape`

按镜头顺序写环境音与拟音，写具体声源与位置，不用"氛围音"代替。

```text
overall_soundscape:
[整体环境音一句]. Shot 1: [具体音效]. Shot 2: [具体音效]. ... Voice only from <Subject N> (Sx); no other dialogue.
```

**本平台默认无背景音乐。** 所有音乐性内容不写在这里，见下一字段。

### 6. `non_diegetic_music`

```text
non_diegetic_music:
N/A
```

除非项目定义里明确要求配乐，**一律写 `N/A`**。写了内容就会真的加 BGM，而 BGM 会在后期无法去掉。

---

## 四、三层加固法（本平台最重要的方法）

服装与发型漂移是这类生成的头号问题，根因只有一个：**只在开头写了一次，模型后续自由发挥。**

三层加固指同一件事在三个位置各写一遍，且 `detailed_description` 内**每镜再重复**：

| 层 | 位置 | 写法 |
|---|---|---|
| 一 | `subject_definitions` | 拆到部件的具体描述 ＋ `LOCKED` ＋ `EXPLICITLY NOT [参考图服装]` |
| 二 | `summary` 开头 | 大写关键词重申，一行一人 |
| 三 | `detailed_description` 开头 | 大写 `OUTFIT LOCKED THROUGHOUT` |
| 加 | `detailed_description` 每镜 | 该镜人物出现即重复一次服装关键词 |

**错误写法**（模糊，模型必然自由发挥）：

```text
<Subject 1> is Lin in <Picture 1>, dark green vest, glasses.
```

**正确写法**：

```text
<Subject 1> is Lin — FACE from <Picture 1> (low ponytail, loose front strands, faint dark circles, no makeup). HAIR LOCKED as a low ponytail tied at the nape, NOT loose, NOT high. OUTFIT LOCKED as a dark green convenience-store vest with a single left-chest pocket, worn OVER a black long-sleeve crew-neck top, black straight-leg trousers, black low-top work shoes, a badge on a lanyard turned back-side-out so no name is visible. POSITION LOCKED: standing BEHIND the black checkout counter, NEVER walks around it. VOICE: quiet low female voice, restrained, 3-4 字/秒. (S1)
```

差别不在长短，在于**每一项都具体到无法自由发挥**。

---

## 五、位置锁定法

人物跑到桌外、座位每段不同，是第二号问题。四条一起用：

1. **`subject_definitions` 写位置 ＋ 否定句**：`SEATED BEHIND the desk, NEVER stands up, NEVER leaves her seat.`
2. **指定一个空间锚点**，并规定它相对机位的位置：`The desk is ALWAYS in the foreground between her and the camera.`
3. **场景 Subject 里写布局**：`desk in the CENTER, her chair BEHIND it, guest chair IN FRONT opposite.`
4. **动作描述里重申不移动**：`She does NOT stand — she reaches forward OVER the desk surface.`

多人场景**优先中景、近景**。全景会让模型自己重排座位，很难救。

需要移动时，写明路径：`she first steps sideways around the desk corner, then forward` ——不写路径就会出现穿模。

---

## 六、语速与气口

第七步已算好每镜的实际语速，本步只负责写进提示词。

```text
<Subject 1> (S1) says, 3.5 字/秒, <d>[Chinese] 你到底在等什么。</d>
<Subject 1> (S1) says, 4.2 字/秒, <d>[Chinese] 八年——一个新人七天做完了。</d> (pause ~0.8s at ——)
```

规则：

- 每句台词前标语速，与第七步一致，不现场估。
- `——` 处必有 `(pause ~0.8s at ——)`，一处一个。
- 同一镜多句台词，各自标语速，不合并。
- 台词为文言或古语时，语速取下限（2.5–3.5），并且**不要为了压时长删句**——删句属于第七步的事，第八步不得改台词内容。

---

## 七、本段自检

交付前逐项过：

- [ ] 六字段齐全、顺序正确，缺项已写 `N/A` 或"无"
- [ ] 参考图顺序表已列，只列本段在用的
- [ ] 每个角色都有 `LOCKED` 服装、`LOCKED` 发型、`POSITION LOCKED`、`VOICE` 与说话人 ID
- [ ] 需要替换参考图服装的，写了 `EXPLICITLY NOT`
- [ ] `summary` 开头重申了全部锁定
- [ ] `detailed_description` 首句是风格、次句是曝光统一前缀、第三句是锁定重申
- [ ] **每个出现人物的镜头都重复了服装关键词**
- [ ] Shot 数 = 分镜表镜头数，时间码逐镜对应，格式 `MM:SS.mmm`
- [ ] 有台词的镜头，说话人即画面主体，无"错误的人动嘴"
- [ ] 每句台词前有语速，气口处有 `pause ~0.8s`
- [ ] `overall_soundscape` 写了具体环境音与拟音，未混入音乐
- [ ] `non_diegetic_music` 为 `N/A`
- [ ] 全文无"氛围感""电影感""高级感"等无数值形容词充当内容

---

## 八、完整示例（现代悬疑 · 一段四镜）

> 示例只演示字段写法与密度，不作质量标杆。实际项目按自己的风格卡与资产编号替换。

```text
subject_definitions:
<Subject 1> is Lin — FACE from <Picture 1> (low ponytail tied at the nape, loose front strands, faint dark circles, no makeup). HAIR LOCKED as a low ponytail at the nape, NOT loose, NOT high. OUTFIT LOCKED as a dark green convenience-store vest with one left-chest pocket, worn OVER a black long-sleeve crew-neck top, black straight-leg trousers, black low-top work shoes, a badge on a lanyard turned back-side-out with no name visible. POSITION LOCKED: standing BEHIND the black checkout counter, NEVER walks around it. VOICE: quiet low female voice, restrained, 3-4 字/秒. (S1)
<Subject 2> is the man — FACE from <Picture 2> (short greying hair, stubble, deep lines around the mouth, worn expression). HAIR LOCKED as short greying hair, flat, NOT styled. OUTFIT LOCKED as a faded dark grey zip-front jacket over a grey crew-neck tee, dark worn jeans, scuffed brown work boots, a white plastic bag in his right hand. POSITION LOCKED: on the customer side of the counter, NEVER moves behind it. VOICE: low rough male voice, 2.5-3 字/秒. (S2)
<Subject 3> is the convenience store interior in <Picture 3>: three rows of shelving running lengthwise on the left, the black checkout counter along the right wall, a row of upright glass-door coolers on the far wall, a round convex security mirror mounted at the upper corner above the counter. The checkout counter is the central spatial reference, separating Lin (behind it) from the man (in front of it). Night, cold-white 6500K ceiling tubes, low-key with orange street light bleeding through the glass door.
<Picture 1> ref <Subject 1>'s face. <Picture 2> ref <Subject 2>'s face. <Picture 3> ref <Subject 3>.
Background is empty and text-defined only, no reference image needed, do not occupy Subject or Picture labels.

summary:
[reference generation] 15s 同一瓶水. LIN LOCKED: dark green vest over black long-sleeve, black trousers, badge back-side-out, low ponytail. NOT hair down. THE MAN LOCKED: faded grey zip jacket, white plastic bag, grey stubble, no styling. The black counter is always between them. 0-3s: man walks in, passes the mirror sector without looking up — no dialogue. 3-8s: Lin sets a bottle on the scanner, looks up, 6 字, 3 字/秒. 8-12s: man answers without raising his eyes, 9 字, 3 字/秒. 12-15s: man takes the bag and turns to leave.

retention_analysis:
<Subject 1> (appears in Shot 2, Shot 3, Shot 4): fully_preserved - face from <Picture 1>; OUTFIT FULLY PRESERVED as dark green vest over black long-sleeve + black trousers; hair FULLY PRESERVED as low ponytail; badge FULLY PRESERVED back-side-out; POSITION FULLY PRESERVED behind the counter; expression new.
<Subject 2> (appears in Shot 1, Shot 3, Shot 4): fully_preserved - face from <Picture 2>; OUTFIT FULLY PRESERVED as faded grey jacket + dark jeans + white plastic bag; POSITION FULLY PRESERVED on the customer side; gaze new.
<Subject 3> (all shots): fully_preserved - shelf rows, counter, coolers, convex mirror, spatial layout consistent throughout.
<Picture 1-3>: fully_preserved.
<Continuity>: none — this is the opening segment.

detailed_description:
The target video is in digital live-action documentary style. Visual characteristics: cold-white 6500K ceiling light mixed with warm orange street light from the glass door, low-key with retained shadow detail, slightly desaturated cool palette with a single warm accent, fine high-ISO grain, realistic skin texture, deep focus, unglamorous.
Exposure unified across all shots — mid-grey baseline, shadows retain detail, no shot darker or greener than another.
LIN OUTFIT LOCKED THROUGHOUT: dark green vest over black long-sleeve top, black straight-leg trousers, black low-top work shoes, badge back-side-out, low ponytail. EXPLICITLY NOT hair down, NOT a white shirt. THE MAN LOCKED: faded dark grey zip jacket, grey crew-neck tee, dark jeans, scuffed brown boots, white plastic bag. The black counter stays between them in every shot.
[Shot 1] At 00:00.000, wide full shot from inside the store facing the glass door, camera fixed at chest height. The man in his faded dark grey zip jacket pushes the door open and steps in, white plastic bag in his right hand, head slightly lowered; the round convex mirror at the upper corner reflects only empty aisle — no one in it. Cold white overhead light, orange street light spilling in behind him. Locked-off, no movement.
[Shot 2] At 00:03.000, medium shot from the customer side of the black counter. Lin, her dark green vest and black long-sleeve top clearly visible, badge back-side-out on its lanyard, low ponytail, sets a clear plastic bottle on the scanner with one hand and lifts her eyes toward the man off-frame; her other hand stops mid-air. Camera locked, slight rack focus from the bottle to her face. <Subject 1> (S1) says, 3 字/秒, <d>[Chinese] 还是这瓶?</d>
[Shot 3] At 00:08.000, tight close-up, slight high angle, from the man's front-left. Only his jaw, mouth, stubble and shoulder enter frame; his eyes stay cast down, away from every reflective surface; the edge of the black counter and the white plastic bag handle show at the bottom of frame. His faded grey zip jacket clearly visible at the shoulder. Camera fixed. <Subject 2> (S2) says, 3 字/秒, <d>[Chinese] 一样就行，不用袋子。</d>
[Shot 4] At 00:12.000, wide full shot from deep inside the store toward the glass door, camera fixed. The man in his faded grey zip jacket walks out through the glass door, back to camera, now lit only by the orange street light; the store behind him stays fully stocked with every light on; the convex mirror at the upper corner reflects an empty aisle. No camera movement.

overall_soundscape:
Steady cold fluorescent hum throughout, faint compressor drone from the coolers. Shot 1: door chime, rubber-soled footsteps, the bag rustling. Shot 2: bottle set down on the scanner, a single short beep. Shot 3: near silence, only the man's breath. Shot 4: footsteps receding, door chime, street ambience through the glass. Voice only from (S1) and (S2); no other dialogue.

non_diegetic_music:
N/A
```

---

## 九、与其他模板的分工

| 文件 | 负责 |
|---|---|
| 本文件 | 六段式怎么写 |
| `references/platforms/comfyui-minimax.md` | 平台参数、Picture 编号、填表包结构 |
| `templates/comfyui-fill-sheet.md` | 每段填表单 |
| `templates/prompt-pack.md`、`standardized-prompts.md`、`image-review.md` | **资产卡**（角色/场景/道具）的提示词与复核，与六段式无关，不要混用 |
