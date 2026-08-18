---
title: GLM-4.7-Flash 免费兜底实施计划
updated: 2026-08-13
tags:
  - Petpet
  - 聊天系统
  - Cloudflare
  - GLM
type: project
summary: 记录 GLM-4.7-Flash 免费兜底实施计划 的实现步骤与验证安排。
---

# GLM-4.7-Flash 免费兜底实施计划

## 目标

- 宠物名称最多 6 个字符。
- 默认聊天仍优先使用 OpenRouter 免费池。
- OpenRouter 失败后，由 Cloudflare Worker 使用智谱官方 `glm-4.7-flash` 免费接口兜底。

## 安全约束

> [!warning]
> `ZHIPU_API_KEY` 只存放在 Cloudflare Secret 中，不写入源码、Git、配置示例、测试数据或日志。

## 请求顺序

1. 客户端请求 Petpet Worker。
2. Worker 校验请求与每日额度。
3. Worker 请求 OpenRouter 免费池。
4. OpenRouter 上游失败时请求智谱官方 `glm-4.7-flash`。
5. 两个上游都失败时返回统一的 `default_provider_unavailable`。

## 部署命令

```powershell
npx wrangler secret put ZHIPU_API_KEY
npx wrangler deploy
```

Secret 的实际值不写入本笔记。

## 部署结果

> [!success] 2026-08-13 已部署
> Worker 版本 ID：`fc223214-eafe-4814-a28f-e3a3e60a665c`。

- Secret 名称检查确认 `OPENROUTER_API_KEY` 与 `ZHIPU_API_KEY` 均已配置；未读取或输出 Secret 内容。
- 线上无隐私消息返回 `200 text/event-stream`，本次由 OpenRouter 免费池正常响应。
- 无效请求仍返回 `400`。
- 智谱兜底分支通过 Worker 契约测试覆盖；未通过删除或篡改线上 OpenRouter Secret 强制触发。
- Python 全量测试：`437 passed`；Worker 测试：`15 passed`。

## 2026-08-13 桌面连接超时修复

> [!bug] 根因
> Worker 与模型服务正常，桌面客户端失败发生在连接 Worker 之前。对比验证显示：Python 经系统代理约 1.72 秒成功，直连在 6 秒后 `ConnectTimeout`；此前的双次重试会把等待时间扩大到约 22 秒。

- Worker 请求显式读取 Windows/环境系统代理，并传给 `requests`。
- 连接超时固定最多 6 秒，正文读取仍沿用聊天超时；移除重复的长连接重试。
- 修复请求尚未建立时 `response.close()` 访问空对象的问题。
- 使用 Petpet 自身聊天代码发送无历史、无隐私消息验证：1.94 秒完成，收到 44 字符回复。
