---
title: Petpet v1.5.1 发布说明
updated: 2026-08-17
version: v1.5.1
status: published
tags:
  - project/petpet
  - release
type: project
summary: 记录 Petpet v1.5.1 发布说明 的说明内容、使用要点和当前状态。
---

# Petpet v1.5.1 发布说明

`v1.5.1` 完成代码与资源结构重构收尾，修复重构后桌面宠物首次绘制崩溃，并公开
Windows 与 macOS 双架构安装资产。

## 主要更新

- 业务实现按 `app`、`chat`、`home`、`progression`、`minigames` 和 `ui` 进入 `petpet` 包。
- 根目录旧模块保留为兼容入口。
- 桌面宠物与家园宠物资源独立管理。
- 运行资源与制作源图分离到 `assets/runtime` 和 `assets/source`。
- 修复 `POSE_NAMES` 缺失导致的桌面宠物首次绘制 `NameError`。
- 修复构建工具读取旧资源路径的问题。

## 下载

- [GitHub Release v1.5.1](https://github.com/Gsheen76/Petpet/releases/tag/v1.5.1)
- `Petpet-v1.5.1-windows.zip`
- `Petpet-v1.5.1-macOS-arm64.zip`
- `Petpet-v1.5.1-macOS-intel.zip`

macOS 应用尚未进行 Apple Developer ID 签名和公证。首次打开时可能需要在系统设置的
“隐私与安全性”中选择“仍要打开”。
