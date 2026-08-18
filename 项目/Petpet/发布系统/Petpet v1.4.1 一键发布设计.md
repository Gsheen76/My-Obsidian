---
title: Petpet v1.4.1 一键发布设计
updated: 2026-08-13
tags:
  - Petpet
  - 发布
  - v1-4-1
status: completed
type: project
summary: 记录 Petpet v1.4.1 一键发布设计 的设计目标、方案和约束。
---

# Petpet v1.4.1 一键发布设计

> [!abstract]
> 将当前聊天、免费代理、游戏知识库、聊天 UI、设置和教程等功能作为 `v1.4.1` 发布，并把 v1.4.0 已验证的双平台发布流程封装成安全的一键 PowerShell 命令。

## 采用方案

未来版本使用：

```powershell
.\scripts\release.ps1 -Version 1.4.2
```

脚本采用混合式发布：本机测试并构建 Windows，GitHub Actions 构建 macOS Intel 与 Apple Silicon。先创建草稿 Release，四项正式资产全部上传并核验后才公开。

## 发布范围

- 包含当前工作树中除本地调试截图外的全部已确认功能。
- 更新版本、README、发布说明、知识库、Cloudflare Worker、测试与功能文档。
- `debug-chat-window.png` 和 `debug-pet-menu.png` 加入 `.gitignore`，不进入版本。
- 发布提交安全同步到 `origin/main`；标签、Release 与 `main` 指向同一个提交。

## 安全闸门

1. 检查版本、发布说明、干净工作树、GitHub 登录和远端状态。
2. 运行全量测试、Python 编译和 `git diff --check`。
3. 构建并冒烟验证 Windows EXE，生成 Windows ZIP 和 SHA-256。
4. 非强制推送发布提交到 `origin/main`，创建注释标签。
5. 创建草稿 Release 并上传 Windows 资产。
6. 触发并等待 macOS 双架构工作流。
7. 四项资产均存在、非空且 uploaded 后公开 Release。
8. 公开后再次核对标签、状态、下载 URL 和资产信息。

> [!warning]
> 任一环节失败即停止，Release 保持草稿。脚本不会执行 `git reset`、`git checkout`、强推、覆盖标签或删除 worktree。

## 重复运行与恢复

- 远端标签只有在已指向同一发布提交时才接受。
- 已存在的 Release 和资产先核对，不盲目覆盖。
- 已完成的 macOS 工作流不重复触发。
- 发布中断后使用同一命令继续；已完整公开时仅重新验证。

## 正式资产

1. `Petpet.exe`
2. `Petpet-v1.4.1-windows.zip`
3. `Petpet-v1.4.1-macOS-arm64.zip`
4. `Petpet-v1.4.1-macOS-intel.zip`

另附 SHA-256 校验清单。

## 测试与记录

发布脚本和版本元数据按测试先行实现。发布前重新运行 focused tests、全量 `pytest -q`、Windows 构建和启动冒烟；发布后将提交、工作流、哈希与 Release URL 写入实施记录及 [[Petpet 总档案]]。

项目内完整技术设计：`docs/superpowers/specs/2026-08-13-v1.4.1-one-click-release-design.md`。
