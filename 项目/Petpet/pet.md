---
title: Petpet 项目工作记忆
type: project
tags:
  - project/petpet
  - Python
  - PyQt5
  - 工程协作
summary: 记录 Petpet 当前实现重点、协作约定和发布前验证要求。
updated: 2026-08-05
migrated: 2026-08-05
---

# Petpet 项目工作记忆

> [!summary] Summary
> 记录 Petpet 当前实现重点、协作约定和发布前验证要求。

## 项目定位

Petpet 是一个基于 PyQt5 的桌面陪伴宠物应用。主入口为 `D:\Agent_project\Petpet\pet.py`，包含透明置顶宠物窗口、拖拽物理、动画、聊天、状态衰减、自动休息、成长系统、商店、小游戏和 Windows/macOS 打包流程。

## 当前实现重点

- macOS 使用 `Qt.WA_MacAlwaysShowToolWindow` 保持小狗失去焦点后仍显示在最顶层。
- macOS 默认宠物窗口尺寸为 `150 x 180`，绘制高度为 `132`。
- 进食和摸头动画默认 `20 FPS`。
- 聊天消息使用原生 Qt 圆角消息组件，底色保持低饱和、浅色、低对比。
- `parameter_tuner.py` 是源码调试工具：通过滑块和精确数值框实时修改物理、尺寸、动画、状态衰减、成长反馈和小游戏参数；正式冻结版不显示调试入口。
- 调试参数可保存到运行数据目录的 `debug_parameters.json`，用于下一次源码启动继续调试。

## 协作约定

1. 用户说 `add tweaks` 时，理解为小幅、局部、可控的参数调整，不擅自扩大改动范围。
2. 任何参数微调优先加入参数优化器，确保可以实时试验，避免反复对话猜数值。
3. 桌面程序改动完成后必须运行测试、重建 `dist\Petpet.exe`、停止旧实例，并以无终端方式启动新版本供验证。
4. 视觉改动必须做离屏渲染或截图检查，不能只依据 QSS 或代码文字判断效果。
5. Qt 富文本圆角效果不稳定，消息气泡优先使用原生 Qt 组件实现。
6. 不回滚用户已有改动；提交前检查 `git status`，避免把运行数据、API key 或个人对话纳入发布。

## 常用验证

```powershell
$env:QT_QPA_PLATFORM = 'offscreen'
python -m pytest -q
```

源码调试入口：托盘菜单 -> `调试` -> `参数调试器`。正式发布版本不显示该入口。

## 关联笔记

- [[项目/Petpet/Petpet 项目总档案]]：项目功能、架构和发布档案。
- [[笔记/MOC/MOC-项目与实践]]：项目与实习专题入口。
- [[笔记/知识库/知识库索引]]：返回知识库索引。
