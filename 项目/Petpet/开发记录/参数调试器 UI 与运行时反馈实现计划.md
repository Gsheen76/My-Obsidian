---
title: 参数调试器 UI 与运行时反馈实现计划
type: project
tags:
  - Petpet
  - 开发记录
  - 参数调试器
summary: 将参数调试器放大为可读的源码调试面板，并用真实 PetWindow 回归测试确认调节值进入运行时。
status: approved
source: D:\Agent_project\Petpet
updated: 2026-08-06
---

# 参数调试器 UI 与运行时反馈实现计划

> [!summary] Summary
> 将参数调试器放大为可读的源码调试面板，并用真实 `PetWindow` 回归测试确认调节值进入运行时。

## 目标与架构

只修改源码调试器和测试，不改变正式版设置、存档格式或默认游戏平衡。`PetWindow.set_debug_parameter()` 继续是唯一运行时应用入口；`ParameterTunerWindow` 负责控件同步、行级反馈和保存操作；真实运行时测试负责验证参数被写入正确的实例属性、设置字典、动画规格或共享规则模块。

## 全局约束

- 调试器只在源码版出现，冻结版不新增调试入口。
- 默认窗口尺寸约为 `1080 x 920`，必须按屏幕可用区域收缩，不能越界。
- 每个参数都显示当前生效值和生效时机；被 clamp 后的值以运行时读取结果为准。
- “恢复默认”先作用于当前进程；只有点击“保存调试参数”才写入 `debug_parameters.json`。
- 使用 `QT_QPA_PLATFORM=offscreen` 运行 Qt 测试；所有全局 progression/小游戏参数测试结束后恢复原值。
- 完成后运行完整 `python -m pytest -q`，不删除或覆盖用户已有改动。

## 文件边界

- 修改 `D:\Agent_project\Petpet\parameter_tuner.py`：窗口尺寸、字体与间距、参数行反馈、控件同步和屏幕边界处理。
- 修改 `D:\Agent_project\Petpet\tests\test_parameter_tuner.py`：UI 尺寸、反馈文案、同步和保存行为测试。
- 创建 `D:\Agent_project\Petpet\tests\test_debug_parameters_runtime.py`：真实 `PetWindow` 参数应用测试。
- 不修改 `pet.py` 的参数语义；如果测试暴露应用入口缺少实际运行时更新，只在 `pet.py` 的对应分支做最小补丁并添加回归断言。

## 任务 1：补充调试器 UI 和应用反馈的失败测试

**文件：**

- 修改：`D:\Agent_project\Petpet\tests\test_parameter_tuner.py`
- 测试目标：`ParameterTunerWindow`

- [ ] 新增测试，断言窗口初始尺寸至少为 `1000 x 880`，并且 `show_near_pet()` 在 `1400 x 900` 屏幕上不会超过屏幕边界。
- [ ] 新增测试，断言每个参数控件都有行级反馈控件，并且修改 `gravity` 后反馈包含规范化后的 `1234` 和生效状态。
- [ ] 新增测试，断言滑块和数值框同步时只产生一次 `set_debug_parameter` 调用，避免重复应用。
- [ ] 新增测试，断言应用返回失败时顶部状态显示失败，而不是误报“已实时应用”。FakePet 的 `set_debug_parameter` 返回 `False` 即可复现。
- [ ] 运行 `pytest tests/test_parameter_tuner.py -q`，确认新增断言在旧实现上失败，记录失败原因后再改实现。

## 任务 2：实现放大后的调试器 UI

**文件：**

- 修改：`D:\Agent_project\Petpet\parameter_tuner.py`

- [ ] 将默认固定尺寸调整为 `1080 x 920`，保留滚动区域；在 `show_near_pet()` 中先计算 `available_width = max(420, screen.width() - 24)`、`available_height = max(560, screen.height() - 60)`，再用 `min(preferred, available)` 收缩，保证小屏不越界。
- [ ] 沿用项目独立像素字体策略，统一增大标题、分组标题、标签、说明、数值框和按钮字体；增大控件高度、行间距和滑块轨道/手柄，确保 100% 和高 DPI 下都可点击。
- [ ] 在每个参数行创建 `QLabel` 反馈控件，保存到 `self.controls[key]["feedback"]`，显示格式为 `当前生效：<value> · <timing>`。
- [ ] 增加明确的 `PARAMETER_EFFECT_TIMING` 映射：尺寸/物理/动画/衰减/进食时长/小游戏参数标记“立即生效”，自动权重、自动睡眠阈值、挖宝、好感冷却标记“下一次行为生效”。未列出的参数使用“当前运行时生效”。
- [ ] 调整滚动内容边距和分组边距，避免说明文本挤压数值框；保留单项恢复、复制、保存和关闭按钮。

## 任务 3：统一控件同步与真实值反馈

**文件：**

- 修改：`D:\Agent_project\Petpet\parameter_tuner.py`

- [ ] 添加 `_apply_value(self, key, value)`：调用 `self.pet.set_debug_parameter(key, value)`，失败时更新顶部状态并返回 `False`；成功时从 `self.pet.debug_parameter_value(key)` 读取实际值，使用 `QSignalBlocker` 同步数值框和滑块，再刷新该行反馈和顶部状态。
- [ ] 让 `_spin_changed()` 和 `_slider_changed()` 都只负责换算输入后调用 `_apply_value()`，不再各自维护 `_syncing` 逻辑或直接写宠物。
- [ ] 让 `reset_parameter()` 通过同一应用入口生效，确保恢复默认不仅改变控件显示，也改变当前运行时值；`reset_defaults()` 继续只提示“当前生效，保存后写入档案”。
- [ ] 保存时导出 `debug_parameter_snapshot()` 的规范化值，并在成功后显示保存路径语义；复制时导出同一快照，避免 UI 值和运行时值不一致。
- [ ] 运行 `pytest tests/test_parameter_tuner.py -q`，确认所有 UI 测试通过。

## 任务 4：增加真实 PetWindow 运行时回归测试

**文件：**

- 创建：`D:\Agent_project\Petpet\tests\test_debug_parameters_runtime.py`
- 依赖：`pet.DEFAULT_STATE`、`pet.PetWindow`、`progression`、`minigames`

- [ ] 使用 `QT_QPA_PLATFORM=offscreen` 创建 `QApplication`，复制 `pet.DEFAULT_STATE`，设置安全的初始位置，并在 `tearDown` 关闭窗口和停止其计时器。
- [ ] 测试 `pet_width`、`pet_height`、`dog_height`：调用 `set_debug_parameter()` 后断言实例属性和窗口尺寸同时更新。
- [ ] 测试 `gravity`、`wall_bounce`、`floor_bounce`、`ground_friction`、`walk_speed_min`、`walk_speed_max`：断言 `debug_physics`、行走速度范围和实例参数更新。
- [ ] 测试 `animation_eat_fps` 和 `animation_play_fps`：断言 `animation_specs` 中对应 FPS 更新。
- [ ] 测试衰减、自动睡眠阈值、自动行为权重、进食动作时长：断言 `settings` 或实例属性更新。
- [ ] 测试好感增益/冷却、挖宝概率/冷却和小游戏时长/目标停留时间：保存原全局值，调用参数入口后断言共享模块值更新，测试结束恢复原值。
- [ ] 运行 `pytest tests/test_debug_parameters_runtime.py -q`，确认真实运行时测试通过。

## 任务 5：完整验证与交付检查

- [ ] 设置 `$env:QT_QPA_PLATFORM = 'offscreen'`，运行 `python -m pytest -q`，确认完整套件无回归。
- [ ] 运行 `python -m compileall parameter_tuner.py pet.py tests/test_parameter_tuner.py tests/test_debug_parameters_runtime.py`，确认新增代码可编译。
- [ ] 检查 Obsidian 记录中的实现计划状态和源码 Git 状态；不要把 `data/`、API Key 或个人存档纳入改动。
- [ ] 启动源码版 `pythonw.exe pet.py`，通过托盘“调试 → 参数调试器”验证窗口尺寸、数值修改、恢复默认和保存按钮；确认 `D:\Agent_project\Petpet\pet.py` 仍存在。

## 交付结果

- 调试器在常见屏幕上可读、可操作，且小屏不会越界。
- 每次修改都能看到真实运行时值和生效时机。
- UI 信号、真实 `PetWindow` 参数入口和共享规则模块都有自动化测试。
