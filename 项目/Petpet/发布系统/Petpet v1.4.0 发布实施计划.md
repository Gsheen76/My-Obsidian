---
title: Petpet v1.4.0 发布实施计划
date: 2026-08-11
tags:
  - Petpet
  - 发布
  - v1-4-0
status: completed
---

# Petpet v1.4.0 发布实施计划

> [!info]
> 对应源码计划：`docs/superpowers/plans/2026-08-11-v1.4.0-release-plan.md`。采用当前会话内联执行；任何测试、非快进推送、构建、工作流或资产核验失败都会阻止 Release 公开。

## Task 1：版本与文档 TDD

- [x] 修改 `tests/test_release_metadata.py` 期待 `1.4.0`。
- [x] 运行 RED：2 项按预期因生产版本仍为 `1.3.2` 失败。
- [x] 更新 `version.py`、README，创建 `RELEASE_NOTES_v1.4.0.md`。
- [x] 运行 GREEN：`5 passed`，并人工核对 README 新亮点和正确小屋入口。

## Task 2：发布提交

- [x] 全量验证：`304 passed in 43.52s`；`py_compile` 与 `git diff --check` 通过。
- [x] 检查状态和敏感文件，未包含用户数据或密钥。
- [x] 创建 `release: Petpet v1.4.0` 提交：`9c5a6ad`。

## Task 3：Windows 资产

- [x] 本地构建 `Petpet.exe`：87,578,028 bytes。
- [x] 创建 `Petpet-v1.4.0-windows.zip`：87,296,476 bytes，内含 EXE 与 README。
- [x] 隐藏启动冒烟成功；EXE SHA-256 `5882F4A20A0991163B6C9F1526152074871D254A38CF473EA36C464A4BF721A5`，ZIP SHA-256 `F8F09C244CBB0FC857E61C248ED9E588F8203DB602509C932F7E178058C81C7E`。

## Task 4：远端与 macOS

- [x] 确认 `origin/main` 可快进，发布提交已推送，`HEAD...origin/main = 0/0`。
- [x] 创建并推送注释标签 `v1.4.0`，标签对象 `c435c631c3945985ccc9c926d49fc47a2ca3d31c`。
- [x] 在标签上触发 macOS Intel/arm64 工作流：run `31452188476`，两个任务均 success。
- [x] 下载两个 artifact：arm64 72,436,036 bytes / `B36D6CE2C19709E41D73525E7BB4584C52F04E53C4D80F32D32A847FF`；Intel 75,271,108 bytes / `A09787AF8468B74516D0BB228D6B5827939EA5895F7639D1FAE19D6783050A87`。

## Task 5：GitHub Release

- [x] 创建 `Petpet v1.4.0` 草稿 Release，ID `368300784`，保持私有。
- [x] 上传并验证 EXE、Windows ZIP；Mac 本地上传连续三次断链且未留下残缺资产。
- [x] 通过标签检出的 GitHub Actions run `31454263313` 上传 macOS arm64 ZIP、macOS Intel ZIP。
- [x] 四项资产全部为 uploaded 且非零后公开。
- [x] 通过公共 API 重新核对标签、状态、资产和下载 URL。

## Task 6：记录收口

- [x] 创建 [[Petpet v1.4.0 发布实施记录]]。
- [x] 将 [[Petpet 总档案]] 切换为正式 `v1.4.0` 状态。
- [x] 记录测试数、提交、工作流、资产哈希和 Release URL。

## 关联

- [[Petpet v1.4.0 发布设计]]
- [[Petpet 总档案]]
- [[场景系统/家场景装修编辑器交互记录]]
- [[菜单系统/宠物快捷菜单交互记录]]
