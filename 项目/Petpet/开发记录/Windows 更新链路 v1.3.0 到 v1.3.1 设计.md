---
title: Windows 更新链路 v1.3.0 到 v1.3.1 设计
type: project
tags:
  - Petpet
  - 开发记录
  - 更新
  - Windows
status: completed
source: D:\Agent_project\Petpet
updated: 2026-08-06
---

# Windows 更新链路 v1.3.0 到 v1.3.1 设计

> [!summary] Summary
> 在隔离临时安装目录中，用真实发布资产复现 `v1.3.0 → v1.3.1` 的 Windows 原位更新，并将失败点转化为更新器回归测试与修复。

## 范围与边界

- 使用 GitHub Releases 的 `v1.3.0` 和 `v1.3.1` Windows 资产。
- 所有下载、解压、替换助手和日志只放在 `%TEMP%\Petpet-update-lab`。
- 不修改 `D:\Agent_project\Petpet` 源码目录中的发布文件，不覆盖正式安装，不操作 `%LOCALAPPDATA%\Petpet` 用户数据。

## 链路

1. 下载并解压 `v1.3.0`，得到隔离的旧版 `Petpet.exe`。
2. 运行旧版，使用真实 `v1.3.1` 发布资产进入现有下载与 Windows 替换助手。
3. 等待旧进程退出，验证目标 EXE 的 SHA-256 与 `v1.3.1` 一致，并确认新版进程启动。
4. 收集替换助手、临时文件、进程和返回状态证据，定位失败的边界。

## 修复原则

- 保持用户数据与安装目录以外的数据隔离。
- 更新失败时保留可启动旧版本；成功时只替换目标 `Petpet.exe`。
- 以真实失败路径补测试，覆盖进程等待、原位替换、重启和清理。

## 实际问题与修复

`File.Replace` 的备份文件原先在启动新版后才清理。新版启动链路会继续占用该旧镜像，导致 `.Petpet.backup-*.exe` 清理失败并残留。现改为在 `Start-Process` 之前重试删除备份；替换失败仍删除 pending/backup 并重启旧版本。

## TLS 握手超时

用户实测更新包下载时出现 `<urlopen error _ssl.c:983: The handshake operation timed out>`。这是 GitHub 连接建立阶段的瞬时网络失败，原实现只尝试一次便直接弹出 Python 原始异常。

修复后，更新检查、网页回退和更新包下载统一最多尝试两次，第二次前等待一秒；HTTP 状态错误不重试。两次均失败时向玩家显示“网络连接超时，请稍后重试”，同时在更新结果中保留原始异常细节。回归测试覆盖首次握手超时后成功，以及最终失败时的用户提示。
