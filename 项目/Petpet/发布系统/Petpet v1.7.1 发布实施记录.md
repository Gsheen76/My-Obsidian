---
title: Petpet v1.7.1 发布实施记录
type: project
tags:
  - project/petpet
  - release
  - v1.7.1
summary: v1.7.1 发布实施：内容范围（礼物系统/游戏自动隐藏/气泡菜单贴图化等）、发版流程执行与验证、SHA256 比对与 macOS Actions 产物确认。
status: active
source: D:\Agent_project\Petpet
updated: 2026-09-10
---

# Petpet v1.7.1 发布实施记录

> [!summary] Summary
> 2026-09-10 发布 v1.7.1（发布提交 `52d9105`，published_at `2026-09-10T07:20:56Z`）：打包 v1.7.0 后累积的礼物系统、游戏自动隐藏、气泡菜单贴图化、待机时长调整与一批界面精调。发布脚本一键完成测试/构建/标签/推送/GitHub Release；远端 SHA256SUMS 与本地 dist 逐字节一致。

## 1. 版本内容（对应用户指令）

| 功能 | 要点 |
|---|---|
| 礼物系统 | 商店第 5 页（3 档×3 选 1）+ 面板第 3 分栏送礼 + 每宠每档最爱 ×1.5（注册表 gift_preferences）+ 送礼成就 7 项；schema v3→v4 |
| 游戏自动隐藏 | `game_guard.py` 游戏路径单信号判定 + 2s 轮询；设置开关 `hide_in_game` 默认开；用户英雄联盟会话实战验证 |
| 气泡菜单贴图化 | 18 键哑光奶油贴图（gutter 拆分器拆 6×3 素材表）+ 图标即按键（悬浮名称胶囊） |
| 待机时长 | 三属性消耗统一 0.0556/2s：无强化 ≈2h、持久活力满级 ≈4h |
| 界面精调 | 5 槽页签栏素材、礼物分栏复用 4 槽素材、滚动条贴边统一、聊天头像大头照（0.80/上提 0.09）、家居卡名字居中、主菜单行宽对齐资料卡 620 |

## 2. 发版流程执行

1. **版本锚点三件套**：`version.py` → 1.7.1；README（当前版本 / v1.7.1 更新亮点 / 下载表 / release 命令行）；`game_knowledge.json` version 字段。门禁测试 `test_release_metadata.py` 同步更新（含 regex 与资产名三处）。
2. **发布说明**：`docs/RELEASE_NOTES_v1.7.1.md`（`# Pet陪它 v1.7.1` 开头供门禁校验）。
3. **提交**：`b08947a` feat（全部功能，36 文件）+ `52d9105` docs（HANDOFF 发布头）。
4. **`scripts/release.ps1 -Version 1.7.1`**：自动停宠物 → 全量测试 → PyInstaller 构建 → 打包/哈希 → 推 main+tag → 草稿 Release 传 Windows 资产 → Actions 构建 macOS arm64 传资产 → `--draft=false` 公开。
5. **脚本尾部按惯例手动收尾**：内置的大文件重下载校验过慢，改用「gh release view 资产清单 + 远端/本地 SHA256SUMS 逐字节比对」后 Stop 后台任务。

## 3. 验证

- 发布前 offscreen 全量 **758 passed**（发版门禁 9 条全绿）。
- 发布资产 4 件齐全（exe 160.8MB / windows.zip 160.4MB / macOS-arm64.zip 127MB / SHA256SUMS），`isDraft: false`。
- 远端 SHA256SUMS 与本地 dist 逐字节一致（exe `f58ea67c…`、zip `4ed21e82…`）。
- 发版脚本自动停了小狗，发布完成后已按 PassThru 流程重启（用户可立即用上新版）。

## 4. 待办遗留

- macOS 包由 GitHub Actions 自动构建上传，本地无法运行验证（与历史版本一致）。
- 下一版候选：聊天长期记忆、CI（GitHub Actions offscreen 测试）、套装分栏素材补图。

## 关联笔记

- [[Petpet v1.7.1 发布说明]]：面向用户的更新内容。
- [[版本规划与发布索引]]：版本入口表（本版已登记）。
- [[开发记录/2026-09-09 游戏自动隐藏判定收紧]]：本轮各功能迭代的逐日记录。
