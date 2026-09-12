---
title: Petpet v1.7.2 发布说明
type: project
tags:
  - project/petpet
  - release
  - v1.7.2
summary: v1.7.2 公开发布（2026-09-12）：长期记忆档案+主动搭话、全景装修+家具扩充、存档备份还原、开机自启动、聊天停止/重新生成、按键反馈全应用统一。
status: active
source: D:\Agent_project\Petpet
updated: 2026-09-12
---

# Petpet v1.7.2 发布说明

> [!summary] Summary
> GitHub `published_at` 2026-09-11T17:19:57Z（本地 09-12 凌晨），tag `v1.7.2` @ `b2cb47d`，四资产（exe/zip/macOS arm64/SHA256SUMS，远端校验和与本地逐字节一致），发布时测试基准 **807 passed**，标题「Petpet v1.7.2」。

完整亮点见仓库 `docs/RELEASE_NOTES_v1.7.2.md`。要点：

- **长期记忆档案 + 主动搭话**：六栏档案自动抽取、聊天窗「档案」查看/编辑；空闲台词档案化（称呼/喜欢/作息/重要的事）。
- **家园全景装修 + 家具扩充重制**：整间一屏铺满不再平移、分栏四类；四件新家具 + 旧四件统一重制；小屋恢复置顶。
- **存档备份/还原 + 开机自启动**：设置页一键备份、导出、从备份恢复（安全快照+自动重启）；HKCU Run 自启开关。
- **聊天停止/重新生成**：发送键流式变「停止」保留已收部分；「↻」重生成上一条。
- **按键反馈与滚动条全应用统一**；修复 API Key 按住显示不恢复密文、依赖清单缺 Pillow/numpy 等隐藏问题；CI 按 runtime.txt 安装。

## 发布过程记录（本版特有）

1. **发版顺序变更**：用户指示「先完成B再发布」——首次流水线中途叫停，Draft release/远端与本地 tag/半成品 zip 全部清理重来。
2. **便携 gh 复活**：`.tools/gh/bin/gh.exe`（2.62.0）其实一直在（之前 find 深度不足误判丢失）；token 走 `git credential fill` → `GH_TOKEN`。
3. **TLS 抖动两次打断脚本**（上传后校验远端 tag / 重跑 preflight）——剩余步骤手动补完（与脚本尾一致）：查资产 → `gh workflow run build-macos.yml -f release_tag/dispatch_id` → watch → `gh release edit --draft=false --latest`。**网络抖动时别整跑脚本（每次重做测试+构建），按脚本尾段手动接力。**
4. 版本号规则定稿入长期记忆：无大更新 → patch。
