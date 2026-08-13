---
title: Petpet 总档案
type: project
status: active
version: v1.4.1
platforms: Windows 10/11, macOS Intel, macOS Apple Silicon
source: D:\Agent_project\Petpet
updated: 2026-08-13
tags:
  - project/petpet
  - PyQt5
  - desktop-pet
  - ai-companion
  - Python
  - 工程协作
summary: 记录项目的定位、实现结构、当前状态和后续工作。
migrated: 2026-08-05
---

# Petpet 项目总档案

> [!summary] Summary
> Petpet 是一个运行在桌面上的治愈系陪伴小狗：它有透明置顶窗口、拖拽和物理弹跳、连续帧动画、喂食/抚摸/玩耍/睡觉等互动、成长与 Pet 币经济、装扮商店、小游戏、可装修家园、健康提醒、托盘入口，以及支持默认免费文字服务与个人 GLM 图文模式的多轮流式聊天。

## 1. 项目定位与当前状态

- **当前公开版本**：`v1.4.1`，版本唯一来源是 `version.py` 中的 `VERSION = "1.4.1"`。
- **发布提交**：标签 `v1.4.1` 指向 `8136eccd0ca44cbe6a38da44e67feafbef397626`；发布工具后续维护提交为 `f1d505d`。
- **最近公开标签**：`v1.4.1`；[GitHub Release](https://github.com/Gsheen76/Petpet/releases/tag/v1.4.1) 已于 2026-08-13 公开，包含 Windows 与 macOS 双架构四项资产。
- **运行平台**：Windows 10/11、macOS Intel、macOS Apple Silicon。
- **技术栈**：Python 3.11、PyQt5、Pillow、NumPy；发布版使用 PyInstaller。
- **测试状态**：`v1.4.1` 最终全量验证为 **407 passed in 40.42s**，发布脚本契约测试为 **16 passed**，Worker 契约测试为 **13 passed**；PowerShell AST、Python 编译、差异格式、Windows 构建与四项发布资产下载哈希均通过。
- **源码位置**：`D:\Agent_project\Petpet`。
- **本笔记位置**：`D:\Github Desktop\My-Obsidian\项目\Petpet\Petpet 总档案.md`。

项目是一个本地优先的单用户桌面应用。除 AI 聊天请求外，养成、动画、装扮、小游戏、设置和数据迁移均可离线完成。发布包不打开命令行窗口，并通过 Windows 托盘或 macOS 菜单栏入口控制显示、设置、更新和退出。

### 当前实现重点

- macOS 使用 `Qt.WA_MacAlwaysShowToolWindow` 保持小狗失去焦点后仍显示在最顶层，默认宠物窗口尺寸为 `150 x 180`，绘制高度为 `132`。
- 进食和摸头动画默认 `20 FPS`；聊天消息使用原生 Qt 圆角组件，底色保持低饱和、浅色、低对比。
- `parameter_tuner.py` 是源码调试工具，通过滑块和精确数值框实时修改物理、尺寸、动画、状态衰减、成长反馈和小游戏参数；正式冻结版不显示调试入口。
- 调试参数可保存到运行数据目录的 `debug_parameters.json`，用于下一次源码启动继续调试。

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

- **温暖记录**：相识时长、实际运行时长、Pet 币收入/消费、抚摸、喂食、玩耍、睡觉、接球、聊天、摇醒、启动、升级等统计。
- **成就**：按陪伴天数、互动总量、喂食、睡觉、玩耍、接球、聊天、等级、Pet 币、装扮、强化、已领取成就、小游戏等维度解锁；成就需在页面手动领取奖励。
- **等级成就**：每次升级自动生成对应的等级成就，旧存档也可以补领。
- **Pet 币来源**：成就奖励、小游戏奖励、随机挖宝奖励；余额、收入、消费均记录在存档中。
- **随机挖宝**：每分钟进行低概率检查，发现后进入 20 分钟冷却；奖励随机分层，领取前保存在 `pending_dig_reward`，播放约 30 帧、20 FPS 的发现动画后入账，防止重复领取。

### Pet 币商店与装扮

- 商店分为“装扮”和“强化”两栏。
- 强化项目：`petting`（抚摸）、`feeding`（喂食）、`playing`（玩耍）、`sleeping`（睡眠）、`experience`（经验）、`endurance`（持久活力），每项最多 5 级，价格逐级增加。
- 装扮按 `head`、`neck`、`eyes`、`body` 四个槽位管理，当前资源包含红色项圈、奶油贝雷帽、圆框眼镜、墨镜、小橙帽、天空蝴蝶结。
- 装扮支持购买/领取、试戴、装备、卸下、分类浏览；试戴使用独立状态，不污染真实购买记录。
- 待机装扮是独立透明 PNG 图层，可同时叠加帽子、眼镜、项圈等。
- 装扮调整支持拖动位置、缩放、旋转角度、恢复默认；选中框为高对比黄色。
- 行走、睡觉、进食、抚摸、接球等复杂动作期间暂不叠加待机装扮，避免尾巴残影、错位和遮挡。

### 小游戏

`minigames.py` 提供可扩展的小游戏中心，目前包含两种 capped Pet 币玩法：

1. **金币雨/接金币（Coin Catch）**：20 秒一局，点击移动金币目标；显示命中数、最佳连击、剩余时间和本局 Pet 币。
2. **幸运爪爪（Lucky Paws）**：3 轮猜碗，奖励分别为 5、10、15 Pet 币；轮次越高交换速度越快。

每局结束统一通过 `progression.award_minigame_coins` 结算，写入最佳成绩和小游戏收入记录。小游戏中心保留后续扩展位置。

### 家园、装修与小屋宠物

- 家场景固定在屏幕右下区域，主画布为 `900×768`；装修侧栏位于画布左侧，尺寸为 `338×768`，不会遮挡场景。
- 家具卡片采用两列布局，图片按原比例居中；家具支持购买、放置、拖动、缩放、旋转、收纳和变换存档。
- 装修时隐藏小狗并显示左右视角按钮；退出装修只关闭侧栏，不退出家场景。
- 小屋内左键指定移动目的地；路线由固定脚印组成，小狗走过的脚印逐步消失，终点使用倾斜椭圆和可爱箭头反馈。
- 小屋内右键小狗沿用桌面快捷菜单与对话体验；对话框使用暖色小屋主题并上移避开宠物。
- `home_pet.py` 管理 2.5D 地面坐标、四向移动、寻路目标、自动睡眠和存档位置；纵深不改变宠物显示尺寸。
- 无指令时播放正坐待机素材；手动或低精力睡眠会先走到地毯，再播放 8 帧、`3 FPS` 的睡眠动画。
- 小屋动画缺图时保留可见占位回退，避免状态机或交互因素材缺失而中断。

### AI 聊天

- 聊天模式由玩家明确选择“免费聊天”或“自己配置”；保存个人 Key 不会自动改变当前模式。
- 免费聊天使用项目方 Cloudflare Worker 转发的默认文字服务，当前上游为 OpenRouter 免费路由 `openrouter/free`。
- 首次默认聊天必须明确同意数据说明；免费模型可能有各自的数据使用条款。安装 ID 与来源 IP 各限制 20 次/UTC 日，每次回复最多 200 个输出 token。
- 默认模式只支持文字。额度耗尽、代理未部署或上游不可用时显示中性系统提示，立即解锁输入框，不把错误伪装成小狗台词。
- 自己配置模式使用玩家保存的智谱 `glm-4.6v-flash` Key；可上传单张 PNG、JPG/JPEG 或 WEBP 图片（最大 10 MiB）进行图文聊天。
- 原图仅用于当前智谱请求，聊天记忆不保存原图、路径或 Base64；本机仅保存 320 px 历史缩略图，移除待发送图片或清除记忆会清理对应缩略图。
- 支持流式输出、最近多轮历史、轻量 `user_profile`、宠物名字同步、时间问候、关键词情绪识别和主动 nudge。
- 本地版本化游戏知识库会把相关已发布玩法注入系统提示；玩家可直接询问小屋、家具、互动、成长、商店、小游戏和图片聊天。
- API Key 优先级：环境变量 `ZHIPU_API_KEY` > 本地 `config.json`。
- 旧 `glm-4-flash` / `glm-4.7-flash` 配置首次读取时迁移到当前模型；此后 `chat_mode` 与 Key 分开保存，免费模式不会使用已保存的个人 Key。
- 记忆历史最多保留 60 条消息；每累计约 6 次用户发言尝试后台刷新一次用户画像，失败静默处理。
- 发送有效消息会记录聊天互动；AI 成功回复会记录 `ai_replies`。
- 绝不把真实 API Key 写入 Git；项目中的 `config.json.example` 只放占位符。

### 健康提醒与教程

- 可配置喝水、休息、站立活动提醒，默认分别为 60、90、45 分钟。
- 首次启动显示分步新手教程，完成后为宠物命名；名字同步到状态、聊天记忆、托盘和成长卡。
- 可从右键菜单“更多 → 教程”重新打开或修改名字。

### 更新与数据迁移

- 默认启动约 5 秒后检查 GitHub Releases，也可从托盘或右键菜单手动检查。
- 更新器会按平台和 CPU 架构选择 Windows `.exe`/ZIP 或 macOS Intel/arm64 ZIP，下载后校验、解压并交给平台更新流程。
- Windows 原位替换 `Petpet.exe`，保留 `%LOCALAPPDATA%\Petpet` 用户数据，清理临时更新目录并自动重启。
- macOS 生成 `Petpet.app`，数据保存在 `~/Library/Application Support/Petpet`。
- `app_paths.py` 负责把旧版本根目录或 `update/updates/updata` 目录中的数据迁移到稳定目录，只复制缺失文件，不覆盖已有数据。

## 3. 程序架构

```text
pet.py
├── app_paths.py       资源目录与跨平台可写数据目录
├── buddy_ai.py        智谱 GLM、流式聊天、本地记忆、离线回复
├── home_pet.py        小屋宠物状态、2.5D 移动、寻路与睡眠目标
├── home_scene.py      家场景画布、家具装修、导航反馈与宠物渲染
├── scene_system.py    家场景坐标、家具几何与视口计算
├── progression.py     记录、好感、经验、Pet 币、强化、装扮、成就
├── progression_ui.py  记录/成就/装扮/商店窗口
├── minigames.py       小游戏中心与两个小游戏
├── decoration_renderer.py  装扮透明图层定位、裁剪、旋转、绘制
└── updater.py         版本检查、资产选择、下载、替换与清理
```

### `pet.py`：主应用与交互层

- 初始化 Qt、DPI、单实例服务、托盘图标和主宠物窗口。
- 加载/保存 `pet_state.json` 与 `pet_settings.json`，维护主循环、位置、状态衰减和动作触发。
- 提供 `ChatWindow`、`StatsWindow`、`SettingsWindow`、`TutorialWindow`、`BubbleMenu`、`SpeechBubble`、`FetchPlayScene` 等 UI。
- `PetWindow` 负责透明窗口、动画帧加载、自动行走、拖拽/弹跳、喂食/抚摸/睡觉/接球和主动气泡。
- `TrayApp` 负责 Windows 托盘/macOS 菜单栏入口、更新、设置和退出。

### `progression.py`：纯养成规则层

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

### `buddy_ai.py`：AI 适配层

默认代理通过正式运行依赖 `requests` 连接并解析 SSE；个人智谱请求继续使用轻量 HTTP 适配，不依赖供应商 SDK。主要流程：

```text
用户输入
  → 读取玩家显式选择的 chat_mode、个人 API Key、默认聊天同意状态与 memory.json
  → 构造宠物人格、时间、情绪、用户画像和最近历史
  → 免费模式：Cloudflare Worker 默认文字代理；自己配置：个人智谱 GLM-4.6V
  → UI 逐 token 更新
  → 写入 history、统计 ai_replies
  → 默认额度/服务错误显示中性提示；普通接口错误使用友好 fallback
```

### `progression_ui.py` 与 `minigames.py`：窗口层

两者复用 `CozyProgressWindow` 的暖色主题、固定尺寸和按钮布局。UI 只调用 `progression.py` 的规则函数，保存由主窗口回调完成。

### `decoration_renderer.py`：装扮绘制

负责透明像素裁剪、按宠物边界适配、旋转后的包围盒计算、图层绘制和待机装扮组合。装扮的归一化位置和缩放范围由 `progression.py` 校验，避免非法存档造成 UI 崩溃。

### `updater.py`：更新器

包含版本比较、Release 资产评分、平台/架构选择、GitHub API 失败时页面兜底、下载进度、Windows 解压/原位替换、旧更新目录清理和 macOS 打开更新包等流程。

## 4. 资源与动画

资源位于 `assets/`，构建时由两个 PyInstaller spec 一起打包：

| 目录 | 内容 | 当前规模 |
|---|---|---:|
| `assets/poses` | idle、happy、sad、eat、sleep、drag、close 静态姿势 | 7 PNG |
| `assets/animations` | 连续帧、`manifest.json`、制作源图 | 114 文件（含 sources） |
| `assets/decorations` | 待机透明装扮图层 | 6 PNG |
| `assets/props` | 接球小球等运行时道具 | 1 PNG |
| `assets/scenes/home` | 家背景、家具、小屋宠物待机/移动/睡眠与导航素材 | 家园专用 PNG 素材 |
| `assets/sounds` | bark、bounce、eat、pet、sleep | 5 WAV |
| `assets/icons` | 16 至 1024 像素应用图标 | 8 PNG |

当前动画目录及配置：

| 动作 | 帧数 | FPS | 循环 | 备注 |
|---|---:|---:|---|---|
| `walk` | 8 | 6 | 是 | 底部锚定、可水平翻转 |
| `eat` | 8 | 4 | 是 | 轻微降饱和度/亮度 |
| `pet` | 24 | 8 | 否 | 结束回到 happy |
| `play` | 24 | 24 | 否 | 接球扑跃，结束回到 happy |
| `sleep` | 12 | 2.4 | 是 | 呼吸起伏 |
| `dig_reward` | 30 | 20 | 否 | 挖宝发现动画 |
| `happy` | 资源目录中配置 | 8 | 是 | 待机开心状态 |

动画清单集中在 `assets/animations/manifest.json`。缺少某动作目录时会回退到 `assets/poses/` 对应静态图，因此可以渐进式补充素材。制作约束记录在 `assets/animations/README.md`：透明 PNG、统一画布与脚底基线、从 `000.png` 连续命名、避免文字/边框/地面线。

## 5. 本地数据与隐私

### 数据目录

| 运行方式 | 数据目录 |
|---|---|
| 源码运行 | 项目内 `data/` |
| Windows 冻结版 | `%LOCALAPPDATA%\Petpet` |
| macOS 冻结版 | `~/Library/Application Support/Petpet` |

### 文件说明

- `config.json`：API Key、自动聊天模式、默认聊天同意状态、安装 ID 与公开代理地址。敏感信息只保存在本地。
- `memory.json`：AI 多轮历史、用户画像、宠物名字和主动 nudge 时间。
- `pet_state.json`：宠物属性、位置、等级、经验、好感、Pet 币、记录、成就、装扮、强化和小游戏成绩。
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

测试覆盖 AI 配置与聊天工具、动画颜色、路径迁移、接球、挖宝、小游戏、菜单、教程、抚摸、睡眠、气泡、成长规则、成长 UI、更新器、单实例和 Windows 打包元数据。当前结果：`407 passed`。

### Windows 构建

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_windows.ps1
```

脚本会在 `.build_deps/` 安装构建依赖、生成图标，然后执行 `PyInstaller packaging\Petpet-windows.spec`。产物：`dist/Petpet.exe`。构建中间文件写入 `build/`，产物统一写入 `dist/`。

### macOS 构建

必须在 macOS 或 GitHub macOS Runner 上执行：

```bash
chmod +x scripts/build_macos.sh
./scripts/build_macos.sh
```

脚本先生成 `build/Petpet.icns`，再执行 `PyInstaller packaging/Petpet-mac.spec`，产物为 `dist/Petpet.app`。`.github/workflows/build-macos.yml` 使用 `macos-15-intel` 与 `macos-15` 双矩阵构建，并上传 `Petpet-v*-macOS-intel.zip` / `Petpet-v*-macOS-arm64.zip`。

macOS 当前尚未使用 Apple Developer ID 签名和公证，首次打开可能需要在“系统设置 → 隐私与安全性”中选择“仍要打开”。

## 7. 文件索引

```text
Petpet/
├── pet.py                         主程序、Qt UI、动画、交互、托盘
├── version.py                     唯一版本号
├── app_paths.py                   资源路径、数据路径、迁移
├── buddy_ai.py                    默认代理、GLM、记忆、知识库与离线回复
├── progression.py                 成长经济规则
├── progression_ui.py              记录/成就/商店/装扮 UI
├── home_pet.py                    小屋宠物状态与移动规则
├── home_scene.py                  家场景、装修编辑器与小屋宠物绘制
├── scene_system.py                场景坐标与家具几何
├── minigames.py                   小游戏 UI 与逻辑
├── decoration_renderer.py         装扮图层渲染
├── updater.py                     自动更新
├── config.json.example             安全配置模板
├── cloudflare-worker/             默认免费文字聊天代理、KV 限额与部署说明
├── assets/                        姿势、动画、音效、图标、装扮
├── data/                          本地运行数据（不应提交敏感内容）
├── docs/                          TODO 与各版本发布说明
├── packaging/                     Windows/macOS PyInstaller spec
├── requirements/                  runtime/build 依赖
├── scripts/                       Windows/macOS 构建入口
├── tests/                         自动化测试
├── tools/                         聊天 POC、图标/音效/精灵表工具
└── .github/workflows/             macOS 双架构构建工作流
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

## 9. 已知限制与后续路线

### `docs/TODO.md` 中未完成项目

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
3. 新增动画时更新 `assets/animations/manifest.json`，检查静态 fallback 和打包 spec。
4. 新增 Pet 币收入/消费时调用 `add_coins` 或对应统一结算函数，确保 records 统计完整。
5. 新增装扮时同时登记分类、价格、默认变换参数、资源文件和测试。
6. 提交前运行 `python -m pytest -q`，并确认 Git 状态没有 `data/config.json` 中的真实密钥。
7. 发布 Windows 前运行 `scripts\build_windows.ps1`；发布 macOS 前在两个架构 Runner 各构建一次，并验证 ZIP 内层确实是 `Petpet.app`。

## 10.1 协作与验收约定

- 用户说 `add tweaks` 时，理解为小幅、局部、可控的参数调整，不擅自扩大改动范围。
- 任何参数微调优先加入参数调试器，确保可以实时试验，避免反复对话猜数值。
- 修改桌面程序的功能、交互、窗口行为、动画或视觉样式后，先运行相关测试；改动涉及共享行为时运行完整 `python -m pytest -q`。
- Windows 改动测试通过后，重新构建 `dist\Petpet.exe`，停止旧的工作区 Petpet 进程并启动新构建的**无终端版**，供用户直接验证。不要只停在源码测试通过。
- 涉及聊天窗口、气泡、菜单、商店等视觉改动时，先生成本地渲染或截图检查实际效果；不能仅依据 QSS/代码文本判断。Qt 富文本对圆角等 CSS 支持有限，消息气泡优先使用原生 Qt 组件渲染。
- macOS 验收重点：小狗失去应用焦点后仍保持可见且置顶、Retina 尺寸不应过大、聊天界面文字和背景对比舒适。macOS 专属改动应在真机打包后复测。
- 视觉取向：避免高饱和、大面积的对话文字底框；消息样式优先采用低饱和浅色、深色文字、细边框、留白和实际可呈现的圆角。
- 不回滚用户已有改动；提交前检查 `git status`，避免把运行数据、API key 或个人对话纳入发布。
- 源码调试入口：托盘菜单 → `调试` → `参数调试器`；正式发布版本不显示该入口。

## 11. 相关源码入口

- 主入口：`D:\Agent_project\Petpet\pet.py`
- 养成规则：`D:\Agent_project\Petpet\progression.py`
- AI：`D:\Agent_project\Petpet\buddy_ai.py`
- 更新：`D:\Agent_project\Petpet\updater.py`
- 动画规范：`D:\Agent_project\Petpet\assets\animations\README.md`
- 路线图：`D:\Agent_project\Petpet\docs\TODO.md`
- 历史发布说明：`D:\Agent_project\Petpet\.worktrees\home-scene-system\docs\RELEASE_NOTES_v1.4.0.md`
- 当前发布说明：`D:\Agent_project\Petpet\.worktrees\home-scene-system\docs\RELEASE_NOTES_v1.4.1.md`
- 公开下载（发布完成后）：https://github.com/Gsheen76/Petpet/releases/tag/v1.4.1
- 测试目录：`D:\Agent_project\Petpet\tests`

## 关键概念

- project/petpet、pyqt5、desktop-pet、ai-companion、python

## 关联笔记

- [[开发记录/参数调试器 UI 与运行时反馈设计]]：参数调试器 UI 与运行时反馈设计。
- [[场景系统/家场景装修编辑器交互记录]]：家园与装修交互演进。
- [[场景系统/小屋宠物功能分流与好感成长设计]]：小屋顶部功能、桌面/小屋自主行为、被动好感、红点与气泡互斥设计。
- [[菜单系统/宠物快捷菜单交互记录]]：五入口快捷菜单与互动页。
- [[聊天系统/默认免费聊天代理实施记录]]：无 Key 默认聊天、个人 GLM 路由、额度、隐私和部署状态。
- [[发布系统/Petpet v1.4.0 发布设计]]：四平台完整发布设计。
- [[发布系统/Petpet v1.4.0 发布说明]]：面向用户的更新与升级说明。
- [[发布系统/Petpet v1.4.0 发布实施记录]]：测试、构建、哈希、Actions 与 Release 结果。
- [[发布系统/Petpet v1.4.1 一键发布设计]]：安全、可恢复的一键发布编排。
- [[发布系统/Petpet v1.4.1 发布实施计划]]：v1.4.1 验证、构建与发布步骤。
- [[发布系统/Petpet v1.4.1 发布说明]]：聊天、知识库和暖色界面更新说明。
- [[发布系统/Petpet v1.4.1 发布实施记录]]：最终提交、测试、构建、Actions、资产哈希与公开结果。
- [[笔记/MOC/MOC-项目与实践]]：项目与实践专题入口。
- [[笔记/知识库/知识库索引]]：返回知识库索引。

## 规划

- [ ] 补充或更新本笔记中的结果、限制与下一步工作。

## 2026-08-13 小屋宠物功能分流与好感成长设计

- 小屋右上角调整为属性、商店、互动、装修和退出；互动展开抚摸、喂食、玩耍、睡觉。
- 小屋右键不再打开桌面快捷菜单；桌面停止随机走动，小屋改为 12–25 秒一次的较高频自主移动。
- 新增每分钟 0.60 的被动好感，零属性逐项减半；好感升级需求逐级增长并封顶 200。
- 属性为 0 时，小屋宠物、互动入口及对应恢复按钮显示红点。
- 桌面低属性改用独立冷却的语言提醒；寻宝改为圆形气泡并与普通对话互斥。
- 小游戏与新发现宝藏的 Pet 币基础奖励整体翻倍；对话框三角跟随小狗头顶锚点。

详见 [[场景系统/小屋宠物功能分流与好感成长设计]]。
## 2026-08-12 聊天模式选择更新

- 聊天窗口使用单一模式按钮，提供“免费聊天”和“自己配置 API”两个明确选项。
- 自配模式的模型选择与 Key 输入合并到一个弹窗；当前支持 `GLM-4.6V-Flash` 图文聊天。
- 模式与 Key 分开保存：免费模式不会使用已保存的个人 Key，切换模式也不会删除 Key。
- 默认免费代理使用 OpenRouter `openrouter/free`；系统提示最多 4000 字符，普通消息每条最多 1200 字符，请求总大小最多 16 KiB。

详见 [[聊天模式选择与代理容量设计]] 与 [[默认免费聊天代理实施记录]]。

> [!bug] 免费聊天空响应修复
> OpenRouter 免费路由可能随机选择推理模型。Worker 必须使用 `reasoning.effort=none`，不能沿用智谱的 `thinking.type=disabled`，否则有限输出额度可能全部消耗在推理字段而没有正文。客户端同时保证只发送一份系统提示，避免短历史下重复提示。

> [!bug] Windows 免费聊天连接修复
> 默认代理请求不再使用会在部分 Windows 代理环境中超时的 `urllib`，改用正式运行依赖 `requests` 进行 SSE 流式连接。诊断日志仅保存状态元数据，不保存对话或 Key。

## 2026-08-12 聊天界面视觉规范

- 聊天模式采用常驻的 `免费｜自定义` 分段选择器，替代单个菜单按钮。
- 免费态只保留模式选择与清除记忆；模型、图片和 API 设置仅在自定义态出现。
- 玩家可见提示使用短句，不显示技术异常名或重复配置说明。
- 当前及后续游戏界面默认采用暖色圆角设计：窗口、面板、输入框、气泡和操作按钮均需有一致的圆角层级，不使用蓝色高亮。
- 本轮先落地聊天窗口；其他界面在后续修改时按同一规范维护，不进行无关的全局重写。

详见 [[聊天系统/圆角精简聊天界面设计]]。

> [!success] 圆角聊天界面已落地
> `免费｜自定义` 分段选择、按模式显示工具、发送中锁定切换、24/18/15px 圆角层级与精简提示均已实现。已有个人 Key 时可直接切换自定义，缺少 Key 时才打开配置。聊天 focused tests 为 56 passed，全量测试为 354 passed；当前 worktree 源码版已启动供验收。

## 2026-08-12 聊天头像与角色素材边界

- 聊天左头像使用桌面宠物素材，当前为 `assets/poses/idle.png`；不使用家园小狗模型。
- 桌面宠物与家园宠物按两个可独立发展的角色来源维护，以适配后续多宠物。
- 玩家头像可在聊天窗口右上角本地上传，默认使用暖色人物头像。
- 聊天窗口采用透明顶层与实体圆角内容容器，确保外轮廓四角真正透明。

详见 [[聊天系统/聊天头像与真实圆角窗口设计]]。

> [!success] 聊天头像与真实圆角已实现
> 顶层窗口四角 alpha 已验证为 0；桌面柴犬头像位于左侧，玩家默认/自定义头像位于右侧。右上角可编辑头像，底部按钮为 `上传` 与 `DEL`。聊天 focused tests 为 67 passed，全量测试为 365 passed。

## 2026-08-12 暖色聊天组件规范

- 聊天界面选中态统一使用低饱和淡粉色，辅以奶油黄、杏色和鼠尾草绿。
- 分段按钮固定相同几何与字体属性，状态切换不得引起上下浮动。
- 聊天内确认框、头像选项与 API 配置采用 Petpet 自绘圆角组件，不使用系统蓝色高亮。
- 只有一个个人模型时显示静态模型卡，不显示重复下拉选项。
- 文件选择器仍使用系统原生窗口。

详见 [[聊天系统/暖色圆角聊天组件设计]]。

## 2026-08-13 小屋指令、好感与提醒系统完成

> [!success]
> 小屋与桌面宠物的行为已正式分流，focused tests 为 `251 passed`，全量测试为 `424 passed`。

- 小屋右上角固定为 `属性｜商店｜互动⌄｜装修｜退出`；互动下拉包含抚摸、喂食、玩耍、睡觉，小屋右键菜单已移除。
- 桌面宠物不再自主走动，也不再弹出饥饿/陪玩操作气泡；属性低于 20 时按精力、饱腹、心情优先级语言提醒，各自冷却 10 分钟。
- 小屋宠物空闲时每 12–25 秒自主走动；低精力仍会前往地毯睡觉，玩家移动与互动优先。
- 被动好感为 0.60/分钟，每个零属性乘 0.5；升级需求从 30 起每级增加 10，并在 200 封顶后继续成长。
- 零属性红点覆盖桌面/小屋宠物、互动入口及对应恢复动作；属性面板同时显示 EXP 与好感成长速度。
- 新寻宝奖励和小游戏基础奖励整体翻倍；圆形宝藏提示位于桌面小狗正上方，右键菜单打开时隐藏、关闭后恢复。
- 普通对话与宝藏提示互斥，对话框下方三角会随当前宠物头顶中心移动。

详见 [[场景系统/小屋宠物功能分流与好感成长设计]] 与 [[场景系统/小屋宠物功能分流与好感成长实施计划]]。

## 2026-08-12 设置与教程视觉改版设计

- 设置和教程沿用聊天界面的暖色圆角、透明外壳与清晰像素字体规范。
- 设置页采用单列纵向卡片；健康提醒改为“少 / 适中 / 多”，日常互动和主动陪伴合并为“性格偏好：文静 / 适中 / 活泼”。
- 三档偏好继续写回原有底层字段，以兼容旧存档；默认档位均为“适中”。
- 教程更新为六页，覆盖当前桌面操作、快捷菜单、小屋移动与睡觉、图文聊天和新设置逻辑。

详见 [[设置系统/暖色圆角设置与教程设计]]。

> [!success] 暖色圆角设置与教程已实现
> 设置页已收敛为“界面体验、健康提醒、性格偏好”三张纵向卡片；健康和性格使用三档吸附滑块并兼容旧字段。教程更新为六页且覆盖当前小屋、图文聊天和偏好设置。focused tests 为 71 passed，全量测试为 386 passed。

> [!info] 2026-08-13 设置与教程字号调整
> 设置页默认字号层级放大为 28/23/21/18px，教程标题/正文/按钮调整为 28/21/20px，解决源码界面大面积留白下文字偏小的问题；设置页字号控件仍可等比调整整套层级。

> [!info] 2026-08-13 设置与教程居中调整
> 设置和教程改为居中显示在小狗所在屏幕；设置字号继续放大到 31/25/23/20px，教程缩小为 740×620 并使用 31/23/22px 标题、正文与按钮。

> [!bug] 教程命名页排版修复
> 精简命名说明并压缩正文与名字卡高度，修复 740×620 教程窗口中长文案被输入框覆盖的问题；新增控件几何不重叠测试。

> [!success] 暖色聊天组件已实现
> 分段选择固定几何并使用淡粉选中态；清除确认、头像菜单和 API 配置均替换为 Petpet 自绘圆角组件。单模型使用静态杏色模型卡。聊天 focused tests 为 72 passed，全量测试为 370 passed。

## 2026-08-13 v1.4.1 正式发布

- `v1.4.1` 已公开，范围包含默认免费聊天代理、个人 GLM-4.6V 图文聊天、游戏知识库、聊天头像与暖色圆角 UI、三档设置和六页教程。
- 新增 `.\scripts\release.ps1 -Version 1.4.1`：本机构建 Windows，GitHub Actions 构建 macOS Intel/arm64，四项资产完整后才公开 Release。
- 发布脚本禁止强推和破坏性 Git 操作；失败时保留草稿并支持同一命令恢复。
- 默认聊天 Worker 已改用 SQLite Durable Object 原子统计安装 ID 与 IP 的每日额度，
  通过 alarm 在次日清理历史哈希计数；部署版本 ID 为
  `834a33fd-35e0-4029-963b-58d955c8ef15`，线上无私人内容冒烟返回 `200 text/event-stream`。

详见 [[发布系统/Petpet v1.4.1 一键发布设计]]、[[发布系统/Petpet v1.4.1 发布实施计划]] 与 [[发布系统/Petpet v1.4.1 发布说明]]。

最终结果见 [[发布系统/Petpet v1.4.1 发布实施记录]]。

## 2026-08-12 聊天字体与 API 提醒修正

- 聊天分段按钮按中文标签实际字宽定宽，消除“免费 / 自定义”重叠，同时保持切换时几何固定。
- 聊天弹窗、头像菜单和底栏控件统一使用 DPI 无关像素字体；标题 21px、正文 18px、按钮 17px、辅助文字 15px，主要控件实际高度统一为 40px。
- 未配置 API Key 的红点显示在桌面小狗本体、主菜单“聊天”和聊天页“自定义”，不再显示在“设置”。首次打开自定义配置后保存空配置的已读标记，之后不重复提醒。
- 本轮 focused tests 为 126 passed，全量测试为 376 passed。

详见 [[聊天系统/暖色圆角聊天组件设计]]。
