---
title: 参数调试器 UI 与运行时反馈实现计划
type: project
tags:
  - Petpet
  - 开发记录
  - 参数调试器
summary: 将参数调试器放大为可读的源码调试面板，并用真实 PetWindow 回归测试确认调节值进入运行时。
status: completed
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

- [x] 新增测试，断言窗口初始尺寸至少为 `1000 x 880`，并且 `show_near_pet()` 在 `1400 x 900` 屏幕上不会超过屏幕边界。
- [x] 新增测试，断言每个参数控件都有行级反馈控件，并且修改 `gravity` 后反馈包含规范化后的 `1234` 和生效状态。
- [x] 新增测试，断言滑块和数值框同步时只产生一次 `set_debug_parameter` 调用，避免重复应用。
- [x] 新增测试，断言应用返回失败时顶部状态显示失败，而不是误报“已实时应用”。FakePet 的 `set_debug_parameter` 返回 `False` 即可复现。
- [x] 运行 `pytest tests/test_parameter_tuner.py -q`，旧实现先以 3 个预期失败进入 RED，修复后为 `7 passed`。

## 任务 2：实现放大后的调试器 UI

**文件：**

- 修改：`D:\Agent_project\Petpet\parameter_tuner.py`

- [x] 将默认固定尺寸调整为 `1080 x 920`，保留滚动区域；按屏幕可用区域收缩，保证小屏不越界。
- [x] 沿用项目独立像素字体策略，统一增大标题、分组标题、标签、说明、数值框和按钮字体；增大控件高度、行间距和滑块轨道/手柄。
- [x] 在每个参数行创建 `QLabel` 反馈控件，保存到 `self.controls[key]["feedback"]`，显示格式为 `当前生效：<value> · <timing>`。
- [x] 增加 `PARAMETER_EFFECT_TIMING` 映射，区分立即生效和下一次行为生效的参数。
- [x] 调整滚动内容边距和分组边距，保留单项恢复、复制、保存和关闭按钮。

## 任务 3：统一控件同步与真实值反馈

**文件：**

- 修改：`D:\Agent_project\Petpet\parameter_tuner.py`

- [x] 添加 `_apply_value(self, key, value)`，统一处理成功、失败、真实值读取、控件同步和行级反馈。
- [x] 让 `_spin_changed()` 和 `_slider_changed()` 都通过 `_apply_value()` 应用参数。
- [x] 让 `reset_parameter()` 通过同一应用入口生效，`reset_defaults()` 继续只作用于当前进程。
- [x] 保存和复制均使用规范化后的当前快照。
- [x] 运行 `pytest tests/test_parameter_tuner.py -q`，结果为 `7 passed`。

## 任务 4：增加真实 PetWindow 运行时回归测试

**文件：**

- 创建：`D:\Agent_project\Petpet\tests\test_debug_parameters_runtime.py`
- 依赖：`pet.DEFAULT_STATE`、`pet.PetWindow`、`progression`、`minigames`

- [x] 使用 `QT_QPA_PLATFORM=offscreen` 创建 `QApplication`，复制 `pet.DEFAULT_STATE` 并在 `tearDown` 关闭窗口。
- [x] 测试尺寸、物理、行走速度、动画 FPS 和衰减目标更新。
- [x] 测试好感、挖宝和小游戏共享模块目标更新，并在测试结束恢复原值。
- [x] 修复参数入口的 clamp 快照缺口：真实窗口值为 `40` 时快照不再返回 `20`。
- [x] 运行 `pytest tests/test_debug_parameters_runtime.py -q`，结果为 `3 passed`。

## 任务 5：完整验证与交付检查

- [x] 设置 `$env:QT_QPA_PLATFORM = 'offscreen'`，运行 `python -m pytest -q`，结果为 `161 passed`。
- [x] 运行 `python -m compileall parameter_tuner.py pet.py tests/test_parameter_tuner.py tests/test_debug_parameters_runtime.py`，无错误。
- [x] 检查源码 Git 状态，未新增 `data/`、API Key 或个人存档；源码 `pet.py` 仍存在。
- [x] 离屏检查窗口几何、控件字体度量和样式；当前 Windows offscreen 平台的 QLabel 文字截图渲染不可用，因此没有把该环境的空白文字截图误判为 UI 缺陷。
- [x] 重启源码版 `pythonw.exe pet.py`，当前进程 ID 为 `24424`。

## 交付结果

- 调试器在常见屏幕上可读、可操作，且小屏不会越界。
- 每次修改都能看到真实运行时值和生效时机。
- UI 信号、真实 `PetWindow` 参数入口和共享规则模块都有自动化测试。

## 实施结果

- 参数调试器默认尺寸从 `760 x 860` 调整为 `1080 x 920`，小屏会按可用区域收缩。
- 每个参数行显示真实运行时值和生效时机；应用失败会明确提示，不再误报成功。
- `PetWindow.set_debug_parameter()` 先归一化 clamp 值，再写入快照，解决 UI 显示值与实际生效值不一致的问题。
- 完整验证结果：`161 passed`，`compileall` 通过，源码版已重启供验收。
