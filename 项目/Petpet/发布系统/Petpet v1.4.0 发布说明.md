---
title: Petpet v1.4.0 发布说明
updated: 2026-08-11
tags:
  - Petpet
  - 发布
  - v1-4-0
status: published
type: project
summary: 记录 Pet陪它 v1.4.0 的背景、过程和结果。
---

# Pet陪它 v1.4.0

本次更新为 Petpet 加入完整的家园体验：小狗拥有独立的小屋活动模型，可以在 2.5D 地面上按目标移动、待机、说话和走到地毯睡觉；家具商店与装修编辑器也已经接入原有 Pet 币和存档系统。快捷菜单同步重组，让常用入口更直接。

## 主要更新

- 快捷菜单改为“聊天、小屋、商店、互动、更多”一行五个入口。
- 互动页集中提供抚摸、喂食、玩耍和睡觉；更多页保留记录、成就、小游戏、设置、隐藏、教程、返回和退出。
- 新增固定在屏幕右下区域的 `900×768` 家场景和独立双列家具装修侧栏。
- 家具支持购买、放置、拖动、缩放、旋转、收纳和变换存档。
- 小屋内支持左键指定地面目的地，小狗按四个方向在 2.5D 地面移动。
- 固定宠物脚印会随走过的路线消失，终点使用暖色倾斜椭圆和箭头提示。
- 小屋小狗新增正坐待机、暖色对话框和与桌面一致的右键快捷交互。
- 手动或低精力睡眠会先走到地毯，再播放 8 帧、`3 FPS` 睡眠动画。
- 旧存档自动补齐家场景、家具和小屋宠物位置字段，不重置现有数据。

## 下载

- [Windows EXE](https://github.com/Gsheen76/Petpet/releases/download/v1.4.0/Petpet.exe)
- [Windows 便携 ZIP](https://github.com/Gsheen76/Petpet/releases/download/v1.4.0/Petpet-v1.4.0-windows.zip)
- [macOS Apple 芯片](https://github.com/Gsheen76/Petpet/releases/download/v1.4.0/Petpet-v1.4.0-macOS-arm64.zip)
- [macOS Intel](https://github.com/Gsheen76/Petpet/releases/download/v1.4.0/Petpet-v1.4.0-macOS-intel.zip)

macOS 应用尚未进行 Apple Developer ID 签名和公证，首次打开可能需要在“系统设置 → 隐私与安全性”中选择“仍要打开”。

## 关联

- [[Petpet v1.4.0 发布设计]]
- [[Petpet v1.4.0 发布实施记录]]
- [[Petpet 总档案]]
