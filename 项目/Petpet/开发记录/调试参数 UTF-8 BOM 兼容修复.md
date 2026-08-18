---
title: 调试参数 UTF-8 BOM 兼容修复
type: project
tags:
  - Petpet
  - 开发记录
  - 参数调试器
status: completed
source: D:\Agent_project\Petpet
updated: 2026-08-06
summary: 修复 `debug_parameters.json` 带 UTF-8 BOM 时被加载器忽略、动画 FPS 回退默认值的问题，并完成进食和抚摸动画 `10 FPS` 的运行时验证。
---

# 调试参数 UTF-8 BOM 兼容修复

> [!summary] Summary
> 修复 `debug_parameters.json` 带 UTF-8 BOM 时被加载器忽略、动画 FPS 回退默认值的问题，并完成进食和抚摸动画 `10 FPS` 的运行时验证。

## 根因

Windows PowerShell 常见的 UTF-8 写入方式会产生 BOM；原加载器使用 `utf-8` 解码，JSON 解析失败后静默回退到默认调试参数。

## 修复与验证

- `load_debug_parameters()` 改用 `utf-8-sig`，兼容带或不带 BOM 的 UTF-8 JSON。
- 新增带 BOM 配置的回归测试；旧实现失败，修复后通过。
- 完整测试：`165 passed`；`compileall` 通过。
- 当前保存与运行时值：`animation_eat_fps = 10`、`animation_pet_fps = 10`。
- 源码进程已重启，PID：`13832`。

## 关联记录

- [[参数调试器审查修复记录]]
- [[参数调试器 UI 与运行时反馈实现计划]]
