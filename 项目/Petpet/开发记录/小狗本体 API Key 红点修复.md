---
title: 小狗本体 API Key 红点修复
type: project
tags:
  - Petpet
  - 开发记录
  - API Key
  - UI
status: completed
source: D:\Agent_project\Petpet
updated: 2026-08-06
---

# 小狗本体 API Key 红点修复

> [!summary] Summary
> API Key 未配置时，在小狗本体的右上角显示红点提示，并与聊天入口及主菜单设置入口使用一致的配置状态。

## 问题与根因

此前仅在聊天窗口 API Key 按钮与主菜单“设置”项绘制提醒红点；`PetWindow.paintEvent()` 没有读取 API Key 配置状态，也没有宠物本体的绘制逻辑，因此小狗上不会出现提示。

## 实现

- 在 `PetWindow.needs_api_key_configuration()` 统一判断 `ai.get_api_key_source() == "none"`。
- 在 `PetWindow.paintEvent()` 的小狗可视区域右上角绘制白边红点。
- 本地配置或环境变量提供 API Key 时，红点不绘制。

## 验证

- 新增状态回归测试，验证未配置时为真、已配置时为假。
- 离屏渲染读取目标像素，结果为红点颜色 `#ee5e62`。
- 完整测试：`171 passed in 16.18s`。
- `python -m compileall -q pet.py tests`：通过。
- 源码版已重启，进程 PID：`28732`。

## 关联笔记

- [[聊天界面与 API Key 配置提示实现记录]]

