---
title: Petpet v1.4.0 发布实施记录
date: 2026-08-11
tags:
  - Petpet
  - 发布
  - v1-4-0
status: published
release_url: https://github.com/Gsheen76/Petpet/releases/tag/v1.4.0
---

# Petpet v1.4.0 发布实施记录

> [!success]
> `Petpet v1.4.0` 已于 2026-08-11 11:36（Asia/Shanghai）公开。公共 API 确认 `draft=false`、`prerelease=false`，四项资产均为 `uploaded`。

## Git

- 发布提交：`9c5a6ad33970f849017f6c9566ec45f73e6e24a1`
- 注释标签：`v1.4.0`，标签保持指向发布提交
- macOS 服务器端上传工作流提交：`26f426c5a51a80af915eed5dcf005176936006c3`
- 最终 `HEAD...origin/main`：`0/0`
- 最终源码工作树：clean

## 测试与构建

- 元数据 TDD RED：2 项因生产版本仍为 `1.3.2` 按预期失败
- 元数据 GREEN：`5 passed`
- 发布前全量：`304 passed in 43.52s`
- 发布后最终全量：`304 passed in 37.92s`
- `py_compile`：通过
- `git diff --check`：通过
- Windows EXE 隐藏启动 4 秒保持运行；冒烟产生的 one-file 子进程已按精确路径停止
- 当前 worktree 源码版 PID：`33840`

## Actions

- 首次双架构构建：[run 31452188476](https://github.com/Gsheen76/Petpet/actions/runs/31452188476)，Intel/arm64 均 success
- 本机向 `uploads.github.com` 上传 Mac ZIP 连续三次断链，草稿始终保持私有且无残缺 Mac 资产
- 服务器端发布：[run 31454263313](https://github.com/Gsheen76/Petpet/actions/runs/31454263313)，从 `v1.4.0` 标签检出源码，Intel/arm64 构建与草稿上传均 success

## 最终资产

| 文件 | 大小（bytes） | SHA-256 |
|---|---:|---|
| `Petpet.exe` | 87,578,028 | `5882F4A20A0991163B6C9F1526152074871D254A38CF473EA36C464A4BF721A5` |
| `Petpet-v1.4.0-windows.zip` | 87,296,476 | `F8F09C244CBB0FC857E61C248ED9E588F8203DB602509C932F7E178058C81C7E` |
| `Petpet-v1.4.0-macOS-arm64.zip` | 72,437,326 | `2657B7B24FA8C19141B5A514D522B501E341A18D14E66699231157A1398929B4` |
| `Petpet-v1.4.0-macOS-intel.zip` | 75,270,064 | `5408C0A2C075CE5975D603B0DBED50BDF456E56BC557B35C7A2FE560716D1E96` |

## Release

- [Petpet v1.4.0](https://github.com/Gsheen76/Petpet/releases/tag/v1.4.0)
- Release ID：`368300784`
- 公开时间：`2026-08-11T03:36:15Z`
- 四个下载 URL 均使用正式标签路径 `/releases/download/v1.4.0/`

## 关联

- [[Petpet v1.4.0 发布设计]]
- [[Petpet v1.4.0 发布实施计划]]
- [[Petpet v1.4.0 发布说明]]
- [[Petpet 总档案]]
