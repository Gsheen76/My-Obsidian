---
title: Petpet v1.4.1 发布实施记录
updated: 2026-08-13
tags:
  - Petpet
  - 发布
  - v1-4-1
status: published
type: project
summary: 记录 Petpet v1.4.1 发布实施记录 的实施过程、结果和问题。
---

# Petpet v1.4.1 发布实施记录

> [!success] 发布结果
> `v1.4.1` 已公开：[GitHub Release](https://github.com/Gsheen76/Petpet/releases/tag/v1.4.1)。Windows 与 macOS 双架构四项资产均已下载并完成 SHA256 复核。

## Git 与发布对象

- 发布提交：`8136eccd0ca44cbe6a38da44e67feafbef397626`
- 注释标签：`v1.4.1`，peeled commit 与发布提交一致
- 发布后工具维护提交：`f1d505d`，修复 GitHub 时间戳的跨区域解析；不改变已发布标签
- macOS Actions：[运行 #31631123999](https://github.com/Gsheen76/Petpet/actions/runs/31631123999)

## 验证结果

- Python 全量：`407 passed in 40.42s`
- 发布脚本契约：`16 passed`
- Cloudflare Worker：`13 passed`
- Python 编译、PowerShell AST、`git diff --check`：通过
- Windows PyInstaller 构建与隐藏窗口冒烟：通过
- Worker 部署版本：`834a33fd-35e0-4029-963b-58d955c8ef15`

## 发布资产

| 资产 | 字节 | SHA256 |
|---|---:|---|
| `Petpet.exe` | 91,952,531 | `29501E436D3452EDBBB88909A2E5C5B976929F8B737897B305E75B521FDBA7F8` |
| `Petpet-v1.4.1-windows.zip` | 91,630,347 | `3F19A5A6E6F55138A6CD4FD7D06863F30DE8A142F144F12923A0C5E7C9DBD694` |
| `Petpet-v1.4.1-macOS-arm64.zip` | 73,219,592 | `AA272FD74339F9B5FB7167AFAB18CCDACD71E17DDC3425ED781AD385E2505AA6` |
| `Petpet-v1.4.1-macOS-intel.zip` | 76,072,816 | `BBBA8312471A970437E77E557BE077D793EF882519FA428BA415274F6A72B0DD` |

## 一键脚本收尾

发布过程中实际发现并修正了三个可恢复性问题：旧 EXE 文件锁、GitHub CLI 对缺少无关 `read:org` scope 的登录判断，以及 GitHub UTC 时间戳在中文区域设置下的解析。脚本现使用原子 main/tag 推送、唯一 dispatch ID、临时凭据恢复和 invariant `DateTimeOffset` 解析。

后续版本命令：

```powershell
.\scripts\release.ps1 -Version X.Y.Z
```

## 关联

- [[Petpet v1.4.1 一键发布设计]]
- [[Petpet v1.4.1 发布实施计划]]
- [[Petpet v1.4.1 发布说明]]
- [[Petpet 总档案]]
