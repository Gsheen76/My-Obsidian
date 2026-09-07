---
title: Petpet v1.7.0 发布实施记录
type: project
tags:
  - project/petpet
  - release
  - v1.7.0
summary: v1.7.0 一键发布全程记录：版本 bump、release-gate、构建冒烟、草稿资产校验、公开发布与验证。
status: active
source: D:\Agent_project\Petpet
updated: 2026-09-07
---

# Petpet v1.7.0 发布实施记录

> [!summary] Summary
> `scripts/release.ps1 -Version 1.7.0` 全程无人工干预跑完（exit 0）；tag `v1.7.0` 推送成功、macOS 工作流 1m11s 完成、草稿四资产齐、SHA 比对一致、公开发布。

## 时间线

1. **版本 bump**（提交 `70b5444`）：`version.py` 1.7.0、README（当前版本/亮点段/资产名/一键命令）、`game_knowledge.json` version、`docs/RELEASE_NOTES_v1.7.0.md` 新建、release-gate 测试 9 条同步（函数名 `..._v163_assets`→`_v170_assets`）。
2. **发布前**：停桌面宠物进程（脚本也会自动停）；preflight 干净（工作树无未提交）。
3. **脚本阶段**：全量 715 passed → PyInstaller 构建 → 冒烟 → Windows 便携包+SHA256 → `git push --atomic`（main + tag）→ `gh release create --draft` → 触发 macOS 工作流（1m11s ✓，zip 直传草稿）。
4. **慢验证跳过**（v1.6.2 惯例）：脚本内置 400MB 资产重下载验证在本机网络过慢，改为等 macOS 完成后手动验证（见下），随后脚本自行走完 edit --draft=false 公开发布。

## 验证

- 草稿四资产齐：exe / windows.zip / macOS-arm64.zip / SHA256SUMS。
- 下载草稿件本地 sha256sum 与 `dist/Petpet-v1.7.0-SHA256SUMS.txt` 逐条比对一致（windows.zip `3F03...4999`、Petpet.exe `0ABB...3E9`）。
- 脚本尾声输出三资产最终 SHA 与 URL，`gh release view` 确认 `draft:false`。
- 桌面宠物进程重启恢复（PID 11500）。

## 坑位与备注

- release-gate 测试**硬编码版本号**三处（VERSION 断言、正则、README 资产名），每次发布必须同步 bump——本次第一遍漏 README 第 337 行一键命令导致 1 failed，补齐后全过。
- 全量测试必须在 commit 前跑完看结果（上一轮曾提交后才见 2 failed，本次严格先绿后提交）。
- `gh` 需 `GH_TOKEN`（`git credential fill` 取）+ `.tools/gh/bin/gh.exe`。

## 关联笔记

- [[发布系统/Petpet v1.7.0 发布说明]]：本次发布的面向用户说明与资产 SHA 清单。
- [[发布系统/版本规划与发布索引]]：版本唯一入口，v1.7.0 已登记「已发布」。
