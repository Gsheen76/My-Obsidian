---
title: Petpet v1.6.0 发布说明
type: release
status: published
version: v1.6.0
date: 2026-08-22
tags:
  - project/petpet
  - release
  - v1.6.0
aliases:
  - Petpet 1.6.0 Release Notes
---

# Petpet v1.6.0 发布说明

> [!success] 当前状态
> `v1.6.0` 已于 2026-08-22 公开发布，目标提交为 `0d40e042f10bbe859d3c080fa50dcbde29d2e3d8`。

## 下载

- [GitHub Release v1.6.0](https://github.com/Gsheen76/Petpet/releases/tag/v1.6.0)
- Windows：`Petpet.exe`、`Petpet-v1.6.0-windows.zip`
- macOS：`Petpet-v1.6.0-macOS-arm64.zip`、`Petpet-v1.6.0-macOS-intel.zip`
- 校验和：`Petpet-v1.6.0-SHA256SUMS.txt`

## 本版本重点

- 完成午餐肉与冰淇淋的多宠物身份、独立属性/聊天记忆与桌面/家园同步。
- 接入按宠物区分的待机、行走、睡眠与套装动画回退，避免切换宠物时串用素材。
- 完成商店宠物、套装、家具和强化页的价格、折扣、简介、免费赠送优先和双列布局。
- 统一聊天头像、昵称显示和午餐肉/冰淇淋差异化性格提示词。
- 修复家园待机尺寸、阴影匹配、睡眠尺寸、菜单双击闪退与精灵表边界问题。

## 兼容与提醒

- 升级保留已有名字、等级、Pet 币、家具、强化、聊天记忆和设置；新增字段自动补齐。
- macOS 资产由 GitHub Actions 构建，未签名、未公证，首次打开可能需要在系统设置中允许。
- Windows 构建日志有 PyInstaller `sip` hidden import 警告，但构建、启动冒烟和发布资产校验均通过。

关联记录：[[Petpet v1.6.0 发布实施记录]]、[[Petpet 总档案]]、[[版本规划与发布索引]]。
