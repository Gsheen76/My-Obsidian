---
title: Petpet 总档案
type: project
tags:
  - project/petpet
  - PyQt5
  - desktop-pet
  - ai-companion
  - Python
  - 工程协作
summary: 项目级总览：定位与当前状态、功能总览、架构、版本演进、维护约定与档案馆索引。日志与细节一律在分类目录。
status: active
version: v1.6.3
platforms: Windows 10/11, macOS Apple Silicon
source: D:\Agent_project\Petpet
updated: 2026-09-02
migrated: 2026-08-05
---

# Petpet 项目总档案

> [!summary] Summary
> Petpet 是一个运行在桌面上的治愈系陪伴小狗：它有透明置顶窗口、拖拽和物理弹跳、连续帧动画、喂食/抚摸/玩耍/睡觉等互动、成长与 Pet 币经济、装扮商店、小游戏、可装修家园、健康提醒、托盘入口，以及支持默认免费文字服务与个人 GLM 图文模式的多轮流式聊天。

> [!info] 本档案只放"总"的东西
> 单轮开发日志 → `开发记录\`；发布细节 → `发布系统\`；设计决策 → 各系统目录。归类与命名规则见 [[文档规范]]。

## 1. 项目定位与当前状态

- **当前公开版本**：`v1.6.3`，版本唯一来源是 `version.py` 中的 `VERSION = "1.6.3"`。
- **发布提交**：`6fe90fa`；标签 `v1.6.3` 与远端 `main` 一致。
- **最近公开标签**：`v1.6.3`；[GitHub Release](https://github.com/Gsheen76/Petpet/releases/tag/v1.6.3) 已公开，包含 Windows exe/zip、macOS arm64 资产及 SHA256 清单。
- **运行平台**：Windows 10/11、macOS Apple Silicon。自 `v1.6.1` 起停止发布 Intel Mac 版本，Intel 用户留用 `v1.6.0`；更新器遇跨架构资产直接判为无适用安装包。
- **技术栈**：Python 3.11、PyQt5、Pillow、NumPy；发布版使用 PyInstaller。
- **当前开发状态**：v1.6.3 已公开发布（2026-09-01，发布日期以 git 标签与 GitHub Release 为准）。发布后进行中（均未推送）：小屋胶囊按键两段式按压反馈（`5e9713f`）；宠物详情面板新素材逐轮重建——十九轮完成：头像对齐烘焙框、X 缩小、`_ArtTitle` 艺术字标题、改名框缩小右移+名字写入、简介删名字与进度条、商店琥珀字色（`2e4c5f9`..`df82cc8`），**长期规则：所有按键必须带悬停+点击两态反馈**（见 [[宠物详情面板新素材重建记录]]）。
- **最近验证**：offscreen 全量测试 **706 passed**（2026-09-01，第十九轮）、Windows 平台交互/像素实测、精确重启 EnumWindows 验证可见（验证流程四步见 §10.1）。
- **源码位置**：`D:\Agent_project\Petpet`。
- **本笔记位置**：`D:\Github Desktop\My-Obsidian\项目\Petpet\Petpet 总档案.md`。

项目是一个本地优先的单用户桌面应用。除 AI 聊天请求外，养成、动画、装扮、小游戏、设置和数据迁移均可离线完成。发布包不打开命令行窗口，并通过 Windows 托盘或 macOS 菜单栏入口控制显示、设置、更新和退出。

### 当前实现重点

- 视觉语言已锁定：温暖奶油/珊瑚系（底色 `#fff9ee`、主色 `#f28f76`）、圆角胶囊控件、全局幼圆字体（统一走 `petpet/app/fonts.py`）。
- 常驻面板（商店/成就/记录/设置/小游戏/聊天）统一 850×960 暖色素材风格；家园主视口宽 700，家园窗口不置顶。
- 多宠物架构：宠物按 ID 注册（`assets/runtime/pets/manifest.json`），存档分"玩家共享 + 每宠独立"两层。
- macOS 使用 `Qt.WA_MacAlwaysShowToolWindow` 保持小狗失去焦点后仍显示在最顶层；默认宠物窗口 `150 x 180`，绘制高度 `132`。
- `parameter_tuner.py` 是源码调试工具，通过滑块和精确数值框实时修改物理、尺寸、动画、状态衰减、成长反馈和小游戏参数；参数可存 `debug_parameters.json` 续调；正式冻结版不显示调试入口。

## 2. 用户可见功能

### 桌面宠物

- 透明无边框小狗窗口，默认置顶，可拖拽移动。
- 拖动时使用拖拽姿态；释放后回到待机或自主移动状态。
- 小狗可在屏幕上行走、弹跳、休息、睡觉和做互动动作。
- Windows 使用 Per-Monitor V2 DPI 策略保持宠物、窗口、控件的 authored pixel 尺寸稳定，文字单独调整，减少不同缩放比例造成的布局漂移。
- 支持单实例：重复启动不会打开第二只宠物，而是唤醒已有实例。
- 支持托盘/菜单栏显示、隐藏、回到屏幕中央、设置和退出。

### 直接互动

| 操作 | 行为 |
|---|---|
| 左键单击 | 抚摸小狗，提升心情/好感并播放音效或动作 |
| 左键双击 | 打开 AI 聊天窗口 |
| 左键拖动 | 移动或弹飞小狗，触发拖拽姿态 |
| 睡觉时按住左键左右晃动 | 摇醒小狗 |
| 右键 | 打开成长卡与快捷气泡菜单 |
| 托盘/菜单栏双击 | 显示或隐藏小狗 |

快捷菜单分为两页：主操作包含喂食、玩耍、聊天、睡觉等；“更多”包含小游戏、记录、成就、商店、设置、教程、更新、显示/隐藏和退出。

`v1.4.0` 快捷菜单改为一行五个主入口：聊天、小屋、商店、互动、更多。互动页为抚摸、喂食、玩耍、睡觉；更多页保留记录、成就、小游戏、设置、隐藏、教程、返回和退出。

### 养成与状态

- 核心状态：饥饿、心情、精力、位置、睡眠、等级、经验、好感等级/好感点、Pet 币。
- 互动带独立冷却：抚摸、喂食、玩耍、接球、聊天、摇醒、手动睡觉、休息气泡等不会无限刷好感。
- 心情、饥饿、精力会随时间衰减；睡眠期间精力恢复，低精力会触发自动休息。
- 精力低于约 30% 时可自动走到最近屏幕角落睡觉，恢复到约 80% 后自动醒来；手动睡觉仍由玩家控制。
- 好感等级决定被动经验基础速率；经验、等级和好感均可从旧存档自动补齐。
- “持久活力”强化可降低清醒状态下饥饿/心情/精力的自然消耗，上限为 5 级，最高约减免 50%。

### 记录、成就与 Pet 币

- **温暖记录**：相识时长、实际运行时长、Pet 币收入/消费、抚摸、喂食、玩耍、睡觉、接球、聊天、摇醒、启动、升级等统计；v1.6.2 起按宠物分页，总计页共享数值。
- **成就**：按陪伴天数、互动总量、喂食、睡觉、玩耍、接球、聊天、等级、Pet 币、装扮、强化、已领取成就、小游戏等维度解锁；成就需在页面手动领取奖励；v1.6.2 起合并为六大类筛选。
- **等级成就**：每次升级自动生成对应的等级成就，旧存档也可以补领。
- **Pet 币来源**：成就奖励、小游戏奖励、随机挖宝奖励；余额、收入、消费均记录在存档中。
- **随机挖宝**：每分钟进行低概率检查，发现后进入 20 分钟冷却；奖励随机分层，领取前保存在 `pending_dig_reward`，播放约 30 帧、20 FPS 的发现动画后入账，防止重复领取。

### Pet 币商店与装扮

- 商店分为“装扮”和“强化”两栏，v1.6.1 起整体素材化（背景/价格签/徽章/页签图标来自 `assets/runtime/ui/shop/`）。
- 强化项目：`petting`（抚摸）、`feeding`（喂食）、`playing`（玩耍）、`sleeping`（睡眠）、`experience`（经验）、`endurance`（持久活力），每项最多 5 级，价格逐级增加。
- 装扮按 `head`、`neck`、`eyes`、`body` 四个槽位管理；支持购买/领取、试戴、装备、卸下、分类浏览；试戴使用独立状态，不污染真实购买记录。
- 待机装扮是独立透明 PNG 图层，可同时叠加帽子、眼镜、项圈等；支持拖动位置、缩放、旋转角度、恢复默认。
- 行走、睡觉、进食、抚摸、接球等复杂动作期间暂不叠加待机装扮，避免尾巴残影、错位和遮挡。
- 套装（outfits）可带专属动画（如恐龙装拖拽 8 帧），未装备时回退共享动画。

### 小游戏

`minigames.py` 提供可扩展的小游戏中心，目前包含两种 capped Pet 币玩法：

1. **金币雨/接金币（Coin Catch）**：20 秒一局，点击移动金币目标；显示命中数、最佳连击、剩余时间和本局 Pet 币。
2. **幸运爪爪（Lucky Paws）**：3 轮猜碗，奖励分别为 5、10、15 Pet 币；轮次越高交换速度越快。

每局结束统一通过 `progression.award_minigame_coins` 结算，写入最佳成绩和小游戏收入记录。小游戏中心保留后续扩展位置。

### 家园、装修与小屋宠物

- 家场景固定在屏幕右下区域，主画布为 `700×768`（世界 `1800×768`，相机跟随）；装修侧栏位于画布左侧，不会遮挡场景。
- 家具卡片采用两列布局，图片按原比例居中；家具支持购买、放置、拖动、缩放、旋转、收纳和变换存档。
- 装修时隐藏小狗并显示左右视角按钮；退出装修只关闭侧栏，不退出家场景；非装修模式下空白处按住可拖动整个小屋窗口。
- 家园右下角为双图标互斥菜单：左「交互」弹出抚摸、喂食、玩耍、睡觉，右「菜单」弹出商店、装修、退出；胶囊按键有 hover/按压反馈，动作在反馈播完后触发。
- 小屋内左键指定移动目的地；路线由固定脚印组成；小屋内右键小狗沿用桌面快捷菜单与对话体验。
- `home_pet.py` 管理 2.5D 地面坐标、四向移动、寻路目标、自动睡眠和存档位置；纵深不改变宠物显示尺寸。
- 无指令时播放正坐待机素材；手动或低精力睡眠会先走到地毯，再播放 8 帧、`3 FPS` 的睡眠动画。
- 小屋动画缺图时保留可见占位回退，避免状态机或交互因素材缺失而中断。

### AI 聊天

- 聊天模式由玩家明确选择“免费聊天”或“自己配置”；保存个人 Key 不会自动改变当前模式。
- 免费聊天优先直连阿里云函数的智谱 `glm-4.7-flash`；阿里云连接前失败或本地额度耗尽时，才尝试 Cloudflare Worker。Cloudflare 仍按 GLM 优先、OpenRouter 免费路由兜底。
- 首次默认聊天必须明确同意数据说明；阿里云由桌面客户端按北京时间本地记录 20 次/日，Cloudflare 由 Durable Object 独立记录 20 次/UTC 日，每次回复最多 200 个输出 token。
- 默认模式只支持文字。额度耗尽、代理未部署或上游不可用时显示中性系统提示，立即解锁输入框，不把错误伪装成小狗台词。
- 自己配置模式使用玩家保存的智谱 `glm-4.6v-flash` Key；可上传单张 PNG、JPG/JPEG 或 WEBP 图片（最大 10 MiB）进行图文聊天。
- 原图仅用于当前智谱请求，聊天记忆不保存原图、路径或 Base64；本机仅保存 320 px 历史缩略图，移除待发送图片或清除记忆会清理对应缩略图。
- 支持流式输出、最近多轮历史、轻量 `user_profile`、宠物名字同步、时间问候、关键词情绪识别和主动 nudge；聊天小狗回复清洗掉开头吠叫类口癖。
- 本地版本化游戏知识库会把相关已发布玩法注入系统提示；玩家可直接询问小屋、家具、互动、成长、商店、小游戏和图片聊天。
- API Key 优先级：环境变量 `ZHIPU_API_KEY` > 本地 `config.json`。
- 旧 `glm-4-flash` / `glm-4.7-flash` 配置首次读取时迁移到当前模型；此后 `chat_mode` 与 Key 分开保存，免费模式不会使用已保存的个人 Key。
- 记忆历史最多保留 60 条消息；每累计约 6 次用户发言尝试后台刷新一次用户画像，失败静默处理。
- 绝不把真实 API Key 写入 Git；项目中的 `config.json.example` 只放占位符。

### 健康提醒与教程

- 可配置喝水、休息、站立活动提醒，默认分别为 60、90、45 分钟。
- 首次启动显示分步新手教程，完成后为宠物命名；名字同步到状态、聊天记忆、托盘和成长卡。
- 可从右键菜单“更多 → 教程”重新打开或修改名字。

### 更新与数据迁移

- 默认启动约 5 秒后检查 GitHub Releases，也可从托盘或右键菜单手动检查。
- 更新器会按平台和 CPU 架构选择 Windows `.exe`/ZIP 或 macOS arm64 ZIP，下载后校验、解压并交给平台更新流程。
- Windows 原位替换 `Petpet.exe`，保留 `%LOCALAPPDATA%\Petpet` 用户数据，清理临时更新目录并自动重启。
- macOS 生成 `Petpet.app`，数据保存在 `~/Library/Application Support/Petpet`。
- `app_paths.py` 负责把旧版本根目录或 `update/updates/updata` 目录中的数据迁移到稳定目录，只复制缺失文件，不覆盖已有数据。

## 3. 程序架构

```text
pet.py
├── petpet/
│   ├── app/           路径、存档、设置与桌面宠物控制器；多宠物状态与资源注册
│   ├── chat/          配置、记忆、知识库、提示词、网络传输与聊天 API
│   ├── home/          家园宠物、几何、渲染与家园窗口
│   ├── progression/   玩家成长规则、记录、成就和商店窗口
│   ├── minigames/     金币雨、幸运爪爪和小游戏入口
│   └── ui/            聊天、设置、教程、桌面浮层、装饰与公共控件
├── app_paths.py 等    根目录兼容入口，不复制业务逻辑
└── updater.py         版本检查、资产选择、下载、替换与清理
```

### `pet.py`：主应用与交互层

- 初始化 Qt、DPI、单实例服务、托盘图标和主宠物窗口。
- 加载/保存 `pet_state.json` 与 `pet_settings.json`，维护主循环、位置、状态衰减和动作触发。
- 提供 `ChatWindow`、`StatsWindow`、`SettingsWindow`、`TutorialWindow`、`BubbleMenu`、`SpeechBubble`、`FetchPlayScene` 等 UI。
- `PetWindow` 负责透明窗口、动画帧加载、自动行走、拖拽/弹跳、喂食/抚摸/睡觉/接球和主动气泡。
- `TrayApp` 负责 Windows 托盘/macOS 菜单栏入口、更新、设置和退出。

### `petpet/`：业务实现

- `petpet.app` 维护跨平台资源/数据路径、玩家共享与宠物独立存档、设置和桌面 `PetWindow` 控制器；多宠物边界见 [[宠物系统/多宠物系统设计]]。
- `petpet.chat` 维护聊天模式、配置、独立记忆、游戏知识、提示词和 HTTP/SSE 传输；根目录 `buddy_ai.py` 保持模块别名兼容。
- `petpet.home` 维护家园宠物的 2.5D 行为、场景几何、渲染规则与窗口控制器。
- `petpet.progression` 和 `petpet.minigames` 分别承载纯成长规则/窗口及小游戏窗口。
- `petpet.ui` 承载聊天、设置、教程、桌面气泡菜单、装饰和可复用控件。

根目录旧模块只保留为历史导入兼容面；包内实现不反向依赖这些兼容模块。

### `petpet.progression.core`：纯养成规则层

关键职责：

- `ensure_progression`：对旧存档做默认值补齐、数值边界归一化、装扮槽位修复、成就列表去重。
- `record_action` / `record_sleep`：统一写入互动统计，并按动作冷却发放好感。
- `add_affection` / `affection_to_next`：好感升级与升级事件。
- `record_xp` / `passive_xp_per_second`：被动经验和成长速度。
- `add_coins` / `award_minigame_coins` / `roll_dig_reward`：Pet 币来源与结算。
- `purchase_upgrade` / `upgrade_effects`：强化价格、等级上限和实际效果。
- `purchase_decoration` / `equip_decoration` / `set_decoration_transform`：装扮资产状态管理。
- `achievement_catalog` / `claim_achievement`：成就生成、可领取判断和奖励入账。

该模块尽量不依赖 UI，便于测试、存档迁移和未来替换界面。

### `petpet.chat.api`：AI 适配层

默认代理通过正式运行依赖 `requests` 连接并解析 SSE；个人智谱请求继续使用轻量 HTTP 适配，不依赖供应商 SDK。主要流程：

```text
用户输入
  → 读取玩家显式选择的 chat_mode、个人 API Key、默认聊天同意状态与 memory.json
  → 构造宠物人格、时间、情绪、用户画像和最近历史
  → 免费模式：阿里云 glm-4.7-flash 优先、Cloudflare 独立额度兜底；自己配置：个人智谱 GLM-4.6V
  → UI 逐 token 更新
  → 写入 history、统计 ai_replies
  → 默认额度/服务错误显示中性提示；普通接口错误使用友好 fallback
```

### `petpet.progression.ui` 与 `petpet.minigames.ui`：窗口层

两者复用 `CozyProgressWindow` 的暖色主题（`shop_theme` 素材化）、统一 850×960 尺寸和按钮布局。UI 只调用 `progression.core` 的规则函数，保存由主窗口回调完成。

### `petpet.ui.decorations`：装扮绘制

负责透明像素裁剪、按宠物边界适配、旋转后的包围盒计算、图层绘制和待机装扮组合。装扮的归一化位置和缩放范围由 `progression.core` 校验，避免非法存档造成 UI 崩溃。

### `updater.py`：更新器

包含版本比较、Release 资产评分、平台/架构选择、GitHub API 失败时页面兜底、下载进度、Windows 解压/原位替换、旧更新目录清理和 macOS 打开更新包等流程。

## 4. 资源与动画

运行资源与制作素材在 `assets/` 下物理分离。两个 PyInstaller spec 只收集 `assets/runtime/`：

| 目录 | 内容 |
|---|---|
| `assets/runtime/pets/<pet_id>/desktop` | 桌面宠物静态姿势（`poses/`）、连续帧动画（`animations/`）、套装（`outfits/`） |
| `assets/runtime/pets/<pet_id>/home` | 家园宠物待机、移动与睡眠素材 |
| `assets/runtime/pets/manifest.json` | 宠物注册表：id、默认名、性格、价格/折扣、preview、avatar、入口 |
| `assets/runtime/scenes/home` | 家背景与导航反馈 |
| `assets/runtime/furniture/home` | 地毯、沙发、绿植与壁画 |
| `assets/runtime/ui/shop` | 商店/面板暖色素材包 |
| `assets/runtime/decorations`、`props`、`sounds`、`icons`、`knowledge` | 装扮、道具、音效、图标与玩家知识库 |
| `assets/source/spritesheets`、`references` | 精灵表与制作参考图（不进入安装包） |

每套动画由 `assets/runtime/pets/<pet_id>/desktop/animations/manifest.json` 声明（`folder`、`fps`、`loop`、`fallback`、可选 `frame_sequence`/`frame_durations_ms`）；缺少动作目录时回退 `poses/` 静态图。所有帧与姿势必须同尺寸、主体大小一致、脚底阴影对齐。制作约束记录在 `assets/source/spritesheets/README.md`。

## 5. 本地数据与隐私

### 数据目录

| 运行方式 | 数据目录 |
|---|---|
| 源码运行 | 项目内 `data/` |
| Windows 冻结版 | `%LOCALAPPDATA%\Petpet` |
| macOS 冻结版 | `~/Library/Application Support/Petpet` |

### 文件说明

- `config.json`：API Key、自动聊天模式、默认聊天同意状态、安装 ID 与公开代理地址。敏感信息只保存在本地。
- `memory.json`：当前宠物的 AI 多轮历史、用户画像、宠物名字和主动 nudge 时间；切换宠物时使用各自的聊天记忆。
- `pet_state.json`：玩家共享的等级、经验、Pet 币、记录、成就、家具、强化和小游戏进度，以及每只宠物独立的属性、好感、昵称和场景位置。
- `pet_settings.json`：窗口尺寸、字体、置顶、更新检查、健康提醒、音效、衰减速度和主动聊天频率。

当前存档兼容层已覆盖 v1.4.0 字段，包括 `home_scene`、`owned_home_decorations`、`home_decoration_positions`、家具变换和小屋宠物位置；不要把真实用户存档或真实 API Key 提交到仓库。

### 存档兼容策略

`pet.py` 先合并 `DEFAULT_STATE`，再调用 `progression.ensure_progression`；`app_paths.py` 负责旧路径迁移。升级不会重置名字、等级、经验、好感、Pet 币、设置、API Key 或聊天记忆，只会为新增字段补默认值并修正越界值。

## 6. 开发、测试与构建

### 源码运行

建议 Python 3.11：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements\runtime.txt
python pet.py
```

macOS：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/runtime.txt
python pet.py
```

首次运行会创建 `data/config.json`，并把旧版根目录数据迁移到 `data/`。

### 测试

```powershell
$env:QT_QPA_PLATFORM = 'offscreen'
python -m pytest -q
```

测试覆盖状态机、聊天、成长规则、UI 边界、更新器、单实例和打包元数据；当前全量结果：**668 passed**（约 80–110s）。Windows 平台渲染验证需真实桌面字体库（offscreen 无字体数据库）。

### Windows 构建

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_windows.ps1
```

脚本会在 `.build_deps/` 安装构建依赖、生成图标，然后执行 `PyInstaller packaging\Petpet-windows.spec`。产物：`dist/Petpet.exe`。一键发版走 `scripts\release.ps1 -Version X.Y.Z`。

### macOS 构建

必须在 macOS 或 GitHub macOS Runner 上执行：

```bash
chmod +x scripts/build_macos.sh
./scripts/build_macos.sh
```

产物为 `dist/Petpet.app`。`.github/workflows/` 使用 `macos-15` 构建 arm64 ZIP。macOS 当前未做 Developer ID 签名和公证，首次打开可能需要在“系统设置 → 隐私与安全性”中选择“仍要打开”。

## 7. 文件索引

```text
Petpet/
├── pet.py                         稳定源码与打包启动入口、Qt 生命周期和托盘编排
├── version.py                     唯一版本号
├── petpet/                        实际业务包：app/chat/home/progression/minigames/ui
├── app_paths.py 等                旧导入兼容转发层
├── updater.py                     自动更新
├── config.json.example             安全配置模板
├── cloudflare-worker/             海外兜底聊天代理与 Durable Object 独立额度
├── aliyun-chat/                   大陆优先 glm-4.7-flash Web 函数
├── assets/runtime/                唯一进入安装包的运行资源
├── assets/source/                 不进入安装包的精灵表与参考图
├── data/                          本地运行数据（不应提交敏感内容）
├── docs/                          TODO 与各版本发布说明
├── packaging/                     Windows/macOS PyInstaller spec
├── requirements/                  runtime/build 依赖
├── scripts/                       构建/发布入口
├── tests/                         自动化测试
├── tools/                         动画导入、图标/音效等工具
└── .github/workflows/             macOS 构建工作流
```

## 8. 版本演进摘要

| 版本 | 主要内容 |
|---|---|
| `v1.0.0` | 初始桌面宠物、基础交互和后续 TODO |
| `v1.1.0` | 治愈系 UI、右键成长卡、互动气泡、健康提醒、音效 |
| `v1.1.1` | 修复 UTF-8 BOM 导致 AI Key 无法读取 |
| `v1.2.0` | 连续帧动画、应用内更新、设置重构、macOS 双架构构建和数据目录整理 |
| `v1.2.1` | 新手教程、宠物命名、更多功能画布和气泡重绘修复 |
| `v1.2.2` | 睡眠呼吸、摇醒互动、单实例、数据迁移和气泡可靠性修复 |
| `v1.2.3` | Windows 原位更新、跨 DPI 固定界面尺寸和独立字体体系 |
| `v1.2.4` | 抚摸、接球、自动休息、应用内 API Key 配置 |
| `v1.3.0` | 温暖记录、成就、Pet 币、好感、强化商店、装扮基础版、2D 分层基础 |
| `v1.3.1` | 待机装扮图层、试戴预览、装扮微调、持久活力、挖宝事件、24 FPS 玩耍、气泡修复 |
| `v1.3.2` | 小游戏中心、参数调试器、聊天提示、动画时长与 Windows 更新可靠性修复 |
| `v1.4.0` | 五入口快捷菜单、家场景、家具装修、2.5D 小屋宠物、脚印寻路、正坐待机与 3 FPS 睡眠动画 |
| `v1.4.1` | 免费/个人图文聊天、玩法知识库、双方头像、暖色圆角聊天、三档设置与六页教程 |
| `v1.5.0` | 家园宠物行为、独立好感成长、状态卡家具、宝藏与属性 UI、阿里云优先免费聊天、GLM-4.7-FlashX |
| `v1.6.0` | 多宠物系统、按宠物动画与聊天人格、商店信息改版、家园/桌面同步 |
| `v1.6.1` | 商店素材化换装、成就页重构、全局幼圆字体、家园双图标菜单；停发 Intel Mac 包 |
| `v1.6.2` | 面板统一 850×960 暖色系、成就六大类筛选、温暖记录按宠分页、聊天头像与口癖清洗 |
| `v1.6.3` | 家园性能大修（paintEvent ~100ms→~2ms）、按键按压反馈、实测影子、恐龙装拖拽、小屋可拖动 |

逐版本的发布细节见 [[发布系统/版本规划与发布索引]]。

## 9. 历史产品路线与维护风险

### 早期路线（历史记录，不作当前排期）

- 多屏与贴边：使用 `QScreen.availableGeometry()`，支持多显示器、贴边吸附和不同分辨率。
- macOS 真机验收：菜单栏交互、Retina 缩放、多屏、签名与公证。
- 补齐 `idle`、`play`、`happy`、`sleep` 等动画素材，并继续补充 `sad`、`drag`、`sit`、`ask`。
- 增加更多商店物品、稀有零食、小窝和待机装扮。
- 成就相册：把重要成就和瞬间保存成可浏览相册。
- 自定义主题/造型、多只宠物共享主题。
- 开机自启异常恢复与崩溃自动重启完善。
- 长期记忆：结构化记录用户姓名、生日、重要事件，并在后续对话中自然召回。

### 维护风险

- PyQt5、系统 DPI、透明窗口和托盘行为具有平台差异，改动 `pet.py` 的窗口几何时必须补 Windows/macOS 回归验证。
- 自动更新属于高风险流程，修改 `updater.py` 后应同时运行 `tests/test_updater.py`、`tests/test_windows_packaging.py`，并检查旧数据不会被覆盖。
- 动画目录和 `manifest.json` 必须保持同步；缺帧虽有静态回退，但会改变动作体验。
- AI 依赖网络与第三方服务，所有面向用户的聊天流程都必须保留离线 fallback。
- 当前 `data/` 是工作区示例数据，发布或共享前应确认没有真实 API Key、个人对话或不希望公开的存档。

## 10. 日常维护清单

1. 修改版本时只更新 `version.py`，再同步发布说明和构建产物名称。
2. 新增存档字段时同时更新 `DEFAULT_STATE`、`progression.ensure_progression`、相关 UI 和测试。
3. 新增动画时更新对应宠物的 `assets/runtime/pets/<pet_id>/desktop/animations/manifest.json`，检查静态 fallback 和打包 spec。
4. 新增 Pet 币收入/消费时调用 `add_coins` 或对应统一结算函数，确保 records 统计完整。
5. 新增装扮时同时登记分类、价格、默认变换参数、资源文件和测试。
6. 提交前运行 `python -m pytest -q`，并确认 Git 状态没有 `data/config.json` 中的真实密钥。
7. 发布 Windows 前运行 `scripts\build_windows.ps1`；发布 macOS 前在 Runner 构建并验证 ZIP 内层确实是 `Petpet.app`。
8. 任何开发轮次收尾按 [[文档规范]] 写入 Obsidian 对应目录；仓库 `HANDOFF.md`/`AGENTS.md` 变更后同步副本到 `工程结构\`。

## 10.1 协作与验收约定

- 用户说 `add tweaks` 时，理解为小幅、局部、可控的参数调整，不擅自扩大改动范围。
- 任何参数微调优先加入参数调试器，确保可以实时试验，避免反复对话猜数值。
- 修改桌面程序的功能、交互、窗口行为、动画或视觉样式后，先运行相关测试；改动涉及共享行为时运行完整 `python -m pytest -q`。
- 视觉改动的完成门（四步，缺一不可）：offscreen 全量测试 → Windows 平台截图/像素实测 → 精确重启（EnumWindows 验证可见） → Obsidian 记录。切勿在未验证可见性的情况下假设代码生效。
- 涉及聊天窗口、气泡、菜单、商店等视觉改动时，先生成本地渲染或截图检查实际效果；不能仅依据 QSS/代码文本判断。Qt 富文本对圆角等 CSS 支持有限，消息气泡优先使用原生 Qt 组件渲染。
- macOS 验收重点：小狗失去应用焦点后仍保持可见且置顶、Retina 尺寸不应过大、聊天界面文字和背景对比舒适。macOS 专属改动应在真机打包后复测。
- 视觉取向：避免高饱和、大面积的对话文字底框；消息样式优先采用低饱和浅色、深色文字、细边框、留白和实际可呈现的圆角。用户反馈"太高/太大/怪怪的"时以实测数据（px 差值、色彩统计）为准；反馈"反了"时禁止翻符号猜，从精灵 alpha 通道质心实测推导。
- 不回滚用户已有改动；提交前检查 `git status`，避免把运行数据、API key 或个人对话纳入发布。
- 源码调试入口：托盘菜单 → `调试` → `参数调试器`；正式发布版本不显示该入口。

## 11. 相关源码入口

- 主入口：`D:\Agent_project\Petpet\pet.py`
- 桌面宠物渲染：`D:\Agent_project\Petpet\petpet\app\pet_window.py`
- 养成规则：`D:\Agent_project\Petpet\petpet\progression\core.py`
- 家园场景：`D:\Agent_project\Petpet\petpet\home\window.py`
- AI 聊天：`D:\Agent_project\Petpet\petpet\chat\`
- 更新：`D:\Agent_project\Petpet\updater.py`
- 动画制作约束：`D:\Agent_project\Petpet\assets\source\spritesheets\README.md`
- 路线图：`D:\Agent_project\Petpet\docs\TODO.md`
- 当前发布说明：`D:\Agent_project\Petpet\docs\RELEASE_NOTES_v1.6.3.md`
- 公开下载：https://github.com/Gsheen76/Petpet/releases/tag/v1.6.3
- 测试目录：`D:\Agent_project\Petpet\tests`
- 长期工作约定（仓库侧）：`D:\Agent_project\Petpet\AGENTS.md` 与 `HANDOFF.md`（副本同步在 `工程结构\`）

## 12. 档案馆目录索引

| 位置 | 职责 | 主要入口 |
|---|---|---|
| [[文档规范]] | 归类/命名/写入规则（写库前必读） | — |
| [[源码启动]] | 源码运行指引 | — |
| `开发记录\` | 按日开发日志与修复记录 | [[开发记录/2026-08-27 成就分类筛选与弹窗交互完善]]（v1.6.1→v1.6.3 全程细节）、[[开发记录/2026-09-01 小屋按键两段式按压反馈]]（最新轮） |
| `发布系统\` | 发布说明/实施/索引、更新链路 | [[发布系统/版本规划与发布索引]] |
| `场景系统\` | 家园/装修/小屋 | [[场景系统/家场景系统设计]] |
| `宠物系统\` | 多宠物/动画 | [[宠物系统/多宠物系统设计]] |
| `聊天系统\` | 聊天/代理/知识库 | [[聊天系统/默认免费聊天代理实施记录]] |
| `菜单系统\` | 快捷菜单交互 | [[菜单系统/宠物快捷菜单交互记录]] |
| `设置系统\` | 设置/教程 | [[设置系统/暖色圆角设置与教程设计]] |
| `工程结构\` | 重构、工具、仓库↔Obsidian 同步件 | [[工程结构/项目代码与资源结构重构实施记录]]、[[工程结构/源码 Markdown 迁移索引]] |

## 关键概念

- project/petpet、pyqt5、desktop-pet、ai-companion、python
