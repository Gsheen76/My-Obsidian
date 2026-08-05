---
title: Petpet 项目总档案
type: project
status: active
version: v1.3.1
platforms: Windows 10/11, macOS Intel, macOS Apple Silicon
source: D:\Agent_project\Petpet
updated: 2026-08-05
tags:
  - project/petpet
  - PyQt5
  - desktop-pet
  - ai-companion
  - Python
summary: 记录项目的定位、实现结构、当前状态和后续工作。
migrated: 2026-08-05
---

# Petpet 项目总档案

> [!summary] Summary
> Petpet 是一个运行在桌面上的治愈系陪伴小狗：它有透明置顶窗口、拖拽和物理弹跳、连续帧动画、喂食/抚摸/玩耍/睡觉等互动、成长与 Pet 币经济、装扮商店、小游戏、健康提醒、托盘入口、离线回复，以及可选的智谱 GLM 多轮流式聊天。

## 1. 项目定位与当前状态

- **当前版本**：`v1.3.1`，版本唯一来源是 `version.py` 中的 `VERSION = "1.3.1"`。
- **当前分支/提交**：`main`，HEAD 为 `b5ddc9c`（`docs: finalize v1.3.1 macOS downloads`）。
- **最近发布标签**：`v1.3.1`；历史版本从 `v1.0.0`、`v1.1.0`、`v1.1.1`、`v1.2.0` 至 `v1.3.1` 均已打标签。
- **运行平台**：Windows 10/11、macOS Intel、macOS Apple Silicon。
- **技术栈**：Python 3.11、PyQt5、Pillow、NumPy；发布版使用 PyInstaller。
- **测试状态**：运行 `python -m pytest -q`，结果为 **149 passed in 4.59s**。
- **源码位置**：`D:\Agent_project\Petpet`。
- **本笔记位置**：`D:\Github Desktop\My-Obsidian\项目\Petpet\Pet.md`。

项目是一个本地优先的单用户桌面应用。除 AI 聊天请求外，养成、动画、装扮、小游戏、设置和数据迁移均可离线完成。发布包不打开命令行窗口，并通过 Windows 托盘或 macOS 菜单栏入口控制显示、设置、更新和退出。

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

### AI 聊天

- 供应商：智谱开放平台；接口为 `https://open.bigmodel.cn/api/paas/v4/chat/completions`。
- 默认模型：`glm-4-flash`（界面名称 `GLM-4-Flash`）。
- 支持流式输出、最近多轮历史、轻量 `user_profile`、宠物名字同步、时间问候、关键词情绪识别和主动 nudge。
- API Key 优先级：环境变量 `ZHIPU_API_KEY` > 本地 `config.json`。
- API Key 缺失、网络失败或接口异常时，自动使用规则型离线回复，不影响其他功能。
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

通过标准库 `urllib` 发起请求并解析 SSE 流，不强依赖第三方 SDK。主要流程：

```text
用户输入
  → 读取 API Key / 模型 / memory.json
  → 构造宠物人格、时间、情绪、用户画像和最近历史
  → 智谱流式 SSE
  → UI 逐 token 更新
  → 写入 history、统计 ai_replies
  → 失败时 fallback_reply
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

- `config.json`：API Key 与模型。敏感信息只保存在本地。
- `memory.json`：AI 多轮历史、用户画像、宠物名字和主动 nudge 时间。
- `pet_state.json`：宠物属性、位置、等级、经验、好感、Pet 币、记录、成就、装扮、强化和小游戏成绩。
- `pet_settings.json`：窗口尺寸、字体、置顶、更新检查、健康提醒、音效、衰减速度和主动聊天频率。

当前示例存档已经包含完整 v1.3.1 字段，例如 `pending_dig_reward`、`last_dig_discovery_at`、`affection_last_gains`、`decoration_adjustments`、`minigame_best_scores`；不要把真实用户存档或真实 API Key 提交到仓库。

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
python -m pytest -q
```

测试覆盖 AI 配置与聊天工具、动画颜色、路径迁移、接球、挖宝、小游戏、菜单、教程、抚摸、睡眠、气泡、成长规则、成长 UI、更新器、单实例和 Windows 打包元数据。当前结果：`149 passed`。

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
├── buddy_ai.py                    GLM、记忆、离线回复
├── progression.py                 成长经济规则
├── progression_ui.py              记录/成就/商店/装扮 UI
├── minigames.py                   小游戏 UI 与逻辑
├── decoration_renderer.py         装扮图层渲染
├── updater.py                     自动更新
├── config.json.example             安全配置模板
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

- 修改桌面程序的功能、交互、窗口行为、动画或视觉样式后，先运行相关测试；改动涉及共享行为时运行完整 `python -m pytest -q`。
- Windows 改动测试通过后，重新构建 `dist\Petpet.exe`，停止旧的工作区 Petpet 进程并启动新构建的**无终端版**，供用户直接验证。不要只停在源码测试通过。
- 涉及聊天窗口、气泡、菜单、商店等视觉改动时，先生成本地渲染或截图检查实际效果；不能仅依据 QSS/代码文本判断。Qt 富文本对圆角等 CSS 支持有限，消息气泡优先使用原生 Qt 组件渲染。
- macOS 验收重点：小狗失去应用焦点后仍保持可见且置顶、Retina 尺寸不应过大、聊天界面文字和背景对比舒适。macOS 专属改动应在真机打包后复测。
- 视觉取向：避免高饱和、大面积的对话文字底框；消息样式优先采用低饱和浅色、深色文字、细边框、留白和实际可呈现的圆角。

## 11. 相关源码入口

- 主入口：`D:\Agent_project\Petpet\pet.py`
- 养成规则：`D:\Agent_project\Petpet\progression.py`
- AI：`D:\Agent_project\Petpet\buddy_ai.py`
- 更新：`D:\Agent_project\Petpet\updater.py`
- 动画规范：`D:\Agent_project\Petpet\assets\animations\README.md`
- 路线图：`D:\Agent_project\Petpet\docs\TODO.md`
- 发布说明：`D:\Agent_project\Petpet\docs\RELEASE_NOTES_v1.3.1.md`
- 测试目录：`D:\Agent_project\Petpet\tests`

## 关键概念

- project/petpet、pyqt5、desktop-pet、ai-companion、python

## 关联笔记

- [[笔记/知识库/知识库索引]]

## 规划

- [ ] 补充或更新本笔记中的结果、限制与下一步工作。
