---
title: Petpet v1.5.2 发布说明
type: project
version: v1.5.2
status: published
updated: 2026-08-20
source: D:\Agent_project\Petpet\.worktrees\home-scene-system\docs\RELEASE_NOTES_v1.5.2.md
tags:
  - project/petpet
  - release
summary: v1.5.2 的桌面待机动画、套装待机资源、性能与菜单稳定性更新说明。
---

# Petpet v1.5.2 发布说明

`v1.5.2` 聚焦桌面宠物的待机动画、套装资源、交互性能和菜单稳定性。

## 主要更新

- 新增 16 帧桌面待机动画，并支持恐龙、草莓套装的独立待机动画。
- 商店装扮转为套装售卖；装备后桌面宠物使用对应待机动画和拖拽预览图。
- 统一调整摸头、进食、玩耍、挖宝与睡眠动画的显示尺寸；睡眠缩放为 `0.7`，自然属性消耗降为原来的一半。
- 按需解码互动动画、预热右键菜单和属性卡，降低内存占用与首次菜单阻塞。
- 修复菜单预热的原生窗口生命周期竞态，增强意外隐藏后的小狗显示恢复与置顶保持。
- 增加待机动画、套装预览、菜单预热、内存限制和窗口生命周期回归测试。

## 数据与下载

升级不重置宠物名字、属性、好感、等级、经验、Pet币、家具、装扮、设置、头像、个人 API Key 或聊天记忆。Windows 用户数据位于 `%LOCALAPPDATA%\Petpet`，macOS 位于 `~/Library/Application Support/Petpet`。

下载资产为 `Petpet.exe`、Windows 便携包，以及 macOS Apple Silicon/Intel 两种 ZIP。macOS 应用尚未完成 Apple Developer ID 签名和公证。

## 关联

- [[版本规划与发布索引]]
- [[Petpet 总档案]]
