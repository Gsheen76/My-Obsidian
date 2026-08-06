---
title: 聊天界面与 API Key 配置提示实现计划
type: project
tags:
  - Petpet
  - 开发记录
  - 聊天
  - API Key
status: completed
source: D:\Agent_project\Petpet
updated: 2026-08-06
---

# 聊天界面与 API Key 配置提示实现计划

> **For agentic workers:** 按任务顺序执行，使用测试优先；当前源码仓库存在用户未提交改动，未经用户明确要求不得提交或回退。

**Goal:** 让聊天中小狗消息更清晰，聊天字体由统一设置控制，并在 API Key 未配置时在聊天与主菜单设置入口显示同步红点。

**Architecture:** `ai.get_api_key_source()` 继续作为唯一配置状态来源。`ChatWindow` 负责将该状态映射为工具按钮文本、红点和统一字体样式；`BubbleMenu` 在绘制设置按钮时查询同一状态并复用已有成就红点绘制方式。

**Tech Stack:** Python 3、PyQt5、unittest、pytest。

## Global Constraints

- 不修改 API Key 存储格式、环境变量优先级、模型配置或聊天接口。
- 聊天消息、输入框和工具按钮都使用 `chat_font_size` 作为字体大小的唯一设置来源。
- 未配置仅提示，不阻止本地话术聊天，也不自动弹出配置窗口。
- Markdown 记录写入 `D:\Github Desktop\My-Obsidian\项目\Petpet\开发记录`。

---

### Task 1: 聊天字体和 API Key 未配置状态测试

**Files:**

- Modify: `D:\Agent_project\Petpet\tests\test_chat_tools.py`
- Modify: `D:\Agent_project\Petpet\tests\test_settings_ui.py`

**Interfaces:**

- Consumes: `ChatWindow._refresh_ai_tool_buttons()`, `ChatWindow._set_log_messages()`, `PetWindow.apply_runtime_settings(previous)`。
- Produces: 对未配置状态、聊天消息字体和运行时设置刷新的回归覆盖。

- [ ] **Step 1: 写入失败测试，固定未配置 API Key 的聊天入口状态。**

```python
def test_missing_key_uses_unconfigured_text_and_badge(self):
    self.window._refresh_ai_tool_buttons()

    self.assertIn("未配置", self.window.api_key_btn.text())
    self.assertTrue(self.window.api_key_btn.property("needsApiKey"))
```

- [ ] **Step 2: 写入失败测试，固定聊天消息字体跟随 `chat_font_size`。**

```python
def test_message_font_tracks_chat_font_setting(self):
    self.window.pet.settings["chat_font_size"] = 24
    self.window.s = self.window.pet.settings
    self.window._apply_style()
    self.window._set_log_messages([("assistant", "测试消息")])

    message = self.window.findChild(QLabel, "chatMessage")
    self.assertEqual(message.font().pixelSize(), pet.independent_font_px(24))
```

- [ ] **Step 3: 运行测试，确认现有实现失败。**

Run: `$env:QT_QPA_PLATFORM='offscreen'; python -m pytest -q tests/test_chat_tools.py`

Expected: 未配置文案仍为“添加 API Key”；消息字体仍为固定值或不随设置更新。

### Task 2: 实现聊天视觉层级、统一字体和 API Key 徽标

**Files:**

- Modify: `D:\Agent_project\Petpet\pet.py:ChatWindow`
- Test: `D:\Agent_project\Petpet\tests\test_chat_tools.py`

**Interfaces:**

- Consumes: `ai.get_api_key_source() -> str | None`、`independent_font_px(size) -> int`。
- Produces: `ChatWindow._chat_font_px() -> int`、`ChatWindow._set_api_key_badge(visible: bool) -> None` 和 CSS 属性 `needsApiKey`。

- [ ] **Step 1: 将聊天正文的字体计算收敛为单一 helper。**

```python
def _chat_font_px(self):
    return independent_font_px(self.s["chat_font_size"])
```

`_apply_style()`、消息 `QLabel`、输入框和工具按钮均使用该 helper；消息气泡不再硬编码 `16px`。

- [ ] **Step 2: 用子 `QLabel` 实现聊天 API Key 按钮右上角红点。**

```python
def _set_api_key_badge(self, visible):
    self.api_key_badge.setVisible(visible)
    self.api_key_btn.setProperty("needsApiKey", bool(visible))
    self.api_key_btn.style().unpolish(self.api_key_btn)
    self.api_key_btn.style().polish(self.api_key_btn)
```

在创建 `api_key_btn` 后创建 `api_key_badge`，固定直径并在 `resizeEvent()` 或工具栏布局完成后定位到按钮右上角；仅当 `get_api_key_source()` 返回空值时显示。

- [ ] **Step 3: 调整机器人消息气泡样式与消息字体。**

```python
bubble.setFont(QFont("Microsoft YaHei", self._chat_font_px()))
bubble.setStyleSheet(
    "background:#f5e9df;color:#55433a;"
    "border:1px solid #dfc9ba;border-radius:14px;padding:9px 13px;"
)
```

用户消息保持右侧布局，但同步使用相同字体对象；不改变滚动、选择文本或流式重绘。

- [ ] **Step 4: 更新 API Key 状态文案与刷新路径。**

```python
if source is None:
    self.api_key_btn.setText("🔑 API Key：未配置")
    self._set_api_key_badge(True)
else:
    self._set_api_key_badge(False)
```

在保存或删除 Key 的回调末尾调用 `_refresh_ai_tool_buttons()`；保留环境变量和本机配置的现有文案。

- [ ] **Step 5: 运行定向测试，确认通过。**

Run: `$env:QT_QPA_PLATFORM='offscreen'; python -m pytest -q tests/test_chat_tools.py`

Expected: 新增聊天状态、徽标和字体测试通过，既有聊天工具测试不回归。

### Task 3: 主菜单设置红点与运行时字体刷新

**Files:**

- Modify: `D:\Agent_project\Petpet\pet.py:BubbleMenu.paintEvent, PetWindow.apply_runtime_settings`
- Modify: `D:\Agent_project\Petpet\tests\test_menu_ui.py`
- Modify: `D:\Agent_project\Petpet\tests\test_settings_ui.py`

**Interfaces:**

- Consumes: `ai.get_api_key_source() -> str | None`、`BubbleMenu._bubble_rects`。
- Produces: `BubbleMenu.needs_api_key_configuration() -> bool`（静态或实例 helper）以及设置入口红点绘制。

- [ ] **Step 1: 写入失败测试，固定设置入口的未配置状态判定。**

```python
def test_settings_entry_requires_badge_without_api_key(self):
    with patch("pet.ai.get_api_key_source", return_value=None):
        self.assertTrue(pet.BubbleMenu.needs_api_key_configuration())

    with patch("pet.ai.get_api_key_source", return_value="config"):
        self.assertFalse(pet.BubbleMenu.needs_api_key_configuration())
```

- [ ] **Step 2: 在菜单绘制中添加设置红点。**

```python
needs_key = self.needs_api_key_configuration()
show_badge = (
    (action in ("more", "achievements") and has_claimable)
    or (action == "settings" and needs_key)
)
```

复用现有白色描边加红色圆点的绘制坐标；成就红点与设置红点可独立出现。

- [ ] **Step 3: 确保设置保存后已打开聊天窗口重新应用字体和状态。**

```python
chat.s = self.settings
chat._apply_style()
chat._refresh_ai_tool_buttons()
chat._set_log_messages(chat._history_messages())
```

保留现有尺寸重算和窗口重定位；只在 `self.chat_win is not None` 时执行。

- [ ] **Step 4: 运行菜单与设置定向测试。**

Run: `$env:QT_QPA_PLATFORM='offscreen'; python -m pytest -q tests/test_menu_ui.py tests/test_settings_ui.py`

Expected: 未配置时设置入口判定为真；已配置时为假；既有菜单行为与设置即时应用测试通过。

### Task 4: 集成验证与源码验收

**Files:**

- Modify: `D:\Github Desktop\My-Obsidian\项目\Petpet\开发记录\聊天界面与 API Key 配置提示实现计划.md`
- Verify: `D:\Agent_project\Petpet\pet.py`

**Interfaces:**

- Consumes: Task 1 至 Task 3 的测试与源码行为。
- Produces: 可验收的源码进程与完成状态开发记录。

- [ ] **Step 1: 完整测试和编译检查。**

Run:

```powershell
$env:QT_QPA_PLATFORM='offscreen'; python -m pytest -q
python -m compileall -q pet.py buddy_ai.py tests
```

Expected: 全部测试通过且无编译错误。

- [ ] **Step 2: 人工验收状态。**

未配置 Key 时检查聊天 API Key 按钮和主菜单设置按钮均有红点；配置后关闭重开菜单确认红点消失；调整聊天字体大小后检查小狗消息、用户消息、输入框与工具按钮同步改变。

- [ ] **Step 3: 更新开发记录。**

将该计划的 `status` 更新为 `completed`，记录最终测试数量、源码进程 PID 与实际验收结果。
