---
title: Petpet v1.6.0 发布实施记录
type: release-log
status: completed
version: v1.6.0
date: 2026-08-22
tags:
  - project/petpet
  - release
  - verification
---

# Petpet v1.6.0 发布实施记录

> [!success] 发布结果
> GitHub Release 已从草稿公开为 [v1.6.0](https://github.com/Gsheen76/Petpet/releases/tag/v1.6.0)，`main` 与标签均指向 `0d40e042f10bbe859d3c080fa50dcbde29d2e3d8`。

## 验证证据

- 全量测试：`645 passed in 126.88s`（发布脚本门禁）。
- `python -m py_compile`：通过。
- `git diff --check`：通过；发布前清理了历史文档末尾多余空白，提交为 `0d40e04`。
- Windows PyInstaller 构建：通过。
- Windows `Petpet.exe` 隐藏启动冒烟：通过。
- macOS Actions：成功，运行号 [32565704675](https://github.com/Gsheen76/Petpet/actions/runs/32565704675)，arm64 与 Intel 均完成上传。

## 发布资产

| 资产 | 大小 | SHA256 |
|---|---:|---|
| `Petpet.exe` | 113,238,440 bytes | `A0D1AAA52AC4583AC426616193D8F53D41DF85A9F518A4B59111B441D586F17B` |
| `Petpet-v1.6.0-windows.zip` | 112,940,020 bytes | `8DAE7AE815A46CB6A9A065D7C71AD5F28217F7FF4CEEB023C02FEA8D89227347` |
| `Petpet-v1.6.0-macOS-arm64.zip` | 94,681,018 bytes | `8EE58CBB1983831DC340A293DE753C1B4A6F58BEDA002D7B31B32E2F1B1EE555` |
| `Petpet-v1.6.0-macOS-intel.zip` | 97,539,286 bytes | `D9F3126F2AC415BE72EB15904E7DB23A6659A0A81C14CA5F11798125CDA6310B` |

发布校验和文件仅包含 Windows 两项哈希；macOS 资产哈希由发布脚本从 Actions 资产下载后核验。

## 过程记录与恢复点

- 发布分支：`codex/release-v1.6.0`，最终提交 `0d40e04`。
- 发布脚本：`scripts/release.ps1 -Version 1.6.0`；不强推、不覆盖已有资产，失败时保留草稿。
- 构建期间发现源码单实例仍在运行，已停止精确匹配的旧源码进程 PID `33344` 后重新完成冒烟；未停止其他 Python 进程。
- 构建自动改写的 8 个图标已恢复，未把构建副作用带入发布提交。
- 回滚：如需撤回，可在 GitHub Release 页面取消公开并保留标签；源码回退应以 `0d40e04` 之前的 `5100577` 为审阅起点，不直接强推。

关联记录：[[Petpet v1.6.0 发布说明]]、[[版本规划与发布索引]]。
