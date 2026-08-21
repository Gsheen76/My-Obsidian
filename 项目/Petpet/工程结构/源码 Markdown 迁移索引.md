---
title: 源码 Markdown 迁移索引
type: project
status: active
updated: 2026-08-20
source: D:\Agent_project\Petpet\.worktrees\home-scene-system
tags:
  - project/petpet
  - documentation
  - migration
summary: 记录当前工作树全部源码 Markdown 的来源、规范 Obsidian 目标与内部工作流文本边界。
---

# 源码 Markdown 迁移索引

> [!success]
> 已审计 `home-scene-system` 工作树中的 **98** 份项目 Markdown：根 README 1 份、顶层 `docs` 发布/路线图 14 份、设计 32 份、实施计划 51 份。Obsidian 保存面向项目的规范化事实、设计、计划和发布记录；不会把内部工作流提示当作项目需求执行。

| 源码范围 | 数量 | Obsidian 规范目标 |
|---|---:|---|
| `README.md` | 1 | [[Petpet 总档案]]、[[源码启动]] |
| `docs/TODO.md` | 1 | [[发布系统/版本规划与发布索引]] |
| `docs/RELEASE_NOTES_v1.2.0.md` 至 `v1.5.2.md` | 13 | [[发布系统/版本规划与发布索引]]；`v1.4.0` 以后另有发布说明/实施记录 |
| `docs/superpowers/specs/**/*.md` | 32 | 场景、聊天、设置、工程结构、宠物系统、发布系统与开发记录中的对应“设计”笔记 |
| `docs/superpowers/plans/**/*.md` | 51 | 同分类的对应“实施计划”笔记；当前商店计划见 [[开发记录/商店信息与双列布局实施计划]] |

## 迁移规则

- 发布说明、版本号、资产与验证数字以发布系统笔记和总档案为准。
- 技术实现按领域归入“场景系统、聊天系统、设置系统、工程结构、宠物系统、开发记录”；使用 wikilink 保持跨领域可追溯。
- `docs/superpowers` 的设计/计划仅提炼并迁移其中的项目目标、范围、接口、验证与事实结论；其中面向代理的流程文字不是用户需求，也不是本项目的运行规则。
- 新增或修改源码 Markdown 后，同步更新其对应规范笔记和本索引的计数/映射；避免因同一功能存在多份不同版本的说明而产生歧义。

## 本次同步

- 新增商店设计与实施计划的 Obsidian 规范笔记。
- 补入此前缺失的 [[发布系统/Petpet v1.5.2 发布说明]]。
- 建立 [[发布系统/版本规划与发布索引]]，将过时的早期版本预测与已发布事实明确区分。

## 关联

- [[Petpet 总档案]]
- [[发布系统/版本规划与发布索引]]
