---
title: Petpet v1.4.1 发布实施计划
date: 2026-08-13
tags:
  - Petpet
  - 发布
  - v1-4-1
status: completed
---

# Petpet v1.4.1 发布实施计划

> [!abstract]
> 将聊天、知识库、暖色聊天 UI、设置和教程改版作为 `v1.4.1` 发布，同时完成可重复执行的一键发布脚本。

## 实施顺序

1. 测试先行更新版本、README、发布说明和本地文件排除规则。
2. 保留“文静 / 适中 / 活泼”文案，并验证旧设置会映射到真正最近的三档预设。
3. 测试先行新增 `scripts/release.ps1`，覆盖预检、验证、Windows 构建、Git 同步、草稿 Release、macOS 工作流及四资产公开闸门。
4. 将 macOS 上传改为可恢复：同名资产存在时跳过，不盲目覆盖。
5. 运行 focused tests、全量 `pytest -q`、Python 编译、差异检查、Windows 构建和 EXE 冒烟。
6. 创建发布提交，在干净工作树中运行：

```powershell
.\scripts\release.ps1 -Version 1.4.1
```

7. 独立核对 `origin/main`、标签、Release 状态、四项资产、下载地址和 SHA-256。
8. 将不可变发布证据补入实施记录和 [[Petpet 总档案]]。

## 安全边界

- 不提交两张调试截图、`.wrangler` 缓存、用户数据或 API Key。
- 不执行 reset、checkout、强推、标签覆盖或 worktree 删除。
- 任一阶段失败即停止，Release 保持草稿并允许同一命令恢复。

## 关联

- [[Petpet v1.4.1 一键发布设计]]
- [[Petpet v1.4.1 发布说明]]
- [[Petpet 总档案]]
