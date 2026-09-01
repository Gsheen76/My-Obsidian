# AGENTS.md — Petpet 代理工作约定

桌面宠物 PyQt5 应用（Windows 单实例托盘常驻 + macOS arm64）。
交接级细节（各版本改动、待办）见 `HANDOFF.md`；本文件是**长期有效的编码与资源约定**，两者冲突时以本文件为准。

## ⚡ 核心要点（最高优先级）：Obsidian 实时记录

**每一次对话中的开发活动，无论大小，都必须同步记录到 Obsidian 档案库**：`D:\Github Desktop\My-Obsidian\项目\Petpet\`

- **每次修改**：在 `开发记录\` 追加当日/当主题的记录块（日期、改了什么、为什么改、如何验证）
- **每次规划**：新功能设想、方案拷问结论、设计决策 → 记入开发记录或总档案对应章节
- **遇到的问题**：bug 现象、排查过程、根因、修复方式 → 单独记条目，便于日后回查
- **总文档**：`Petpet 总档案.md` 必须实时更新（当前公开版本、当前开发状态、版本演进表、关联链接），禁止等批量补记
- 发版类内容另入 `发布系统\`

这不是收尾时的可选动作，而是与代码修改同节奏的**强制动作**：改完 → 验证 → 记录，一轮才算完成。用户将 Obsidian 视为项目的唯一权威记忆（HANDOFF.md 的完成门亦指向它）。

## ⚡ 文档同步规则（强制）

开发过程中**每引入一条新规则、新约定或新坑位**，必须**即时**同步到以下两个文件（不等批量补记）：

1. **`HANDOFF.md`**：当前版本号、最近变更表、坑位表、待办清单——保证新对话读到的是最新状态
2. **`AGENTS.md`**：新规则如果属于长期有效的编码/资源/UI/验证约定，写入对应章节

这两份文件修改后须**同步上传到 Obsidian** 档案库对应路径（HANDOFF.md → `工程结构\`，AGENTS.md → `工程结构\`），保持"仓库 ↔ Obsidian"双端一致。

## 视觉风格（已锁定，改动前必读）

项目的视觉语言已经过用户多轮调校并**锁定**，做任何 UI 改动必须沿用，不得引入新的设计方向：

- **主题**：温暖奶油/珊瑚系 —— 底色 `#fff9ee`，珊瑚主色 `#f28f76`；圆角、胶囊形（pill）控件；面板内容居中布局
- **字体**：全局幼圆，统一走 `petpet/app/fonts.py`；聊天字号预设 20/24/28；家园交互气泡 19px；聊天头像 60px
- **布局**：主视口宽 700；设置面板开关不得改变聊天窗口大小；纯文字记录区用透明背景叠在公共爪印背景图上
- **阴影规范（用户定稿，勿再调）**：所有宠物 idle 用原始扁平椭圆（alpha 42）；仅 ice_cream 走路时用斜阴影（alpha 55、接触长 0.52、foot_y 0.90/0.98；左下&右上 → 右斜 +16°，左上&右下 → 左斜 −16°，按 dx/dy 符号分支实现，**绝不绑定 sprite-mirror 变量**）；lunch_meat 全场景保持扁平椭圆。地面粉色椭圆+箭头是点击目标标记，不是阴影
- **宠物朝向**：按宠物 ID 固定（registry `facing` 字段），走路不左右翻转
- **角色约束**：聊天小狗**永远不说「汪…」类口癖**，回复清洗掉开头吠叫模式
- 用户反馈「太高/太大/怪怪的」时，以实测数据（px 差值、色彩统计）为准做微调轮；反馈「反了」时禁止翻符号猜——从精灵 alpha 通道质心实测推导方向

## 技术栈

- Python 3 + PyQt5（`requirements/runtime.txt`）；图像处理用 Pillow/numpy
- 打包：PyInstaller（`scripts/build_windows.ps1` / `build_macos.sh`），发布一键走 `scripts/release.ps1 -Version X.Y.Z`
- 云端：聊天中转在 `cloudflare-worker/` 与 `aliyun-chat/`（Node，独立部署，与 Python 主程序无共享代码）
- 测试：pytest，`tests/conftest.py` 会把 `LOCALAPPDATA` 指到临时目录，**禁止**在测试中读写玩家真实数据目录

## 架构边界（改代码前先确认归属）

| 归属 | 模块 | 说明 |
|---|---|---|
| 入口/托盘 | `pet.py` | 单实例、系统托盘、主窗口装配 |
| 桌面宠物渲染与交互 | `petpet/app/pet_window.py` | 动画播放、资产切换、拖拽/点击 |
| 状态持久化 | `petpet/app/state.py`、`app/paths.py` | 所有可写数据走 `app/paths.py` 的路径常量，**不许硬编码用户目录** |
| 养成/商店/货币逻辑 | `petpet/progression/core.py` | 纯逻辑，UI 无关，可 TDD |
| 养成/商店面板 | `petpet/progression/ui.py` | 核心视觉层 |
| 家园场景 | `petpet/home/`、`home_scene.py`、`home_pet.py` | 根目录同名文件多为 `petpet/home/` 的兼容 facade，新代码 import 包内模块 |
| 聊天 | `petpet/chat/` | `api.py`（上游调用）、`service.py`（编排）、`memory.py`（记忆）；key 只从 `config.json` 读 |
| 通用 UI 控件 | `petpet/ui/common.py`、`controls.py` | 新控件先看这里能否复用 |

## 资源约定（assets/runtime/）

- 宠物按 ID 组织：`pets/<pet_id>/desktop/{poses,animations,outfits}` 与 `pets/<pet_id>/home/…`
- 每套动画由 `animations/manifest.json` 声明：`folder`、`fps`、`loop`、`fallback`、可选 `frame_sequence` 与 `frame_durations_ms`（逐帧毫秒数允许非均匀）
- 姿势静态图在 `poses/<动作>.png`；**所有帧与姿势必须同尺寸、宠物主体大小一致**，脚底阴影对齐（历史 bug 多源于此）
- 资产加载必须有失败回退：损坏或缺失的单个资源不得拖慢绘制或崩溃（见 README v1.6.1 约定）
- 新增宠物需同步更新 `pets/manifest.json`（id、默认名、性格、价格/折扣、preview、avatar、desktop/home 入口）

## UI 约定

- 全局字体走 `petpet/app/fonts.py`，不要在面板里散落 `setFont(new QFont(...))`
- 视口/窗口尺寸调整需同时检查：设置面板开关不应改变聊天窗口大小（历史修复），主视口宽 700
- 交互动画（摸头/喂食/玩耍/挖宝/睡觉）统一缩放到与 idle 主体一致
- 家园窗口**不置顶**（允许被其他窗口遮挡）；气泡按钮 hover 有描边、按下有染色，且在按钮内松开才触发

## 代码风格

- 类型注解与 `from __future__ import annotations` 跟随所在文件既有风格；公共函数保留中文 docstring 习惯
- 兼容 facade（根目录薄包装模块）保持 3–10 行，不添加新逻辑
- 聊天回复清洗、口癖类规则集中在 `petpet/chat/`，不要散落在 UI 层

## 验证流程

1. `pytest`（tests/ 覆盖状态机、聊天、UI 边界；offscreen 可跑，Windows 平台模式见 conftest）
2. 涉及资源/动画的改动：确认 manifest.json 与文件实际帧数一致，跑一次程序目检 idle 帧循环
3. 发版：更新 `version.py` 与 `docs/RELEASE_NOTES_vX.Y.Z.md`，走 `scripts/release.ps1`

## 明确不做

- 不引入 GUI 框架之外的重量级依赖（保持 runtime 三件套：PyQt5/requests/Pillow）
- 不在 `cloudflare-worker`/`aliyun-chat` 中存放任何密钥；`config.json.example` 是唯一密钥模板
- 不动 `data/` 下玩家真实存档（测试环境除外）
