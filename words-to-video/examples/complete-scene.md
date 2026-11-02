# 示例｜一句话 → 完整生产包（原创 · 现代清晨 · 60 秒 4 段）

> **一句话是唯一的 `[来源]`，其余全部 `[创作]`。** 本样例演示 `original` 模式怎么把一句话铺成一部能直接进 ComfyUI 的短片：S0–S14 全流程走通：G1–G3 是检查点（展示即继续），**只在 G4 停下等用户确认**。
>
> 为控制篇幅：**P01 写全**（分镜表、六段式全文、故事板映射、填表包），P02–P04 只给段落清单与每段一句概述，结构与 P01 同构。**本样例不产出实图**，只给图位、提示词要点与裁切区。
>
> 与 `adaptation` 模式的三处差异：① S0 的来源类型填 `one_line` 而不是 `poem`；② S2 没有信息表可抓，改为登记用户原话 + 待建节拍；③ S3 必须先写节拍表再落场次，不能直接从原文搭骨架。其余各步完全相同。
>
> 本样例只演示**一个题材**（四轴定位：当代／生活流＋家庭／中国城市老街沿／克制·写实·暖）。题材怎么定、怎么发散、换题材要改哪几处，见 `references/genres/taxonomy.md`——**换题材不换流程**，四道门与六段式一律不动。

---

## 输入

> 每天凌晨四点，早餐摊老板都会多煮一碗面放在角落的桌上，从来没有人吃；今天，有人坐下了。

- 用户未指定时长、题材、风格。按一句话来源的缺省建议：60 秒（56–64 可浮动）、`剧情演绎`、当下中国老街区街沿。
- 参考图：无。

---

## S0 破题与核心动作（`templates/project-brief.md`）

### 方案候选（先给 3 个，用户选定后再往下走）

> 一句话进来时按山音口径先出 3–5 个方案——**每个都是一条完整的戏剧动作，不是同一个故事的三个角度**。用户选定后，才把它的四项填进下表并锁定。

- **方案 A**：主角 老周／目标 每天把那碗面放上角落空桌／阻碍 三十年来没人碰过，今天一个陌生小女孩径直坐下／logline 一个每天多煮一碗面的老人，第一次看见有人坐到那张空桌前
- **方案 B**：主角 小女孩／目标 在没有大人同意之前吃完这碗面／阻碍 摊主盯着她，且她自己也说不清为什么非要坐这张桌／logline 一个孩子坐上了不该坐的位置，必须在被赶走之前吃完那碗面
- **方案 C**：主角 老周／目标 赶在有人坐下之前收走那碗面／阻碍 今天客人来得太早，他的手慢了一步／logline 一个守了三十年规矩的老人，今天第一次没来得及守住它

> **本样例走方案 A**（悬念由"谁来吃"驱动，全片张力最省成本）。这一步必须真的给出不同选项——**破题退化成"给一句话找借口"是弱剧本的第一根因**。

### 核心戏剧动作（破题）

| 项 | 内容 |
|---|---|
| 谁 | 老周，在街边摆了三十年早餐摊的老人 |
| 想要什么（目标） | 每天多煮一碗面、放在角落空桌上——一个没人要求他做的固定动作，他必须每天完成 |
| 被什么挡住（阻碍） | 三十年来从没人碰过那碗面；今天一个陌生小女孩径直坐下，把它拉到自己面前 |
| 代价是什么 | 规矩一旦被打破，他得在"继续等下去"和"承认要等的人不会来了"之间做出处置 |
| **logline** | 一个每天多煮一碗面的老人，在一个下雨的清晨，第一次看见有人坐到了那张空桌前 |

> 原句里"每天多煮一碗、从没人碰过"是动作，"今天有人坐下"是阻碍——**这才构成一个戏剧动作**。如果只提炼出"雨夜的早餐摊，一个老人的孤独"，那是氛围不是动作，后面每一步都会失去方向。

### 项目定义

| 字段 | 内容 | 标注 |
|---|---|---|
| 来源形态 | `original` | `[来源]` 只有一句话，无原作可忠 |
| 来源类型 | `one_line` | — |
| 项目名称 | 第二份 | `[创作]` |
| logline | 一个在街边摆了三十年早餐摊的老人，每天多煮一碗面放在角落的空桌上，从没人碰过；一个下雨的清晨，一个陌生的小女孩径直坐下，把那碗面拉到了自己面前 | `[创作]`（由原句展开） |
| 题材（四轴） | 时代世界：当代（当下中国城市）／类型片：生活流＋家庭／地域：中国·城市老街沿／调性：克制·写实·暖 | `[推断]` 原句的"早餐摊、凌晨四点"给出时代与生计方式，未提超自然 |
| 题材包 | 无（四轴已写全；`modern.md` 可带可不带，本例不带——它的三条检查项已落进 W01–W04） | `[创作]` 见 `references/genres/taxonomy.md` 第四节 |
| 时代或世界背景 | 当下中国某城市老街区，一条有早市的街沿；雨，中雨不停 | `[创作]` |
| 目标总时长 | 60 秒（56–64 可浮动） | `[创作]` 缺省建议 |
| 画幅 | 16:9 | 平台默认 |
| 视频内容类型 | `剧情演绎` | 原句有"多煮一碗"这个带动机的固定动作，成立的是因果而非情绪线 |
| 调性 | 暖、克制、雨天的湿冷；热气是唯一的暖 | `[创作]` |
| 结局倾向 | 留白 | `[创作]` |
| 必须保留 | 凌晨四点、早餐摊老板、每天多煮一碗面、放在角落的桌上、从来没有人吃、今天有人坐下 | `[来源]` 逐项对应原句 |
| 禁止出现 | 鬼魂、逝者显形、回忆闪回、旁白、字幕解释"那碗面是给谁煮的" | `[创作]` |
| 明确不做 | 不要配乐、不要旁白、不要字幕 | `[创作]`（用户未要求，按本平台默认） |

**判定说明**：原句没有第二个人、没有前史、没有解释，**不能当改编处理**——按 `original` 走，人物与规矩全部由我们补建，并逐条标 `[创作]`。

> 原句的"今天，有人坐下了"已经把转折给了：本片的任务不是制造意外，而是**让"那碗面"在被吃掉之前先变得不可碰**。所以展开的重点在规矩，不在反转。

> **构思武器库（S0 内部，不展示给用户）**：原句已是清晰的一句话来源，未走五选题路径，但其"规矩 vs 打破"的结构符合"从关系/空间出发"的张力；logline 由 `references/ideation-toolkit.md` 锐化——把"每天多煮一碗"定为可拍的固定动作（目标＋阻碍的雏形），再进 S2/S3 展开。

---

## S1 梗概草稿与容量判断

### 梗概（一段话）

> 老周在老街沿摆了三十年早餐摊。每天凌晨四点，他都会多煮一碗面，端到角落那张空桌上——三十年来没人碰过，他也没对任何人说过为什么。这个下雨的清晨，一个陌生的小女孩走进来，径直坐到那张桌前，把那碗面拉到了自己面前。老周站住了。全片没有一句解释：规矩被打破之后，他只是把碗放下，说了句"吃吧"。雨还在下。

> **这一段先给用户看，认可走向与气质再进 S2。** 梗概是 S1 的主产出——它让用户在花任何成本之前就能判断"这片子大概是什么"，也比直接看节拍表更容易提出修改。

- **容量**：一句话只够一个"固定动作 + 一次打破"。60 秒需要补三层——① 一条必须被看见的规矩（建立）② 一次无声的侧目（压力）③ 规矩被打破之后的处置（代价）。三层全部 `[创作]`。
- **内容类型**：`剧情演绎`。原句的动作带动机（"从来没有人吃"是一种守，"多煮一碗"是一种等），不靠音乐节奏承载，不走 `MV`。
- **风格意向**：未给。按原句的生计与天气，主推"写实记录感、单灯暖光、雨湿低饱和"，备选"黑白＋只留面汤的白"（成本更低，但会抹掉雨天路面的反光层次）。缺省取主推。
- **参考图状态**：无。风格一致性与**雨量一致**是两条主要风险，靠第五步六维风格卡与统一负面词压住。

---

## S2 人物深度与弧光 ＋ 前史与世界观：一句话要展开成什么（`templates/canon-bible.md`）

### 用户原话（唯一的 `[来源]`）

> 每天凌晨四点，早餐摊老板都会多煮一碗面放在角落的桌上，从来没有人吃；今天，有人坐下了。

### 世界规则

| 编号 | 规则 | 类型 | 标注 | 如何约束行动 |
|---|---|---|---|---|
| W01 | 四点出摊的顺序是固定的：先开灯、先擦角落那张桌子、先摆好一副碗筷，然后才点火下第一碗面 | 制度 | `[创作]` | 观众第一眼见到的动作就是"擦一张没人坐的桌子"，不用一句台词就把规矩立起来 |
| W02 | 那碗面放在角落桌上之后不再动：不回锅、不端给任何人、不收摊前不撤；凉了就凉着 | 制度 | `[创作]` | 所以"有人要吃"必须主动违反一条他守了很多年的规矩——这就是拍5 的全部阻力 |
| W03 | 摊子只做街坊和过路司机，不吆喝、不摆招牌；熟客各有自己的位置，四张桌坐满也不坐角落那张 | 社会 | `[创作]` | 角落那张桌是全摊唯一"没人认领"的位置，坐下去就是越界——小女孩坐下这个动作才有分量 |
| W04 | 下大雨也照常出摊；雨大没人来，那碗面照煮 | 物理 | `[创作]` | 让"没人吃"变成可拍的空镜（一碗面在雨里冒热气），也让今天"有人来"显得反常 |

> 四条规则没有一条是背景装饰：W01 管第一镜的擦桌、W02 管拍5 的犹豫、W03 管拍3 的侧目、W04 管全片的雨。**写规则时就要想好它落在哪个镜头上，落不下来的不要写。**

### 人物

**角色01 老板（老周）**

| 项 | 内容 | 标注 |
|---|---|---|
| 身份 | 62 岁，在这条街沿摆了三十年摊，一个人和面、下面、收摊 | `[创作]` |
| want | 把这个早晨照常做完：四点出摊，六点半收摊，不被打断 | `[创作]` |
| need | 承认那碗面不是给一个还会来的人煮的 | `[创作]` |
| 阻力 | 规矩上那碗面必须凉着、必须倒掉；他自己更不想看见有人吃它 | `[创作]` |
| 弧光 | 从"把碗推过去然后转身走开"到"把碗放下、站住说完那句话" | `[创作]` |
| 矛盾性 | 外在沉默克制 vs 内在执念——三十年守一个没人领的面，却从不对人解释 | `[创作]` |
| Ghost（前史创伤） | 曾有一个会来吃这碗面的人（女儿），某年之后再没出现；他守的是"她还会回来"的可能 | `[创作]` |
| Lie（角色谎言） | 他告诉自己（和街坊）这碗面"只是习惯，顺手多煮" | `[创作]` |
| Flaw（性格缺陷） | 用规矩压住思念，越守越僵，不肯让人靠近 | `[创作]` |

**角色02 小女孩**

| 项 | 内容 | 标注 |
|---|---|---|
| 身份 | 8 岁上下，一个人，穿一件明显大了一号的黄色儿童雨衣 | `[创作]` |
| want | 吃一碗热的 | `[创作]` |
| need | **不给**——她是变量，不是主角 | `[创作]` |
| 阻力 | 她不知道这张桌子有规矩 | `[创作]` |
| 弧光 | **不给**——她只是坐下，全片不解释她是谁、从哪来、为什么一个人 | `[创作]` |
| 矛盾性 / Ghost / Lie / Flaw | **不给**——她是变量，不是被解释的对象 | `[创作]` |

> 两个人物必须一个给弧光、一个不给。若小女孩也有成长或反转，本片就变成"两代人互相救赎"，原句那点克制全没了。**她是被拍的对象，不是被解释的对象。**

### 视觉连续性锁（`[设定]`，全片不改）

- 老周：白色无袖汗衫＋深蓝帆布围裙（系在腰前，遮到膝上）＋左肩搭一条褪色灰毛巾＋深灰宽松长裤＋黑色旧橡胶套鞋；**围裙上有两处固定的油渍（右胸下、左胯）**。
- 小女孩：亮黄色连帽儿童雨衣（大一号，袖口翻折）＋深灰雨靴＋齐耳短发；**全片只有这一件黄色**。
- 场景：街沿，帆布雨棚从摊车斜拉出来；四张白色折叠桌，三张在雨棚下，**角落那张在雨棚边缘外，会淋到一点雨**。
- 光与雨：摊车顶一只白炽灯泡（约 3000K）为唯一主光；路灯钠灯（约 2200K）只在远景背景出现；天光冷青作环境。**中雨，全片雨量不变，不得中途停雨或转晴**。

---

## S3 结构大纲 → 场景拆解 → 场景写作 → 剧本医生（`templates/screenplay.md`）

### 结构选型（先选骨架方法论）

本片体量是一句话原创的极简单场短片（约 60 秒、单场景），先按 `references/storycraft.md` 第一节选定骨架，再写节拍表：

- **选定：STC 内在节拍（精简为 6 拍）**，价值轴锁定为单一轴 **「守规矩 ↔ 破规矩」**。
- **不选完整 15 拍 STC**：15 拍的"激励事件—进展—中点—危机—高潮—结局"是为 90 分钟长片设计的，本片没有独立的"中点转折"或"第二幕"，强套会把节奏拉空、多出无效过场。
- **不选 Story Circle 环**：环结构依赖"角色离开常态—归来已变"的旅程感，本片角色没有空间位移，用环会虚假。
- **为什么是内在节拍**：拍 1–6 每一拍都让"守/破规矩"这一价值位移一格（建立规矩 → 面是真的 → 众人知道 → 有人坐 → 他选违规 → 他把规矩也去掉了），正好是一个压缩到极致的"单一价值转折"。

> 一句话原创没有现成骨架可拆，所以先定骨架再填拍；`adaptation` 模式则以来源事件为骨架，不在此做选型。

### 节拍表（6 拍）

| # | 节拍 | 本拍改变了什么 | 标注 |
|---|---|---|---|
| 1 | 四点，雨。开灯，走到角落把那张折叠桌擦一遍，摆上一副碗筷 | 信息：规矩建立起来了，且是"先摆桌、后下面" | `[创作]` |
| 2 | 点火，下第一碗面，捞起来，撒葱花，卧一个蛋，端到角落那张桌上；热气在雨里直上 | 信息：那碗面是真的面，不是摆设 | `[来源]` 原句核心动作 ＋`[创作]` 具体处理 |
| 3 | 五点多，熟客陆续来，另外三张桌坐满；有人抬眼看了角落那碗面一下，又低头吃 | 压力：所有人都知道那碗面，也都不碰它 | `[创作]` |
| 4 | 一个穿黄色雨衣的小女孩从街角走过来，径直走到角落那张桌前，拉开凳子坐下 | 打破：原句的"今天，有人坐下了" | `[来源]` |
| 5 | 老周的手停在锅上方，勺还举着；他把碗端过去、放下、推了一下，说了一句话 | 决定：他选择违规，且只说一句 | `[创作]` |
| 6 | 收摊，雨还在下。碗是空的，汤见底，筷子横在碗沿；他把碗收进水池，第一次没有倒掉剩下的汤 | 选择：规矩破了，他把"倒掉"这一步也去掉了 | `[创作]` |

> 第 6 拍必须是代价或选择，不能只是"他明白了"。这里给的是"他第一次没有倒掉"——**一个可拍的动作，不是一个表情**。
>
> 拍 3 那个"抬眼"的人**不给台词、不给正脸**。一旦有人开口评价那碗面，本片就多了一个说话人，"说话镜头锁人"立刻失守，还替观众把答案说了。**侧目用眼睛演，不用嘴演。**

### 开场钩子（必交付）

本片开场即 W01 的"擦一张没人坐的桌子"——第一个画面就把"规矩"立起来，不靠一句台词（满足"从最有张力的截面切入"）。前 30 秒观众的疑问是"那张桌子是给谁的"，类型基调（克制·写实·暖）由单灯暖光与雨湿冷青同框定调。

### 场次表（全片 1 场）

**场次 S01｜老街沿早餐摊｜凌晨四点至六点半（雨）**

> **双轨节奏**：本场外部情节从松到紧（擦桌→来客→坐下→违规），内在情感始终压在"那碗面"上、直到结尾才释放；两线在本场末同至高点，是全片唯一高潮段。短段内也要有张弛，不一条平线走完。

| 事件序号 | 事件 | 角色动作 | 关键对白/独白 | 标注 |
|---|---|---|---|---|
| 1-1 | 开灯，擦角落的桌，摆碗筷 | 擦、摆、直腰 | 无 | `[创作]` |
| 1-2 | 下面，装碗，端到角落桌上 | 挑面、撒葱花、卧蛋、端、放 | 无 | `[来源]`＋`[创作]` |
| 1-3 | 熟客来，三桌坐满，有人侧目 | 坐、吃、抬眼、低头 | 无 | `[创作]` |
| 1-4 | 小女孩走来，坐下 | 走、停、拉凳、坐 | 无 | `[来源]` |
| 1-5 | 端碗过去，说一句话 | 端、绕过桌角、放、推、站直 | 「这碗，是给我女儿的。」 | `[创作]` |
| 1-6 | 收摊，空碗，不倒汤 | 收伞、收碗、进水池、不倾倒 | 无 | `[创作]` |

**本场档案**

| 项 | 内容 |
|---|---|
| 开场状态 | 雨里一个还没开始营业的摊子，一盏灯 |
| **本场改变了什么** | 制度（一条守了多年的规矩，在这一天被自己破了，且没有还原） |
| 结束状态 | 碗空了，汤没倒；观众知道的和老周知道的不再一样 |
| 是否新增主线冲突 | 否 |

### 台词（全片 1 句）

1. 「这碗，是给我女儿的。」（8 字，陈述句，音量很低，不是解释给谁听）

> 台词只承担压力，不解释设定。"她是谁""去了哪""为什么下雨"从头到尾没有一句交代，靠 W03 的空桌、拍 3 的侧目、拍 6 的不倒汤承担。
>
> **全片只有一句台词是对的**：60 秒里，沉默本身就是信息。不要在拍 1、拍 3 加"自言自语"式的台词来"让人物立体"——那会把悬念提前花掉。

### 剧本医生（S3 自检 / 抛光）

按 `references/storycraft.md` **第六节**（剧本医生诊断维度）做诊断（第八节四张自检清单覆盖"输出前自检"；长内容项标注不适用）：

- **价值转变**：核心轴「守规矩 ↔ 破规矩」在拍 6 真正翻转，且以"不倒汤"这一可拍动作落地，非情绪交代 ✅
- **鸿沟（McKee）**：老周"以为只是端一碗面"与"实际上破了守多年的规矩"之间的落差由观众而非角色说出，留白成立 ✅
- **危机中的选择**：拍 5 的选择是"违规且只说一句"，是动作不是表态 ✅
- **无效情节审计**：6 拍无一拍可删——删拍 3（侧目）则"众人都知道"不成立，删拍 6（不倒汤）则结尾无落点 ❌不可删
- **伏笔审计**：本片无跨场伏笔（单场）；开场"空桌"即收尾"空碗"的视觉回扣已闭环 ✅（长内容伏笔/回扣登记表不适用）
- **群像功能审计**：侧目者 = 节奏/压力功能（不给台词，避免新增说话人、守住说话镜头锁人）；小女孩 = 破局功能；老周 = 主角。无冗余角色 ✅
- **节奏诊断**：外部情节拍 1–6 由松到紧，内在情感始终压在"那碗面"上直到拍 6 释放，两线在本场末同至高点，无平线段 ✅
- **开场质量**：第一个画面即"擦一张没人坐的桌子"，立规矩不靠台词，前 30 秒疑问成立 ✅
- **常见陷阱自查**：无心理描写 ❌无；无括号暗示 ❌无；无解释性台词 ❌无；无说教煽情 ❌无；无 AI 腔 ❌无；台词与动作冲突以动作为准（说"给我女儿的"同时手在推碗）✅

> 诊断结论：本片通过。唯一需留意的是拍 4 小女孩"径直坐下"——若镜头给太久会稀释留白；导演阶段（S5+）用"她坐下后立刻切老周的手"压住，不在剧本层多写。

---

## S4 资产设定与编号锁定（`templates/asset-design.md`）

> 本片四轴＝当代／生活流＋家庭／中国城市老街沿／克制·写实·暖，**世界背景＝现代**。按 `templates/asset-design.md` 〇章的「角色具体化拆解」步骤，走 `references/character-craft.md` 的「现代／科幻／架空」路由：**服饰查 `char-library/styles/服装风格.md`＋`时代与类型.md`＋`人群与身份.md`，不查 `古典形制.md`**（古代库只给历史题材，本片不加载）。

### 角色具体化拆解（示范，对应 〇章步骤，先于填表）

**角色01 老周**——先把"一个沉默的早餐摊老人"拆成维度名词，再落下面「角色设定」与「造型清单」：

- **一句定人**：62 岁、在这条街沿摆了三十年摊的个体小生意人；想要"把早晨照常做完"，守着一个不会回来的人（对应 S2 的 want／need）。
- **查库**：`人群与身份.md` → 市井小生意人／老年个体户；`时代与类型.md`（中国·当代城市）＋ `dimensions/06-生活痕迹.md`；状态＝雨里站了半夜、手常泡在面汤里。
- **形容词→名词化（摘关键几条）**：
  - "苍老" → 方脸、法令纹深、灰白寸头、下颌两天未刮的胡茬（**身份层**，进卡锁定）；
  - "劳苦" → 手掌厚、指节粗、右手虎口一道旧疤（**生活痕迹**，身份层）；
  - "湿冷里的安稳" → 白汗衫＋深蓝帆布围裙（**造型层**，围裙两处油渍固定位置）。
- **三层标注**：脸型／骨相／疤／寸头＝身份（跨镜不变）；汗衫＋围裙＝造型A（单场单造型）；"雨湿发梢、袖口微潮"＝状态（仅拍1–2 写，不进卡锁定段）。
- **刚柔**：底色柔（微驼、重心偏左脚、动作慢），推向仍柔；但"把碗推过去"那一下是全片唯一的硬——逆推反差，对应 need 的释放。
- **形容词残留检查**：原形容"克制"已拆为动作与着装，无残留形容词进卡。

**角色02 小女孩**——一类人＝学龄儿童；造型＝功能服（亮黄雨衣大一号、雨靴），属 `dimensions/04-服装.md` 的"童装／雨具"；**不写弧光、不解释**（她是变量，不是被解释的对象，见 S2 判定）。

> 拆解结果直接落到下方「角色设定」与「角色造型清单」。六行信息表 schema 不变（姓名／身份／年龄／性格／外貌／着装），本步骤只是把"外貌·发型""着装·气质"两格写得更具体、可生成。

### 角色

**角色01 老周**，男，62 岁，`[创作]`：方脸、法令纹深、灰白寸头、下颌有两天没刮的胡茬；手掌厚、指节粗、右手虎口有一道旧疤；背微驼，站着时重心偏左脚。

**角色02 小女孩**，女，8 岁上下，`[创作]`：身高约 120cm，齐耳短发被雨打湿贴在颊侧；雨衣明显大一号，袖子长到盖住半个手背、翻折了两道；雨靴到小腿。**脸部不做美化，不化儿童妆**。

### 角色造型清单

| 造型编号 | 所属角色 | 造型描述 | 出场场次 | 依据 |
|---|---|---|---|---|
| 角色01-造型A | 角色01 | 白色无袖汗衫、深蓝帆布围裙（系在腰前、遮到膝上、右胸下与左胯各一处油渍）、左肩搭褪色灰毛巾、深灰宽松长裤、黑色旧橡胶套鞋 | S01 全片 | `[创作]` 单场单造型，不做变体 |
| 角色02-造型A | 角色02 | 亮黄色连帽儿童雨衣（大一号，袖口翻折两道）、深灰雨靴、齐耳短发 | S01 拍4–拍6 | `[创作]` 单场单造型，不做变体 |

### 第二角色是否出卡的判定

| 角色 | 判定 | 理由 |
|---|---|---|
| 角色01 老板 | **出图** | 全片主体，跨 4 个段落出现，面部与围裙油渍位置必须跨镜一致 |
| 角色02 小女孩 | **出图** | 拍 4–6 的画面主体，连续三个段落出镜、被中近景拍到正脸、且"亮黄色"是全片唯一的暖色变量——**靠文字描述写不住，跨镜必失配** |

> 第二角色出卡不是"人多就给卡"，也不是"省钱就不给"。判定只看三条：**是不是被拍的画面主体、跨不跨段、文字写得住写不住。** 本片小女孩三条全中，所以多花一张卡是值的；如果她只在远景出现一次、不露脸，就应判为"仅文字"，由场景卡承载。**她坐在那儿被拍了 20 秒，省这张卡的结果就是后三段换了个孩子。**

### 场景视角拆分（整合进 1 张 6:5 场景卡）

| 视角编号 | 类型 | 卡内位置 | 说明 |
|---|---|---|---|
| 场景01-V01 | 空间微缩全景 | 左列上格 | 掀顶轴测：街沿走向、摊车与雨棚位置、四张折叠桌的分布，**角落那张必须单独看出来在雨棚边缘外** |
| 场景01-V02 | 人眼写实全景 | 左列下格 | 眼高平视、无人，雨丝可见，摊灯亮着，湿沥青上有灯光的碎反光 |
| 场景01-V03 | 取景（远景1） | 右列第 1 格 | 角落那张折叠桌与一张白色塑料凳（中景·陈设）——**本片的第二个主角，必须能看清桌面水痕、桌腿锈迹、凳面裂纹** |
| 场景01-V04 | 取景（远景2） | 右列第 2 格 | 摊车与锅灶（中景·构件）：铝锅、灶头、油渍、抹布挂沿 |
| 场景01-V05 | 取景（远景3） | 右列第 3 格 | 雨棚边缘滴水与灯泡（特写·光影）：雨珠挂在帆布边、灯泡外罩有油污 |
| 场景01-V06 | 取景（远景4） | 右列第 4 格 | 湿沥青的路灯光反光与摊车倒影（中景·材质） |

### 道具出图判定

| 道具编号 | 名称 | 出图判定 | 理由 |
|---|---|---|---|
| 道具01 | 那碗面 | **出图** | 情节核心、被特写（拍2 放置、拍6 空碗）、主要角色端起使用——三项全中。形制必须与场景卡 V04 的铝锅同源 |
| 道具02 | 长柄铝笊篱 | **出图** | 老板所有手部动作都靠它落地（挑面、抖水、装碗），拍5 的"停住"就是一个特写——**这个停顿是本片唯一的高光时刻，笊篱形制画不稳它就不成立** |
| 道具03 | 抹布 | **仅文字** | 只在拍1 擦桌时出现一次、不被特写、属随手陈设；由场景卡 V04 承载（挂在摊车沿上） |

### 编号总表

| 类型 | 编号 | 出图张数 |
|---|---|---|
| 角色造型 | 角色01-造型A、角色02-造型A | 2 张 6:5 角色卡 |
| 场景 | 场景01（V01–V06 整合） | 1 张 6:5 场景卡 |
| 道具 | 道具01、道具02 | 2 张 5:6 道具卡 |
| 段落 | P01–P04 | 4 套故事板 × 2 版式 = 8 张 |

**本片图片总数 5 + 8 = 13 张**（G3 展示后由成本告知环节向用户报数）。

> 比单角色故事多花的那一张卡，是角色02。**这个数字要在 G3 时报给用户，而不是等出完图再说。**

> **此处为 G1 检查点（不停）。** 展示完即进 S5，不索要口令。G1 锁定：项目定义与核心戏剧动作、梗概走向、世界规则、人物 want/need、节拍表、场次、全部编号。

---

## S5 六维风格卡（`templates/style-anchor.md`）

- 风格卡 ID：`DIERFEN-STYLE-v1`　状态：已定稿

| 维度 | 定稿内容 |
|---|---|
| ① 媒介与渲染 | 电影写实摄影 |
| ② 世界美学取向 | 当代中国老街市井 · 生活流（不做复古怀旧滤镜，不做日式清新） |
| ③ 影像质感 | 35mm 胶片颗粒；低饱和；暗部保留细节；浅景深，雨幕虚化成光斑 |
| ④ 色彩体系 | 主色 `#2E3338` 雨晨青灰；辅助 `#8A6A4B` 旧木与油渍；点缀 `#E0A24A` 摊灯暖光；唯一高饱和色 `#E8C33A` 小女孩雨衣；冷底暖点缀 |
| ⑤ 光线与氛围 | 唯一主光为摊车顶白炽灯（约 3000K，顶光压下、灯下有明显暗角）；路灯钠灯只在远景背景；天光冷青作环境填充；氛围词：湿、热、不敢问 |
| ⑥ 参考锚点 | 无参考图。文字参考"凌晨街沿早点摊、帆布雨棚、白炽灯泡、湿沥青反光"，`[推断]` |
| 材质与表面规则 | 铝、白瓷、帆布、塑料、湿沥青、棉布；全部带油渍、水痕与使用痕迹，禁止崭新无痕 |

- 统一负面词：插画感、3D渲染感、塑料质感、影楼风、过度磨皮、**第二个主光源、雨量变化、雨突然停**
- 资产展示风格：风格浅色底（`#2E3338` 调浅的非纯白）、均匀柔光、无强投影；成片风格按上表 ④⑤

> **天光是会变的，曝光值不能变。** 本片时间从四点走到六点半，天光要从墨蓝推到灰白——这是叙事，必须做；但**每个镜头的曝光值要恒定**：不能出现某一镜无故偏暗、偏绿、噪点更重。写提示词时这条要显式写进去（见 S8 的第二句），否则六格拼起来会像六个不同时间拍的。

---

## S6 导演交接包（`templates/director-handoff.md`，摘要）

- **时长**：总 60 秒（56–64）；单镜上限 15 秒；段落上限 15 秒／段，每段关键帧 N 默认 6（短段可降到 2–3 格）。
- **统一画面风格**：`DIERFEN-STYLE-v1` 六维全文＋统一负面词。
- **情节简述**：四点，雨。老周开灯，先把角落那张空桌擦一遍、摆好一副碗筷，才点火下第一碗面。这碗面端到角落桌上就不许再动。五点多熟客陆续来，三张桌坐满，有人抬眼看了那碗面一下，又低头吃。六点，一个穿黄色雨衣的小女孩从街角走来，径直坐下。老周的手停在锅上。他把碗端过去、放下、推了一下，说"这碗，是给我女儿的"。收摊时碗是空的，他把碗收进水池，第一次没有倒掉剩下的汤。
- **资产编号**：`角色01-造型A`、`角色02-造型A`、`场景01`（V01–V06 为卡内格位，整合进 1 张 6:5 场景卡）、`道具01`、`道具02`、`道具03`（仅文字，不出图）。**资产图将在第九至十一步生成，本阶段以编号占位。**
- **内容类型与平台**：`剧情演绎`；16:9；需要台词、音效描述，不需要背景音乐。
- **全局约束**：面部／发型／服装／围裙油渍位置跨镜一致；四张桌的分布与角落那张的相对位置跨镜一致；**中雨全片不变，雨量不得中途变化**；唯一主光规则不可破；曝光值恒定。

- **核心视听手法**（`templates/director-handoff.md`「三·补」）：
  - 手法 1＝**画面内前景/背景叙事**：前景永远是老周的手与锅，背景永远带着角落那张空桌——**不靠剪辑、不靠台词，让观众在同一画面里自己发现"他在为一张没人坐的桌子忙"**。它契合本片概念：主角做的每件事都指向画面里那个不在场的人。
  - 递进方式：升级——P01 空桌只在背景里露一角 → P02/P03 同一画面里空桌占比逐渐变大 → P04 前景第一次空掉（老周收摊离画），只留那张桌子在画面里。
  - 落到分镜字段：画面内容（**逐镜分"前景／背景"两层写**，背景必写空桌状态）、景别（中景为主，只在碗上给一次大特写）、运镜（保持在极小幅度，不破坏前后景同框）、音效（雨声全程，P03 小女孩坐下时雨声突然压低）。
  - 手法 2＝**无**（不堆第二种）。
  - 自检：只有 1 种 ✓；能说出为什么契合 ✓；递进已写明 ✓；单段内可闭合（每段都在自己的画面里完成前后景并置）✓；与风格卡第⑤维（唯一主光、雨）不冲突 ✓。

> **此处为 G2 检查点（不停）。** 展示完即进 S7，不索要口令。G2 锁定六维风格卡与交接包（含核心视听手法）。此刻仍无任何资产图，导演只按编号与文字工作。

---

## S7 段落划分与 P01 分镜表

### 段落清单

| 段落 | 起 | 止 | 时长 | 镜头数 | 关键帧数 | 故事板 | 覆盖节拍 |
|---|---|---|---|---|---|---|---|
| P01 | 00:00.000 | 00:15.000 | 15s | 3 | 6 | SB-01 | 拍1＋拍2 |
| P02 | 00:15.000 | 00:30.000 | 15s | 4 | 6 | SB-02 | 拍3 |
| P03 | 00:30.000 | 00:45.000 | 15s | 3 | 6 | SB-03 | 拍4＋拍5 前半 |
| P04 | 00:45.000 | 01:00.000 | 15s | 4 | 6 | SB-04 | 拍5 后半＋拍6 |

目标总时长 60 秒 / 预计 60 秒 / 差额 0。段落边界与关键帧数在此一次定死，第十二步不得增删。**镜头数一栏同时是格子上限的体检**：四段分别是 3／4／3／4 镜，都小于 6，所以每镜都吃得到格子；哪段写成 7，就说明该段装不下、必须拆——这一栏不是统计，是约束。

### Picture 槽位分配（整集统一，锁定）

| 槽位 | 资产编号 | 用途 | 使用段落 |
|---|---|---|---|
| Picture 1 | 角色01-造型A | 老周的外型（半身主视觉区裁切） | P01–P04 |
| Picture 2 | 场景01-V02 | 街沿与摊位的空间基准 | P01–P04 |
| Picture 3 | 道具01 | 那碗面 | P01、P04 |
| Picture 4 | 场景01-V03 | 角落那张桌与凳 | P02–P04 |
| Picture 5 | 角色02-造型A | 小女孩的外型 | P03–P04 |
| Picture 6 | 道具02 | 长柄铝笊篱 | P01、P03 |
| Picture 7–9 | — | 空 | — |

> 编号整集统一，不逐段重排；**某一段用哪几个槽位是按需挑的，不要求连续**——P01 挑 1、2、3、6，跳过 4、5，这是正常的。每段最多挂 5 张，按"**说话人＞当前段的目标人物＞场景＞道具**"取舍：P01 挂 4 张（无第二角色；角落桌的独立参考先不给，因为擦桌动作本身就落在 V02 视野里；但笊篱必须给，SH02 整镜的对象就是它），P03 **挂满 5 张**（三镜分属两个人物和一个道具，省哪张都会坏：她的两镜要 2、4、5，他的特写给 1、6），P04 挂 4 张（1、3、4、5，去掉笊篱——锅上的戏已经结束）。

### P01 分镜提示词表

| 字段 | S01-SH01 | S01-SH02 | S01-SH03 |
|---|---|---|---|
| 时间码 | 00:00.000–00:05.000 | 00:05.000–00:10.500 | 00:10.500–00:15.000 |
| 单镜时长 | 5s | 5.5s | 4.5s |
| 场景 | 场景01-V02 | 场景01-V02（摊车正面局部） | 场景01-V02（角落桌所在方向） |
| 出场角色 | 角色01-造型A | 角色01-造型A（背身，只见肩与手） | 角色01-造型A |
| 位置锁定 | 从摊车走向画面右后的角落桌，不横穿画面 | 站定在摊车后，面朝锅，不转身 | 从摊车走向角落桌，放下即回身 |
| 情节递进 | 建立环境与"灯是唯一亮的东西" | 建立"先摆桌、后下面"的规矩顺序 | 那碗面第一次离开锅，落到空桌上 |
| 画面内容 | 雨。街沿上只有摊车亮着，帆布雨棚滴水；老周背身把角落那张折叠桌擦一遍，摆上一副碗筷，直腰 | 中近景：他的手在铝锅上方挑面、提笊篱、抖水，蒸汽扑到镜头上；旁边一只白瓷碗已摆好 | 他把碗端到角落桌上放下，撒葱花、卧一个蛋；热气在冷雨里直上；他转身往回走，碗留在空桌前 |
| 景别与角度 | 全景／平视 | 近景／略俯（看锅） | 中景／平视 |
| 运镜轨迹 | 起幅定住 → 极缓右移跟人 → 落幅在他直腰 | 起幅近景手部 → 固定 → 落幅锅与碗 | 起幅跟碗移动 → 停 → 落幅定在空桌，人出画 |
| 衔接方式 | 开场 | 硬切 | 硬切（动作接：放下） |
| 说话人与音色 | — | — | — |
| 台词 | 无 | 无 | 无 |
| 台词字数 | 0 | 0 | 0 |
| 气口数 | 0 | 0 | 0 |
| 纯动作时长 | 5.0s（擦、摆、直腰） | 5.5s（挑、提、抖、装碗） | 4.5s（端、放、撒、卧蛋、回身） |
| 实际语速 | — | — | — |
| 音效 | 中雨打在帆布上的闷响、桌椅刮地一声、远处早市拉卷闸门 | 油锅轻爆、笊篱抖水、铝勺磕锅沿、蒸汽声 | 瓷碗落桌一声、葱花撒落、雨声持续、脚步走开 |
| 背景音乐 | N/A | N/A | N/A |
| 参考图 | Picture 1, 2（本镜那碗面还不存在，不挂 Picture 3） | Picture 1, 2, 3, 6 | Picture 1, 2, 3（本镜不再动锅，不挂笊篱） |
| 关键帧 | P01-KF01–KF02 | P01-KF03–KF04 | P01-KF05–KF06 |

**说话镜头锁人自检**：P01 三镜全无台词，不涉及锁人 ✓

> **P01 不给台词，是刻意的。** 第一段的任务是把规矩立起来——一个六十多岁的人在雨里先擦一张没人坐的桌子，比让他说"这是给我女儿的"有力一百倍。**能在动作里说完的，不要交给嘴。** 台词只有一句，要留到拍5 才舍得用。

**P02–P04 分镜（不展开，结构同 P01）**
- P02｜4 镜：全景熟客陆续坐下（三张桌，避开角落）→ 三桌坐满、角落那桌空着，那碗面还在，热气已经淡了 → 近景：一个熟客抬眼看了那碗面一下，低头继续吃，**不给正脸全貌、不开口** → 老周在锅前背身，没回头。
- P03｜3 镜：远景长焦，雨幕里一个黄色的小小身影从街角走来（黄是全片第一个高饱和色）→ 中景，她径直走到角落那张桌前，拉开凳子坐下，雨衣还在滴水 → 特写：老周的手停在锅上方，笊篱悬着不动，蒸汽从网眼里穿上来。
- P04｜4 镜：他站着不动（反应，中景）→ 端碗、绕过桌角、把碗放到她面前，推了一下（无台词）→ 站直、收回手，说「这碗，是给我女儿的。」→ 收摊：空碗、汤见底、筷子横在碗沿；他背对镜头把碗收进水池，不倾倒。

> **P04 的语速推演（一次真实返工，"太快"型）。** 初稿把这句写成「这碗面是我女儿的，她走那年也是这样的雨，你吃吧，别提」，24 字，全压在 SH02 里——SH02 要端碗、绕过桌角、放下、推一下，纯动作 3 秒，8 秒的镜头只剩 5 秒给嘴：24 ÷ 5 = **4.8 字/秒**，超出 3.5 上限。**出错的原因不是台词长，是这一镜的动作太满——动作越多，能装的台词越少。** 改法是两条一起用：① **把说话从 SH02 里拆出来**，独立成 SH03（SH02 变成纯动作、无台词）；② **台词砍到 8 字**（「这碗，是给我女儿的。」，删掉"她走那年也是这样的雨"和"你吃吧，别提"）。SH03 给 4 秒，气口 1 个（逗号 0.5s），纯动作 1.0s（站直、收回手）：8 ÷ (4 − 0.5 − 1.0) = **3.2** ✓ 落在区间内。**砍掉的那两句不是废话，是应该留在留白里的东西**——说出来就成了交代，本片就不成立了。第七步发现，就在第七步改：不改台词内容（台词的取舍属第三步，此处只允许"删"不允许"重写"），不压语速凑数。

> **两种返工都要会认。** "太慢"（字太少、镜头太长，会拍成假慢镜——模型容易把停顿演成"忘了说"）和"太快"（字太多、动作太满，会拍成念稿）都是不合格，处理方向相反：**太慢压镜头、加动作配比；太快拆镜头、删台词。**

---

## S8 提示词包：P01 六段式全文（可整段粘贴）

**参考图顺序表（不属于提示词正文）**

| 槽位 | 资产 | 在本段的作用 |
|---|---|---|
| Picture 1 | 角色01-造型A | 老周的外型与服装 |
| Picture 2 | 场景01-V02 | 街沿、摊车与雨的空间基准 |
| Picture 3 | 道具01 | 那碗面 |
| Picture 6 | 道具02 | 长柄铝笊篱（仅 SH02 使用） |

> 本段挂 4 张，但**不是四张都服务三个镜头**：Picture 6 只进 SH02；SH01 不挂 Picture 3（那碗面还没煮出来）；SH03 不挂 Picture 6（锅上的动作已经结束）。运行时按分镜表逐镜连节点，别把四张一股脑全连上。

```text
subject_definitions:
<Subject 1> is Lao Zhou, the breakfast-stall owner — FACE from <Picture 1> (early sixties, broad square face, deep nasolabial folds, short cropped grey hair, two days of grey stubble along the jaw, weathered matte skin with visible pores, thick hands with a small old scar on the right web between thumb and index). OUTFIT LOCKED as a plain white sleeveless cotton undershirt, a dark navy canvas apron tied at the waist and hanging to just above the knee, a faded grey towel draped over his LEFT shoulder, loose dark grey cotton trousers, old black rubber slip-on shoes. The apron carries TWO FIXED stains: one below the right chest, one on the left hip. HAIR LOCKED short cropped grey, NOT long, NOT combed back. POSITION LOCKED behind or beside the stall cart, NEVER walking through the middle of the frame, NEVER sitting down. BODY: slight forward stoop, weight resting on the left leg when standing still.
<Subject 2> is the street-side breakfast stall in <Picture 2>: a steel-frame cart with a canvas awning sloped out and away from it, a single bare incandescent bulb hanging under the awning as the only strong light, wet dark asphalt in front, four white folding tables — three under the awning, one at the edge just outside it so it catches rain, a row of shuttered shopfronts receding into the rain behind. The wet asphalt and the cart's position are the central spatial reference.
<Subject 3> is the bowl of noodles in <Picture 3>: a thick white porcelain bowl with a thin blue line just under the rim, clear broth with a faint sheen of oil, a nest of thin wheat noodles, a scatter of chopped scallion, one fried egg laid on top with its yolk intact, a pair of plain bamboo chopsticks resting across the rim. Steam rises from it continuously.
<Subject 4> is the skimmer in <Picture 6>: a long-handled aluminium wire skimmer, a shallow perforated disc about a hand wide, a flat aluminium handle worn bright where the palm grips it, one dark burn ring on the disc rim, a wire loop joining disc and handle.
<Picture 1> ref <Subject 1>'s face. <Picture 2> ref <Subject 2>. <Picture 3> ref <Subject 3>. <Picture 6> ref <Subject 4>.
Background is text-defined only, no reference image needed, do not occupy Subject or Picture labels.

summary:
[reference generation] 15s 凌晨四点, 中雨. LAO ZHOU LOCKED: white sleeveless undershirt, dark navy canvas apron with two fixed stains, grey towel on the LEFT shoulder, dark grey trousers, black rubber shoes. NOT a chef's jacket, NOT a Chinese tunic, NOT an apron tied at the back. Rain falls at the SAME moderate density in every shot and never stops. 0-5s: he wipes the empty corner table and sets out a pair of chopsticks and a bowl, then straightens up — no dialogue. 5-10.5s: close on his hands working the aluminium skimmer in the pot, lifting noodles into the porcelain bowl — no dialogue. 10.5-15s: he carries the bowl to the corner table, sets it down, adds scallion and one fried egg, and turns back — no dialogue.

retention_analysis:
<Subject 1> (all shots): fully_preserved - face from <Picture 1>; OUTFIT FULLY PRESERVED as white sleeveless undershirt + dark navy apron with the two fixed stains + grey towel on the left shoulder + dark grey trousers + black rubber shoes; HAIR FULLY PRESERVED short cropped grey; the wiping hand, the lifted ladle and the turning back are new.
<Subject 2> (all shots): fully_preserved - steel cart, sloped canvas awning, single bulb, wet asphalt, four white folding tables with one at the awning edge, shuttered shopfronts behind; moderate rain at constant density.
<Subject 3> (Shot 2 as an EMPTY bowl of the same shape; Shot 3 fully dressed): fully_preserved - thick white porcelain bowl with blue rim line, bamboo chopsticks; the broth, thin wheat noodles, scallion and the fried egg with intact yolk appear ONLY in Shot 3, never earlier.
<Subject 4> (appears in Shot 2): fully_preserved - perforated aluminium disc, flat worn handle, burn ring on the disc rim, wire loop join.
<Picture 1-3, 6>: fully_preserved.
<Continuity>: none — this is the opening segment.

detailed_description:
The target video is in cinematic live-action documentary style. Visual characteristics: one warm 3000K bare bulb under the awning as the only key light, cool blue-grey pre-dawn daylight as ambient fill, low saturation with the yellow raincoat colour reserved and absent in this segment, fine 35mm grain, matte damp skin with visible pores, shallow focus with rain falling out of focus into bokeh.
Exposure value is CONSTANT across all shots — mid-grey baseline, shadows retain detail, no shot darker, greener or grainier than another; the sky may shift from ink-blue toward grey, the exposure may not.
LAO ZHOU OUTFIT LOCKED THROUGHOUT: white sleeveless cotton undershirt, dark navy canvas apron tied at the waist with one stain below the right chest and one on the left hip, faded grey towel on the LEFT shoulder, loose dark grey trousers, black rubber slip-on shoes. EXPLICITLY NOT a chef's jacket, NOT a Chinese tunic suit, NOT an apron tied at the back, NOT a hat. Moderate rain falls continuously at the same density in every shot; water drips from the awning edge throughout. The bare bulb is the ONLY strong light — no other lamp is lit, no headlights, no shop lights on.
[Shot 1] At 00:00.000, wide shot, eye level, camera holding then drifting slowly to the right to follow him. Rain. At the street edge only the stall cart is lit: a bare bulb under a sloped canvas awning, four white folding tables, three under the awning and one at its outer edge catching rain, wet asphalt mirroring broken light, shuttered shopfronts fading into the rain behind. Lao Zhou — white sleeveless undershirt, dark navy apron with its two stains, grey towel on the left shoulder — stands with his back three-quarters to camera at the corner table, wipes the tabletop once with a cloth, sets down a white bowl and a pair of bamboo chopsticks squared to the table edge, then straightens up. He does NOT walk through the middle of the frame. No dialogue.
[Shot 2] At 00:05.000, close shot, slightly high angle looking down into the pot, camera fixed. Steam rolls up into the lens. His thick hands lower the worn aluminium wire skimmer of <Picture 6> — perforated disc, flat handle bright where the palm grips, one burn ring on the rim — into an aluminium pot of boiling water, lift a nest of thin wheat noodles, shake the skimmer twice so water falls away, and tip the noodles into the empty bowl of the same thick white porcelain with the thin blue rim line that waits on the cart — plain noodles only, NO scallion and NO fried egg in this shot, they are added in the next shot; the apron front with its right-chest stain and the grey towel edge stay in the lower frame, his face is NOT in this shot. No dialogue.
[Shot 3] At 00:10.500, medium shot, eye level, camera following the bowl then stopping as he leaves frame. Lao Zhou — white sleeveless undershirt, dark navy apron with the two stains, grey towel on the left shoulder all clearly visible — carries the bowl in both hands from the cart toward the corner table just outside the awning, sets it down on the wet tabletop, scatters chopped scallion over it, lays one fried egg on top with the yolk intact, and turns back toward the cart; steam rises straight up into the cold rain and the rain hits the table edge beside the bowl. The bowl stays on the empty table. No dialogue.

overall_soundscape:
A street edge at four in the morning under steady moderate rain: rain drumming on taut canvas, water running off the awning edge and hitting the asphalt, a distant roller shutter being pulled up somewhere down the block, otherwise no voices. Shot 1: the cloth wiping a wet tabletop, a folding chair leg scraping once, rain constant. Shot 2: oil popping faintly, water shaken from a wire skimmer, a spoon tapping the rim of an aluminium pot, steam hissing. Shot 3: a porcelain bowl set down on a wet table, scallion scattering, footsteps walking away on wet asphalt, rain constant and unchanged. No dialogue anywhere in this segment. No music.

non_diegetic_music:
N/A
```

**本段自检**：六字段齐全 ✓ ／ `<Continuity>` 为 `none`（首段）✓ ／ Shot 数与分镜表一致（3）✓ ／ Subject 数与实挂 Picture 数一致（4 对 4：1、2、3、6）✓ ／ 每镜重复服装关键词（白汗衫＋深蓝围裙＋灰毛巾）✓ ／ 本段无台词，不涉及锁人 ✓ ／ 围裙两处油渍在 `subject_definitions` 与 `detailed_description` 各写一遍 ✓ ／ `non_diegetic_music` 为 `N/A` ✓ ／ **曝光恒定前缀在第二句** ✓ ／ 雨量恒定在 `summary`、`retention_analysis`、`detailed_description` 三处各交代一次 ✓ ／ 雨衣黄色在 `detailed_description` 里显式声明"本段不出现"，防止模型提前把黄色加进来 ✓

---

## S9–S11 三类资产卡（图位与提示词要点）

> 提示词草稿与 S7／S8 一并展示（G3 检查点，不停），展示后报成本告知（本片 13 张图）再进 S9 生图。全文按 `templates/standardized-prompts.md` 的对应卡型写，卡内分区必须逐区点名占比与内容；产出前统一拼接 `templates/generation-boundary.md` 的 DO/AVOID 块。

| 图位 | 文件 | 画幅 | 卡内结构 |
|---|---|---|---|
| 角色卡 | `角色01-造型A.png` | 6:5 | 五区：顶栏约 7%／上半区约 60%（左 25% 半身主视觉＋右 75% 三视图，正侧视图面部灰圆遮罩）／下半区约 33%（左 30% 六行信息表＋右 70% 四格特写） |
| 角色卡 | `角色02-造型A.png` | 6:5 | 同上五区结构。**儿童角色：三视图用同一年龄体型，不得出现成人比例**；四格特写取"雨衣帽兜压住额发""袖口翻折两道""雨靴筒口""湿发贴颊" |
| 场景卡 | `场景01.png` | 6:5 | 左二右四六格：左列 V01 微缩全景／V02 人眼全景，右列 V03–V06 四张真实取景；**V03 必须能看清桌腿锈、凳面裂纹与桌面水痕** |
| 道具卡 | `道具01.png` | 5:6 | 2×2 四宫格：正面／侧面／背面／入戏画面（入戏格＝那碗面放在角落桌上冒热气，依据场景卡 V03，占格 ≥1/4） |
| 道具卡 | `道具02.png` | 5:6 | 2×2 四宫格：正面／侧面／背面／入戏画面（入戏格＝笊篱悬在铝锅上方不动，炊具与光位依场景卡 V04） |

- 现代项目**不写分层着装**（无外层内层），但必须写清"哪些是衣服、哪些是污渍"——围裙上那两处油渍要在卡上明确标出位置，否则三视图里会自己长。
- **道具卡形制以先出的场景卡为准**：V04 里铝锅的金属色与油污程度是基准，那碗面的碗沿厚度要与锅里的一致。
- 道具03（抹布）不出图，只在场景卡 V04 内出现（挂在摊车沿上）。
- **角色02 的卡要单独提示"不要与角色01 同框、不要同风格背景"**，两张卡是两套独立参考，混成一张会让模型把两个人物焊在一起。

---

## S12 故事板 P01（`SB-01`，两版式两张）

由 N 张无字单格画面拼版（本例 6 张）：`cells/P01-KF01.png`…`KF06.png`（严格 16:9、长边 ≥2400px、画面内零文字），再

```text
python scripts/build_storyboard.py --data p01.json --cells cells/ --assets assets/ --out SB-01.png --layout all
```

得到 `SB-01-table.png`（六区段落板，给人看）与 `SB-01-raw.png`（6 格网格零文字，给视频模型裁首帧）。

**格位映射**

| 格位 | 镜号 | 关键帧 | 时间码 | 景别 | 画面简述 |
|---|---|---|---|---|---|
| R1C1 | S01-SH01 | P01-KF01 | 00:00.000–00:02.500 | 全景 | 雨里只有摊车亮着，四张桌，没人 |
| R1C2 | S01-SH01 | P01-KF02 | 00:02.500–00:05.000 | 全景 | 老周背身在角落擦桌，桌上已摆好碗筷 |
| R1C3 | S01-SH02 | P01-KF03 | 00:05.000–00:07.750 | 近景 | 手在锅上方提笊篱，蒸汽扑镜 |
| R2C1 | S01-SH02 | P01-KF04 | 00:07.750–00:10.500 | 近景 | 面落进白瓷碗，蛋放上去，碗端离锅沿 |
| R2C2 | S01-SH03 | P01-KF05 | 00:10.500–00:12.750 | 中景 | 碗放到角落桌上，热气直上，雨打在桌边 |
| R2C3 | S01-SH03 | P01-KF06 | 00:12.750–00:15.000 | 中景 | 他已转身往回走，那碗面留在空桌前 |

> 3 镜 6 帧：SH01／SH02 各 2 帧（运镜起落各一），SH03 2 帧（放碗／人离画）。6 格填满 15 秒，不留空格（短段可降为 2–3 格出板）。拼版后按 `templates/storyboard-selfcheck.md` 过 A 类几何项（`verify_storyboard.py --layout table|raw`）与 B 类视觉项。
>
> **这张表同时是格镜对齐的样板（B19 硬项）**：镜号变化的两处，前格结束时间**正好等于**后格起始时间（`00:05.000`、`00:10.500`），即镜头切换点落在格分界线上；镜号相同的三处（R1C1→R1C2、R1C3→R2C1、R2C2→R2C3）是一镜多格，属正常。首格起于 `00:00.000`、末格止于 `00:15.000`，五条全过。**反过来说也成立**：每镜至少占一格，所以这一段的上限就是本段格数 N（此例 6）镜——想加第 7 镜，只能回第七步拆段，不能在一格里叠两个镜头。
>
> **B 类必查本片三处特有项**：① 六格的**灯位**是否同一个位置（灯泡必须在摊车同一角）；② 六格的**雨量**是否一致（有一格雨变小就得重出）；③ 六格的**围裙油渍**是否在同一位置（这一项最容易在近景里丢）。

---

## S13 校验与交付

**校验通过项（摘要）**：全部资产引用 `DIERFEN-STYLE-v1`；场景引用精确到 `场景01-V02／V03／V04`；造型仅 角色01-造型A／角色02-造型A，无未登记造型；道具仅 道具01／02 出图，道具03 未出图符合判定；五张资产卡分区齐备；SB-01 两版式两张、六格与 3 镜 6 帧一一对应、**格镜对齐五条全过（`00:05.000` 与 `00:10.500` 两处切点正好落在格分界线上，每镜各占 2 格）**；标注只用 `[来源]/[设定]/[推断]/[创作]` 四类；P01 六段式六字段齐全、`non_diegetic_music` 为 `N/A`；P01 全无台词故不涉及锁人；P04 台词语速 3.2 与第七步一致、气口有 `pause`；Picture 1–6 整集统一无重排、每段不超 5 张；雨量与曝光两条恒定约束在 P01 提示词内三处落地。

**待决定**：那颗卧蛋要不要在拍5 里被老周自己夹走（给一个"他还在守"的实拍动作，但会把话说满，削弱留白）。

**交付文档（.docx，结构见 `templates/final-delivery.md`）**
```
第一部分｜剧本总览
  1.1 项目定义（原创：项目名、logline、用户原话、世界前提）
  1.2 情节总览　1.3 世界与故事背景
  1.4 主要角色（附 角色卡 角色01-造型A、角色02-造型A）
  1.5 场次与场景（附 场景卡 场景01，含 V01–V06）
  1.6 关键道具（附 道具卡 道具01、道具02）
  1.7 风格统一基调
第二部分｜分镜执行
  段落 P01｜00:00.000–00:15.000｜SB-01
    剧情推进 → 本段用图（Picture 1–3）→ 六段式全文 → 分镜表 → 两张故事板
  段落 P02 … P04 同构
```
第一部分不出现时间码与镜号；第二部分每段自包含，单独抽出即可执行。

---

## S14 ComfyUI 填表包

```text
package/
  Picture-映射表.md
  参数清单.md
  P01/
    prompt.txt          ← 上面 S8 那段，一字不改
    negative.txt
    refs/
      Picture1_角色01-造型A.png
      Picture2_场景01-V02.png
      Picture3_道具01.png
      Picture6_道具02.png
    handoff/
      P01-first.png     ← 取自 cells/P01-KF01.png
      P01-last.png      ← 取自 cells/P01-KF06.png，供 P02 承接
    sheet.md
  P02/ … P04/
```

> `P02` 的 `<Continuity>` 就写接 `handoff/P01-last.png`；`P02` 的 `handoff/P02-first.png` 与 `P01-last.png` 必须接得上（人物、服装、位置、光位、构图方向五项）。当前纯参考模式下这两帧只作比对，工作流支持首帧输入后 `P01-last.png` 直接接进 `P02` 的首帧槽。

**P01 填表单（`sheet.md` 摘要）**

| 项 | 内容 |
|---|---|
| 段落 / 时间码 / 时长 | `P01` ／ `00:00.000–00:15.000` ／ `15s` |
| 镜头数 / 故事板 | 3 ／ `SB-01`（`table` / `raw`） |
| 风格卡 | `DIERFEN-STYLE-v1` |
| 节点时长 | `15s`（节点可调，本段一次生成） |
| 上一段 | `—`（首段） |
| 承接 | `<Continuity>: none` ／ `handoff/P01-first.png`、`P01-last.png` 已落盘，`P01-last.png` 交 `P02` 承接 |

| 槽位 | 资产编号 | 文件 | 裁切区 |
|---|---|---|---|
| Picture 1 | 角色01-造型A | `Picture1_角色01-造型A.png` | 半身主视觉 `[0.02,0.08,0.26,0.615]` |
| Picture 2 | 场景01-V02 | `Picture2_场景01-V02.png` | 场景卡左下格 `[0.03,0.558,0.63,0.93]` |
| Picture 3 | 道具01 | `Picture3_道具01.png` | 道具卡左上格 `[0.05,0.12,0.485,0.468]`（仅 SH02、SH03 连） |
| Picture 4 | — | 本段不用 | — |
| Picture 5 | — | 本段不用 | — |
| Picture 6 | 道具02 | `Picture6_道具02.png` | 道具卡左上格 `[0.05,0.12,0.485,0.468]`（仅 SH02 连） |
| Picture 7–9 | — | 本段不用，不连节点 | — |

> **槽位可以不连续。** 本段用 1、2、3、6，中间的 4、5 空着不连——编号是整集统一的资产身份，不是段落内的顺序，不必为了"看着整齐"把 6 挪到 4 的位置。
>
> Picture 4（`场景01-V03` 角落的桌）留给 P02–P04，Picture 5（角色02）只进 P03–P04。**Picture 4 的裁切区要按卡面右列第 1 格实际量取，不能套用 V02 的 `[0.03,0.558,0.63,0.93]`**——那个坐标取的是左下格，套错了会裁到中缝与格框。Picture 5 用与 Picture 1 同一卡型坐标 `[0.02,0.08,0.26,0.615]`。
>
> 道具卡的裁切区两张相同（都是左上格），因为卡型一致；**但角色卡与道具卡的坐标不能互借**——`[0.02,0.08,0.26,0.615]` 在 5:6 的道具卡上是错的画幅比例。

| 参数 | 值 |
|---|---|
| 分辨率 | 1920×1080（成片画幅 16:9，按本机节点档位填） |
| 时长 | `15`（不大于本段实际时长） |
| 帧率 | 工作流默认 |
| seed | 首次试跑固定 `20261102`，后续改内容不改 seed |
| 工作流版本 | H3 Ref2VA（本机工作流版本号须自行记录） |

**提交前三件事**：① 四层检查（内容／衔接／文件／成本）逐项过；② 报告本次消耗（**含 13 张图的总数与单段试跑的费用**）；③ 建议先试跑 **P01**——纯动作、无台词、单人出镜，是验证"服装锁定＋雨量恒定"成本最低的一段；但**风险最高的一段其实是 P03**（黄色雨衣第一次出场，模型最容易把它画小、画成卡通），P01 过了一定要单独看 P03。

> **此处提交 `生产包确认`。** 通过后才导出 Word。填表包只是执行单，按下运行的永远是用户。

---

## 验收要点

- 一句话是**唯一的** `[来源]`，其余每条都能追到 `[创作]` 或 `[设定]`，没有一条假装是原句给的
- 世界规则 W01–W04 各自约束过一次具体行动（W01 管"先擦桌后下面"、W02 管拍5 的犹豫、W03 管拍3 的侧目、W04 管全片的雨）
- want（把早晨做完）与 need（承认没人会来）不同；阻力可拍；弧光落在"站住说完那句话"这个动作上
- 6 拍每拍只改一项，第 6 拍是选择（第一次不倒汤），不是领悟
- **两个人物一个给弧光、一个不给**；小女孩全片不解释、不给反转
- **全片只有一句台词**，且只出现在 P04；P01 刻意无台词
- 第二角色出卡有判定依据（被拍的画面主体＋跨段＋文字写不住），成本在 G3 报清
- 段落 4×15 秒，每段关键帧 N 默认 6（短段可降到 2–3 格）；P01 是 3 镜 6 帧，**镜头数 ≠ 关键帧数**，六段式按 3 个 `[Shot N]` 写
- 语速返工是"太快"型：24 字压进动作满的 8 秒镜 = 4.8 不合格 → **拆镜（说话独立成镜）＋台词砍到 8 字**，得 3.2 ✓；**动作越多能装的台词越少**
- 六段式三层加固齐备：`subject_definitions` 拆部件＋`LOCKED`＋`EXPLICITLY NOT`；`summary` 开头大写重申；`detailed_description` 开头再重申，且每镜重复服装关键词
- **两条恒定约束各自被写死**：曝光值恒定（防六格色温分裂，写在第 2 句）、雨量恒定（防中途停雨，写在三处）
- Picture 1–6 整集统一，每段不超 5 张
- 全片 13 张图（2 角色卡＋1 场景卡＋2 道具卡＋8 故事板），成本在 G3 后一次报清
