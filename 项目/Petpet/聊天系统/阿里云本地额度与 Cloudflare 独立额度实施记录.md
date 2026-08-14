---
title: 阿里云本地额度与 Cloudflare 独立额度实施记录
date: 2026-08-14
tags:
  - Petpet
  - 聊天系统
  - 实施记录
status: ready-to-deploy
---

# 阿里云本地额度与 Cloudflare 独立额度实施记录

> [!success] 本地实现完成
> 阿里云不再访问 Cloudflare。阿里云额度由桌面客户端本地记录每天 20 次，Cloudflare 保持 Durable Object 独立每天 20 次。

## 已完成

- `buddy_ai.py` 新增 `DATA_DIR/chat_quota_state.json` 本地账本。
- 按北京时间自然日自动重置阿里云额度。
- 阿里云 HTTP 200 才计数；连接失败和 HTTP 错误不扣本地次数。
- 同一个 `request_id` 只记录一次。
- 阿里云本地 20 次用完后跳过阿里云，直接尝试 Cloudflare。
- 阿里云函数删除 `QUOTA_ENDPOINT`、`QUOTA_SHARED_SECRET` 和跨境额度请求。
- 阿里云函数校验请求后直接调用 `glm-4.7-flash` 并转发 SSE。
- `config.json.example` 的主入口已设为 `https://petpet-yun-chat-zqblnbrnfs.cn-hangzhou.fcapp.run/v1/chat`。

## 部署包

- 文件：`D:\Agent_project\Petpet\.worktrees\home-scene-system\aliyun-chat\dist\petpet-aliyun-chat-root.zip`
- ZIP 根目录：`server.js`、`package.json`
- SHA-256：`733BD39AAEE1799AEB9DDDE5A71D4F8C3E47C661E86C996AE26DA91CF3F4096A`
- 启动命令：`/var/fc/lang/nodejs20/bin/node server.js`
- 监听端口：`9000`

## 验证

- Python 聊天 focused：`97 passed`
- Python 全量：`450 passed in 28.42s`
- 阿里云 Node：`5 passed`
- Cloudflare Worker：`21 passed`
- `python -m py_compile buddy_ai.py`：通过
- `git diff --check`：通过，仅有 Git 的 LF→CRLF 提示，没有空白错误

## 阿里云部署操作

1. 上传新的 `petpet-aliyun-chat-root.zip` 并部署。
2. 保留 `ZHIPU_API_KEY`、`ZHIPU_MODEL=glm-4.7-flash` 与 `PORT=9000`。
3. 删除不再使用的 `QUOTA_ENDPOINT` 和 `QUOTA_SHARED_SECRET`。
4. 发送一条测试消息，日志应出现 `zhipu_response`，不应再出现 `quota_response` 或 `quota_exception`。

> [!note]
> 本轮没有创建 Git 提交、推送或发布版本，也没有把任何 API Key 或 Secret 写入源码、配置示例或笔记。

## 关联文档

- [[阿里云本地额度与 Cloudflare 独立额度设计]]
- [[阿里云本地额度与 Cloudflare 独立额度实施计划]]
- [[阿里云优先与统一免费额度设计]]：已被本方案取代的旧额度架构。
- [[Petpet 总档案]]

