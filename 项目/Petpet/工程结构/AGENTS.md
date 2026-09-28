# AGENTS.md — Petpet 代理工作约定

桌面宠物 PyQt5 应用（Windows 单实例托盘常驻 + macOS arm64）。
交接级细节（各版本改动、待办）见 `HANDOFF.md`；本文件是**长期有效的编码与资源约定**，两者冲突时以本文件为准。

## ⚡ 核心要点（最高优先级）：Obsidian 实时记录

**每一次对话中的开发活动，无论大小，都必须同步记录到 Obsidian 档案库**：`D:\Github Desktop\My-Obsidian\项目\Petpet\`

**写到哪个目录、文件怎么命名、各类内容怎么写，一律先读档案库根目录的《文档规范.md》并遵照执行**（`D:\Github Desktop\My-Obsidian\项目\Petpet\文档规范.md`），本文件只保留强制时机。速记：

- 单轮修复/调整/迭代日志 → `开发记录\`，命名 `YYYY-MM-DD 主题.md`
- 方案/设计/实施 → 对应系统目录（场景/宠物/聊天/菜单/设置/工程结构），后缀限 `设计 / 实施计划 / 实施记录 / 交互记录`
- 发布与更新链路 → `发布系统\`（`Petpet vX.Y.Z 发布说明/发布设计/发布实施计划/发布实施记录`）
- `Petpet 总档案.md` 只放项目级总览（状态行、功能总览、架构、版本演进表、目录索引），**禁止当日志堆**；状态变了只刷新总档案的状态行
- 档案维护动作（改名/移动/拆分）本身记入 `开发记录\`，且必须先全库 grep 修复反向链接

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
- **角色约束**：聊天小狗**永远不说「汪…」类口癖**，回复清洗掉开头吠叫模式；**回复一律单段不换行**（用户定稿 2026-09-12）——`clean_assistant_reply` 合并所有换行（非 ASCII 边界直接相连，两侧均 ASCII 补一个空格），不要在任何下游重新引入 `\n`
- **聊天头像裁剪按宠物**（用户定稿 2026-09-12）：大头照（`_assistant_head_rect` 头部方裁）**只属于 `PET_HEADSHOT_AVATARS`（现仅 ice_cream）**；午餐肉等竖版整身宠物沿用「顶部 68% 整身裁 + 近方形图居中方裁」原版（用户：「原来的已经很好了，不要改了」），整身裁**顶不留让位**（耳尖必须完整落在圆框内，有几何测试钉住），新增宠物默认走原裁、勿并入大头照
- **主动搭话/提醒规则**（2026-09-12）：生日/纪念日提醒只认「`生日|纪念日|周年` 关键词 + 公历 `N月N日`」**同时出现**的「重要的事」条目（保守防误触发），当日只发一条；节日只收 `SOLAR_FESTIVALS` 公历固定日——**不做农历换算**（算错日子比没有更糟）；季节话术按月份混池不置顶，节日行才置顶
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
| 宠物详情面板 | `petpet/ui/pet_profile.py` | 快照纯函数 + PetProfileWindow；xp 升级曲线在 `progression/core.py`，勿再复制公式 |
| 家园场景 | `petpet/home/`、`home_scene.py`、`home_pet.py` | 根目录同名文件多为 `petpet/home/` 的兼容 facade，新代码 import 包内模块 |
| 聊天 | `petpet/chat/` | `api.py`（上游调用）、`service.py`（编排）、`memory.py`（记忆）；key 只从 `config.json` 读 |
| 通用 UI 控件 | `petpet/ui/common.py`、`controls.py` | 新控件先看这里能否复用 |

## 资源管理规范（assets/，2026-09-04 素材治理轮定稿）

**目录分工**：`assets/runtime/` 是唯一随程序打包的运行时素材根（打包 spec 只带它）；`assets/source/` 是开发期归档（AI 稿/参考图/精灵表中间稿），不打包、可自由命名。参考图、弃用稿**绝不留在 runtime**——归档进 `assets/source/references/`。

**命名规范（强制）**：runtime 文件名纯 ASCII、snake_case `^[a-z0-9_]+\.(png|wav|json)$`；例外：动画帧 `NNN.png`、应用图标 `icon-N.png`。禁止中文、大写、连字符。

**守卫测试**：`tests/test_asset_inventory.py` 四条规则，新增/改动素材必须过——① runtime 每个文件可被引用链命中（代码/manifest/spec/脚本文本，或为 manifest 声明目录下的帧文件）；② 命名符合上述规范；③ 动画帧目录必须被 manifest `folder` 字段声明（无幽灵文件夹）；④ 主代码禁止盘符绝对路径引用 assets。

**其余既有约定**：

- **素材导入默认不校色**（两次用户定稿：恐龙拖拽 2026-08-31、原皮抓起 2026-09-22，均判校色版「暗淡/偏色」而选原色）——精灵图按源图原色导入；配平 idle 之类的校色只走显式 opt-in 参数（如 `import_lunch_meat_grab.py` 的 `--sat/--val/--green`），不设默认增益
- 宠物按 ID 组织：`pets/<pet_id>/desktop/{poses,animations,outfits}` 与 `pets/<pet_id>/home/…`
- 每套动画由 `animations/manifest.json` 声明：`folder`、`fps`、`loop`、`fallback`、可选 `frame_sequence` 与 `frame_durations_ms`（逐帧毫秒数允许非均匀）；`fallback` 指向**静态姿势名**（非动画键），文件夹缺失时加载器跳过并落回姿势，允许预声明尚不存在的文件夹
- 姿势静态图在 `poses/<动作>.png`；**所有帧与姿势必须同尺寸、宠物主体大小一致**，脚底阴影对齐（历史 bug 多源于此）
- 资产加载必须有失败回退：损坏或缺失的单个资源不得拖慢绘制或崩溃（见 README v1.6.1 约定）
- **贴图加载一律预缩到显示预算（2026-09-12 定稿，勿存源分辨率）**：姿势/套装预览走 `_shrink_to_display_budget`（2×max(PET_W,DOG_H)×DPR），动画帧在 `ANIMATION_MAX_SIZE=384` 绝对护栏后再缩到 `_animation_display_budget_px()`（1.5×显示）——绘制目标恒为 190×160 窗口，全分辨率常驻曾是 +124MB/+77MB 的两个大头；预缩纯加载期动作，不往每帧绘制加活
- 新增宠物需同步更新 `pets/manifest.json`（id、默认名、性格、价格/折扣、preview、avatar、desktop/home 入口）
- 动画制作/拆帧流程见 `assets/source/spritesheets/README.md`（v2）；`tools/build_fetch_animation.py`、`build_petting_animation.py` 为旧目录结构时代的遗留脚本，重跑前需重指路径

## UI 约定

### 按键交互规范（2026-09-28 用户定稿：纯缩放反馈，全应用统一，无例外）

所有可交互按键（面板/商店/家园/弹窗/贴图键/QSS 键）的反馈**只有缩放**，不得加任何描边/白洗/高亮叠层：

1. **悬浮**：按键**放大**（约 +2px/边，家园自绘键 ±3px）。
2. **点击/按住**：**还原原大小**——按压内缩与压暗已按用户 2026-09-28 终版定稿**全部删除**（「最简单的逻辑：悬浮放大，点击还原大小」）。
3. **松开**：在键内 → **点击音瞬间即响**、0ms（下一事件拍）即**触发动作**；拖出键外 → 取消不触发。
4. **可选中按键**（页签/筛选等 checkable）：反馈视觉相同，但保留原生释放时序——拦截 release 会跳过 `nextCheckState` 破坏选中切换。
5. **未选中的可切换按键**：不得过度透明（透明度 ≥0.65），保持可辨识。
6. **分栏/页签类 checkable 键用 `setFlatFeedback(True)` 轻反馈**（2026-09-28 用户定稿：栏目只要悬浮颜色变化——整帧缩放会把文字压扁，放大也不要）。实现要点：**视觉反馈依赖的预渲染帧缓存（如 `FeedbackButton._capture_skin` 的 render 抓帧）必须在 `showEvent` 时机预建**——懒抓会让每个键首次悬浮/按压的第一帧走素颜（无反馈、迟一拍，2026-09-28 手感延迟轮根因）；贴图自绘键按各自余量机制绘制（`_AvatarButton` 常态内缩 2px、悬浮放大到全幅；`_ArtButton`/`_TabButton` 靠 margin/headroom/side_margin 余量）——绘制永远在 widget 边界内（KeepAspectRatio 限制维度会翻转，余量按最坏轴预留）；QSS 全铺满皮肤的按键用 `render` 抓素颜帧整体缩放（`FeedbackButton`），几何余量为零不能直接放大矩形。
7. **守卫**：`tests/test_button_feedback_pure_scale.py` 钉死 hover 帧 == 素颜帧整体放大（无叠层像素）。

> **气泡菜单例外（2026-09-28 晚用户定稿：「右键菜单栏的那些效果还是保持之前的效果，我喜欢之前那样的交互方式」）**：BubbleMenu 的悬浮光环（白洗 `242,143,118,34` + 珊瑚描边 `#f28f76` 2.2px，画在整格内无裁角）保留旧效果，纯缩放规范不适用于气泡菜单——`test_button_feedback_pure_scale.py` 反向钉死光环必须存在。
> **四角锁定特效根因存档（勿重蹈）**：2026-09-09 版规范曾定「悬浮=放大+白洗+珊瑚描边」，`FeedbackButton` 把描边画在 `rect±2` 的圆角矩形上——控件边界把描边直线段全部裁掉、只剩四角的弧段，视觉即「取景框角标/四角锁定特效」，被用户连拍 6 张截图否决。教训：① 任何叠层只能画在 widget 边界**内**；② 悬浮描边/白洗类效果已被用户明确废弃，禁止复活（同轮根除的还有家园 `_draw_scene_button`/图片键/分类签/放置键、宠物面板 `_TabButton`/`_AvatarButton` 的同类叠层）。
> 统一点击音（2026-09-28 三轮定稿：**所有按键都要响，包括分栏页签**——checkable 不响的旧豁免已废除）：`petpet/app/sounds.py` 两层结构——显式调用层（FeedbackButton 松开/家园键/贴图键/头像/气泡菜单）+ `install_click_sound_filter`（pet.py main 安装的**应用级过滤器**，兜住 QAbstractButton 全家/QTabBar/设 PointingHandCursor 的自绘键，键内左键松开即响）；`play_click` 带 25ms 节流防双层命中双响，跟随设置项 `sound_enabled`。`RESOURCE_DIR` 是 str，用 `/` 拼 TypeError 会被静默吞掉，坑位见 HANDOFF。**音效预热一律放启动期**（pet.py main 拿单实例锁后 + PetWindow 构造尾部）：QSoundEffect 的 play 有设备接入同步段（进程首个 ~1s+每实例 ~200ms），任何「启动后延时预热」都会把冻结压到用户操作窗口上（2026-09-28 卡顿轮，曾致切分栏冻 5s）；play() 自带 restart 语义，勿加 stop()（每次同步 ~240ms）。**点击音=QSoundEffect 单实例+节流 40ms>音效时长**（播放中再 play()=restart 有 ~300ms 同步段——节流大于音长是单实例永不撞 restart 的结构性保证，音效时长改动必须同步评估节流值；多实例在本机 WASAPI 每次 play ~500ms 勿用；winsound 的 waveOut 出声缓冲有耳朵延迟勿用）。**静音路径一律 volume=0 且不在播放中解除**（mute 即时属性，播放中解除必漏声；音量只在真实播放前设）。

- **无父顶层原生窗必须继承 `petpet/ui/common.KeepAliveTopLevelWindow`**（2026-09-24 家族根治）：任何设 `Qt.Tool` 标志的顶层 QWidget 子类（气泡/菜单/浮窗/面板壳）构造即入类级保活表、`closeEvent` **延迟出表**（`CLOSE_GRACE_MS=2500` 缓冲后在途窗口消息排空才 discard——2026-09-28 15:56 第六案：当场出表会让最后引用在嵌套事件投递中同步析构 C++ 对象，qwindows→notify×3→AV 读 -1）——杜绝「弃引用→GC 连 C++ 销毁→在途窗口事件投递已释放接收者」的 AV 闪退家族；`tests/test_parentless_window_guard.py` 静态扫描全库强制，**零豁免**。短命浮窗在各自 `closeEvent` 里先停自身定时器再 `super()`（基类刻意不停表，防误杀关后复用面板的实例定时器）
- 桌面浮窗**预热一律不 `show` 停靠屏外**：用 `grab()` 强制完整 paintEvent 即可——常驻显示的停靠窗在 125% 缩放屏首次移入会被 WM 按 100/125 钳到 517/620（事后重申尺寸无效），未显示窗口首开直接按目标几何创建无此患
- **面板尺寸统一 850×960**（2026-09-28 用户定稿「打开的页面要统一大小」）：所有 CozyProgressWindow 子类偏好尺寸、聊天窗 fixedSize、宠物详情 UNIFIED 常量一律 850×960；`tests/test_panel_size_uniform.py` 静态扫描强制，新面板别用别的尺寸
- 全局字体走 `petpet/app/fonts.py`，不要在面板里散落 `setFont(new QFont(...))`
- 视口/窗口尺寸调整需同时检查：设置面板开关不应改变聊天窗口大小（历史修复），主视口宽 700
- 交互动画（摸头/喂食/玩耍/挖宝/睡觉）统一缩放到与 idle 主体一致
- 家园窗口**置顶**（`WindowStaysOnTopHint`，2026-09-10 用户定稿恢复）；装修模式切**全景**：窗口临时加宽为 左栏 338 + 整幅世界 1800（`decoration_scene_window_geometry`），画布 1:1 铺满世界、镜头归零，**不再有左右平移**（pan 链路已整体移除）；家园胶囊键遵循上述按键交互规范（`_button_state` 的 pressed/recover/hover 相态；松开键内回弹 8ms 后触发（点击音在松开瞬间即响）），常量 `HomeSceneWindow.BUTTON_PRESS_FLASH_MS=8`（2026-09-28 三轮 40→15→8ms，回弹与触发延迟）

## 代码风格

- 类型注解与 `from __future__ import annotations` 跟随所在文件既有风格；公共函数保留中文 docstring 习惯
- 兼容 facade（根目录薄包装模块）保持 3–10 行，不添加新逻辑
- 聊天回复清洗、口癖类规则集中在 `petpet/chat/`，不要散落在 UI 层

## 验证流程

1. `pytest`（tests/ 覆盖状态机、聊天、UI 边界；offscreen 可跑，Windows 平台模式见 conftest）
2. 涉及资源/动画的改动：确认 manifest.json 与文件实际帧数一致，跑一次程序目检 idle 帧循环
3. 发版：更新 `version.py` 与 `docs/RELEASE_NOTES_vX.Y.Z.md`，走 `scripts/release.ps1`

## 明确不做

- 不引入 GUI 框架之外的重量级依赖（runtime 四件套：PyQt5/requests/Pillow/numpy——Pillow 与 numpy 在 `petpet/home`、`ui/pet_profile`、`progression/ui` 运行时使用，`requirements/runtime.txt` 必须与实际 import 一致）
- 不在 `cloudflare-worker`/`aliyun-chat` 中存放任何密钥；`config.json.example` 是唯一密钥模板
- 不动 `data/` 下玩家真实存档（测试环境除外）
