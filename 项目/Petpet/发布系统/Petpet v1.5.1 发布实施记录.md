---
title: Petpet v1.5.1 发布实施记录
updated: 2026-08-17
version: v1.5.1
status: published
tags:
  - project/petpet
  - release
  - verification
type: project
summary: 记录 Petpet v1.5.1 发布实施记录 的实施过程、结果和问题。
---

# Petpet v1.5.1 发布实施记录

> [!success]
> `v1.5.1` 已公开：[GitHub Release](https://github.com/Gsheen76/Petpet/releases/tag/v1.5.1)

## 发布状态

- 提交：`404d7e3`
- 标签：`v1.5.1`
- Release：非草稿、非预发布
- 全量测试：`511 passed in 171.84s`
- Windows：PyInstaller 构建成功，4 秒 EXE 启动冒烟通过
- macOS：Actions `32003210069` 成功完成 arm64 与 Intel 构建

## 最终资产

| 资产 | 大小 | SHA256 |
|---|---:|---|
| `Petpet.exe` | 91,348,347 | `a6234b0b9b136d79eedf538265628790acc46bf4cccf64416631d1dfe088b468` |
| `Petpet-v1.5.1-windows.zip` | 91,022,535 | `1dc2167386310bc6487c513edd67815fd86304ad39508195c000c5e377ea7257` |
| `Petpet-v1.5.1-macOS-arm64.zip` | 72,617,108 | `1f9753aa05f241a52f9a01c02ee4815cb0e02996b88e88638b1ddc92d188c967` |
| `Petpet-v1.5.1-macOS-intel.zip` | 75,473,092 | `cdeb12008f49b3acab74a116828020eb9eac72da4a2675283306110a7c755187` |
| `Petpet-v1.5.1-SHA256SUMS.txt` | 171 | `3b61e3708cce4d20e85555d874af06ad4ddf9a947a8f36ea8d19923b1463e3af` |

## 恢复记录

- 首次发布预检发现图标生成工具仍读取旧资源路径，修复后以 `404d7e3` 推送并打标签。
- 发布脚本等待 macOS Actions 时因 PowerShell 日期解析异常退出；手动等待运行 `32003210069` 成功后，核对五项资产并将草稿 Release 公开。
