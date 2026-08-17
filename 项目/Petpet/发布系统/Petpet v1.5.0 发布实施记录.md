---
title: Petpet v1.5.0 发布实施记录
date: 2026-08-14
version: v1.5.0
status: published
tags:
  - project/petpet
  - release
  - verification
---

# Petpet v1.5.0 发布实施记录

> [!success]
> `v1.5.0` 已公开：[GitHub Release](https://github.com/Gsheen76/Petpet/releases/tag/v1.5.0)

## 发布状态

- 提交：`a6545343e86c9859179c106c7488033d67ee5460`
- 标签：`v1.5.0`
- Release：非草稿、非预发布
- 全量测试：`457 passed in 27.32s`
- Windows：PyInstaller 构建成功，隐藏窗口启动冒烟通过
- macOS：Actions `31800821250` 成功完成 arm64 与 Intel 构建

## 最终资产

| 资产 | 大小 | SHA256 |
|---|---:|---|
| `Petpet.exe` | 91,970,942 | `24680cde991bd3da88a8903f2e7517e6dc4bd6aa58217952fcee59651ba7031f` |
| `Petpet-v1.5.0-windows.zip` | 91,649,260 | `8215ad1c0c202c791e85bd66bf9ef2ca932954f4c8dbd444b666be6038a51492` |
| `Petpet-v1.5.0-macOS-arm64.zip` | 73,242,845 | `3889a4e33956765c29ce883641411af441f3fd1973c46546c47e14a04f50ea7a` |
| `Petpet-v1.5.0-macOS-intel.zip` | 76,096,241 | `c1f8e397bd61477e78d7003dd5f0fc9bc72bc268e71fff0ca8072289f8015880` |
| `Petpet-v1.5.0-SHA256SUMS.txt` | 171 | `5d31e9010e97624b6ec0faa5e785a1f961ad3e03756eedfeb8559d9d793a9032` |

## 恢复记录

- 首次闸门发现知识库与发布测试仍锁定 `v1.4.1`，并发现测试读取玩家本地调参文件；修正后测试隔离到临时用户目录。
- 构建脚本原先每次强制联网安装依赖；改为本地依赖完整时直接复用。
- macOS 工作流成功上传资产后，PowerShell 5.1 日期解析使脚本保留草稿。
- 恢复运行时 PyInstaller 重建产物哈希不同，因此未覆盖首次已冒烟资产；最终重新核对远端 main/tag、五项资产状态、下载内容和 SHA256 后公开。

## 关联

- [[Petpet v1.5.0 发布说明]]
- [[../Petpet 总档案|Petpet 总档案]]
