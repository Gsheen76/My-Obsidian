---
title: Petpet v1.7.3 发布说明
type: project
tags:
  - project/petpet
  - release
  - v1.7.3
summary: v1.7.3 于 2026-09-15 发布——家具 12 件整套重制、状态卡重新设计、生日提醒上线、内存减半（347→174MB）、三天三次的闪退根除、遮挡滞回带消闪烁。
status: active
source: D:\Agent_project\Petpet
updated: 2026-09-15
---

# Petpet v1.7.3 发布说明

> [!summary] Summary
> 发布提交 `eb5ad93`（release 主体 a1d88bf + 审查修正），**published 2026-09-15T06:19:24Z**，四资产（Petpet.exe / windows.zip / macOS-arm64.zip / SHA256SUMS），远端校验和与本地逐字节一致，发布基线 **856 tests**，CI 全绿。

## 版本内容（六大块）

1. **家具扩充与重制（8→12 件）**：挂钟/猫爬架/软垫床/摇椅新增，全套按用户定稿画风重制、用户自行去背景的透明素材直落；抠图管线升级（连通背景+接触阴影 BFS 吸收+彩色包围保护）；引擎接地软影；购买默认收纳；商店家居四栏；装修面板滚动；遮挡 2.5D+拖拽置顶+±6px 滞回带。
2. **状态卡重设计**：用户定稿暖木挂牌底板 + 场景画笔实时叠画（文字按最终分辨率栅格化，模糊/错位两轮根治）。
3. **长期记忆提醒**：生日/纪念日（关键词+公历月日双条件，每条当日一次）；四季+公历节日搭话；聊天导出 txt；档案 JSON 导入导出。
4. **性能**：内存 347→174MB（姿势 2×/动画 1.5× 显示预算预缩）；落地连续碰撞顺滑；触底音效删除。
5. **稳定**：BonusBubble 保活根治三天三次闪退（qt_static_metacall AV）；faulthandler 崩溃转储常驻。
6. **细节**：回复单段不换行；午餐肉头像整身还原（耳尖入圆）；新按键胶囊化；菜单悬浮跟手优化。

## 发布流程记录

- 版本锚点三件套（version.py / test_release_metadata / game_knowledge）+ README 亮点 + RELEASE_NOTES。
- **双轴 code-review**（v1.7.2→HEAD）：规范轴 1 硬违规（崩溃日志硬编码路径→DATA_DIR）+ 判断题若干（墙面集合抽 WALL_DECORATIONS、局部 import math 清理已做；chip bar 抽取/尺寸双份维护留待后续）；需求轴 3 项修正（导出 pet 字段、scipy 撤除、提醒措辞对齐）。
- `release.ps1 -Version 1.7.3` 一趟跑通（无 TLS 中断）；macOS workflow dispatch→watch→publish。
- 发布后宠物已重启（动态 PID），闪烁日志清空换新基线（滞回带后只记真实越带翻转）。
