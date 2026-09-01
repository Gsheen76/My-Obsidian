---
title: Windows 更新链路 v1.3.0 到 v1.3.1 实现计划
type: project
tags:
  - Petpet
  - 开发记录
  - 更新
  - Windows
status: completed
source: D:\Agent_project\Petpet
updated: 2026-08-06
summary: 以隔离的真实发布资产升级为主验证，依据失败证据补充最小修复和自动化回归测试。
---

# Windows 更新链路 v1.3.0 到 v1.3.1 实现计划

> [!summary] Summary
> 以隔离的真实发布资产升级为主验证，依据失败证据补充最小修复和自动化回归测试。

## 执行步骤

- [x] 下载并校验 `v1.3.0`、`v1.3.1` Windows 发布资产。
- [x] 建立临时隔离安装目录并启动 `v1.3.0`。
- [x] 通过更新器执行 `v1.3.1` 下载、原位替换和新版重启。
- [x] 对比替换前后哈希、进程、临时文件和用户数据目录。
- [x] 为复现的失败路径写失败测试。
- [x] 实现最小更新器修复并运行完整测试。
- [x] 再执行一次真实隔离升级，记录最终证据。

## 验证结果

- 隔离目录：`%TEMP%\Petpet-update-lab-v130-v131-rerun`。
- `v1.3.1` 目标 EXE SHA-256：`61995F0FBFA475722CD23DDEE00AA76B5DD7C3486839C2AFEA9D98B65600F43B`。
- 替换完成后 `.backup-*` 与 `.update-*` 文件数量均为 `0`。
- 隔离用户数据写入 `data\Petpet`，未使用正式 `%LOCALAPPDATA%\Petpet`。
- 更新器测试 `9/9` 通过；项目测试 `169/169` 通过。
- 修复：备份文件在启动新版前删除，避免新版启动后锁住备份导致残留。
