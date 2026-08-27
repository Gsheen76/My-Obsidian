---
title: Petpet v1.6.1 发布实施记录
type: release-record
version: v1.6.1
date: 2026-08-27
tags:
  - project/petpet
  - release
---

# Petpet v1.6.1 发布实施记录

## 发布结果

- **发布提交**：`a1c49118e4e31eb9dc0865ef40fde39dd3231986`，远端 `main` 与标签 `v1.6.1` 一致。
- **Release**：[v1.6.1](https://github.com/Gsheen76/Petpet/releases/tag/v1.6.1) 已公开并标记 latest。
- **全量测试**：`659 passed in ~125s`（offscreen），脚本内 pytest、py_compile、`git diff --check` 全部通过。
- **Windows 构建**：PyInstaller 成功，`dist/Petpet.exe` 冒烟通过；SHA256 与官方校验和一致。
- **macOS 构建**：Actions run `33033968459`（arm64 单架构，1m13s）成功上传。

## 资产清单（SHA256）

| 资产 | 大小 | SHA256 |
|---|---:|---|
| `Petpet.exe` | 144,264,652 B | `57a4f7d6a7695e611f68c6c7310afa57ef861a38b98d0576aee52dab8eb3b8e9` |
| `Petpet-v1.6.1-windows.zip` | 143,846,116 B | `ae84bebb77f69d871b01c101cf1463ebd3b09131a756e6154f928b5dabfd00e3` |
| `Petpet-v1.6.1-macOS-arm64.zip` | 113,007,129 B | （远端下载核对中） |
| `Petpet-v1.6.1-SHA256SUMS.txt` | 171 B | — |

注意：校验和文件只包含 Windows 两项资产（沿用既有 release.ps1 行为）。

## 停发 macOS-intel

- `.github/workflows/build-macos.yml` 矩阵删除 `macos-15-intel`，仅保留 arm64。
- `scripts/release.ps1` 必需资产减为三项。
- `updater.py`：darwin 平台遇跨架构资产由降分改为直接返回 None，Intel Mac 更新器将得到 "unsupported / 无适用安装包" 的中性提示，不会误装 arm64 包。
- README 与发布说明声明 Intel 用户留用 `v1.6.0` 及更早版本。

## 过程问题与处置

| 阶段 | 问题 | 处置 |
|---|---|---|
| git diff --check | HANDOFF.md 有 4 行行尾空格被拦截 | trim 后单独提交 |
| 冒烟测试 | 首次失败：源码版宠物（pythonw pet.py）持有单实例锁，新 exe 启动即"唤醒已有实例"退出（exit 0）误判为崩溃 | 按流程停掉源码实例后重跑通过 |
| preflight 清洁检查 | 构建脚本重新生成 tracked icon PNG 字节非确定，污染工作树 | 构建产物不影响推送内容，`git checkout -- assets/runtime/icons/` 还原后重跑 |
| 推送 | `git push --atomic` 网络重置（curl 55 Recv failure），远端无变化，本地 tag 已按设计回滚 | 手动重建 annotated tag 并带重试推送，一次成功 |
| 时间戳解析 | 脚本监听 Actions 时 `[DateTimeOffset]::Parse` 因 PS 文化区域设置抛异常（与 v1.5.0 同一已知坑） | 工作流实际已触发且成功；用 gh CLI 直接确认 run 与资产后手动执行终验步骤 |
| 公开 Release | 因上条未走完脚本收尾 | 手动 `gh release edit --draft=false --latest` + 校验 remote refs 三点一致（main/tag/HEAD 均 a1c4911） |

## 结论

- v1.6.1 为首个三资产版本（Win EXE + Win ZIP + macOS arm64 ZIP）。
- 本机曾通过凭据管理器令牌认证；系统无全局 gh，采用便携版 `.tools/gh/`（gitignore 内）。
- 本地环境恢复：源码版宠物已停止（冒烟所需），用户可随时 `pythonw.exe pet.py` 重启。

## 关联

- [[Petpet v1.6.1 发布说明]]
- [[Petpet v1.6.0 发布实施记录]]
- [[版本规划与发布索引]]
