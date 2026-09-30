---
title: 2026-09-30 摇醒卡顿根治（SpeechBubble DWM 冻结）
type: log
tags:
  - project/petpet
  - performance
  - bugfix
summary: 摇醒卡在原地不跟鼠标的两层根因——wake 函数同步阻塞 37ms（deferred 修）+ SpeechBubble 首次 show 的 DWM 合成 ~1.7s 冻结（预建+show 一帧预热修）。
status: done
source: D:\Agent_project\Petpet
updated: 2026-09-30
---

# 2026-09-30 摇醒卡顿根治（SpeechBubble DWM 冻结）

> [!summary] Summary
> 用户「摇醒卡在原地不跟鼠标」。第一轮修 wake 函数的 37ms 同步阻塞（deferred），仍卡——深层根因=SpeechBubble 首次 show 的 DWM 合成冻结 ~1.7s。预建+show 一帧预热根治。全量零失败。

## 排查链（两轮递进）

### 第一轮：wake 函数内部成本
逐项计时：record_action 2ms / say 25ms / play_sound 0.1ms / save_state 9ms → 同步 37ms 阻塞。修=deferred 到下一拍（同步 37→4ms）——改善但用户仍报卡。

### 第二轮：真正的元凶——DWM 冻结
- 500ms 事件循环（含 say）实际 wall **2206ms** → say 引入 **+1700ms** 额外
- 对照（不含 say）wall 1307ms → 基线开销
- 预建隐藏 bubble 后 say 仍 +1700ms → **成本不在创建而在首次 show（DWM 合成）**
- 预建 + show 一帧再 hide → say 降至 **8.6ms**

## 修复

PetWindow 构造尾部：
1. 预建 SpeechBubble
2. `resize(10,10) + move(-5000,-5000) + show() + hide() + move(0,0)` — 瞬态闪现一帧（非 -10000 常驻停靠，避开 DPI 钳制坑）
3. say() 复用常驻泡（不再 close 旧→建新）

## 坑位

**原生窗首次 show 的 DWM 合成是秒级冻结**——必须启动期 show 一帧预热。与音效预热同一原理：一次性成本放启动。

## 关联笔记

- [[开发记录/2026-09-28 按钮反馈纯缩放反馈统一与四角锁定真根因]]：DWM 衰减型开销首次定位。
