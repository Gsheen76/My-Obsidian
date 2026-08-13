---
title: GLM-4.7-Flash 免费兜底实施计划
date: 2026-08-13
tags:
  - Petpet
  - 聊天系统
  - Cloudflare
  - GLM
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
