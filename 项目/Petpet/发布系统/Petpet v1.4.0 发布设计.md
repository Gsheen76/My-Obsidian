---
title: Petpet v1.4.0 发布设计
updated: 2026-08-11
tags:
  - Petpet
  - 发布
  - v1-4-0
status: completed
type: project
summary: 记录 Petpet v1.4.0 发布设计 的设计目标、方案和约束。
---

# Petpet v1.4.0 发布设计

> [!abstract]
> 将当前家园系统、家具装修、快捷菜单和小屋宠物行为作为 `v1.4.0` 发布。Windows 与 macOS 双架构四个资产全部验证后，再一次性公开 GitHub Release。

## 发布内容

- `version.py` 唯一版本更新为 `1.4.0`。
- README 更新当前版本、`v1.4.0` 亮点、实际菜单入口和项目结构。
- 新增 `docs/RELEASE_NOTES_v1.4.0.md`。
- 重点记录快捷菜单、家场景、家具装修、2.5D 四向移动、脚印寻路、正坐待机、对话和 3 FPS 睡眠动画。

## 正式资产

1. `Petpet.exe`
2. `Petpet-v1.4.0-windows.zip`
3. `Petpet-v1.4.0-macOS-arm64.zip`
4. `Petpet-v1.4.0-macOS-intel.zip`

> [!warning]
> 先建立草稿 Release。四个资产全部上传并验证文件名、大小与下载状态后才公开；任何测试、构建、工作流或推送失败都会停止发布，不使用强制推送。

## Git 与构建

- 当前工作区：`D:\Agent_project\Petpet\.worktrees\home-scene-system`
- 当前分支：`codex/home-scene-system`
- 发布提交快进推送到 `origin/main`，不切换或回退当前 worktree。
- 标签：`v1.4.0`
- Windows 在当前 worktree 本地构建；macOS Intel/arm64 使用 GitHub Actions 的 `Build macOS app`。

## 验证闸门

- 版本元数据先写失败测试，再更新生产文件。
- 全量 `pytest -q`。
- `py_compile` 与 `git diff --check`。
- Windows EXE 隐藏启动冒烟与 EXE/ZIP SHA-256。
- macOS 双架构工作流成功且两个 ZIP 非空。
- Release 公开后通过 GitHub API 核对标签、状态、四项资产和下载 URL。

## 相关记录

- [[小屋睡眠动画接入设计]]
- [[小屋睡眠动画接入实施计划]]

## 发布故障回退

> [!warning]
> 本机已成功上传两个 Windows 资产，但向 `uploads.github.com` 发送 macOS ZIP 时，PowerShell `Invoke-RestMethod` 两次、`.NET HttpClient` 一次均发生连接中断。草稿保持私有且没有残缺 Mac 资产。

经确认后改用 GitHub Actions 服务器端上传：工作流从 `main` 启动，源码明确 checkout `v1.4.0` 标签；Intel/arm64 Runner 构建后使用 `gh release upload` 向现有草稿上传各自 ZIP。工作流不使用 `--clobber`，标签仍固定在 `9c5a6ad`。
