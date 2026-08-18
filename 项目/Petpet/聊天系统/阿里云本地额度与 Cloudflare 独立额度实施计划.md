---
title: 阿里云本地额度与 Cloudflare 独立额度实施计划
updated: 2026-08-14
tags:
  - Petpet
  - 聊天系统
  - 实施计划
status: ready-to-deploy
type: project
summary: 记录 阿里云本地额度与 Cloudflare 独立额度实施计划 的实现步骤与验证安排。
---

# 阿里云本地额度与 Cloudflare 独立额度实施计划

> [!info] 目标
> 阿里云由桌面客户端本地记录每天 20 次；Cloudflare 保持云端独立每天 20 次。阿里云函数不再访问 Cloudflare。

## 实施顺序

- [x] 在 `DATA_DIR/chat_quota_state.json` 建立北京时间本地额度账本。
- [x] 测试损坏恢复、跨日重置、20 次上限和 `request_id` 幂等。
- [x] 将账本接入阿里云优先、Cloudflare 兜底路由。
- [x] 阿里云 HTTP 200 才扣次数；连接失败不扣，额度耗尽直接切 Cloudflare。
- [x] 删除阿里云函数的 `QUOTA_ENDPOINT` 和 `QUOTA_SHARED_SECRET` 依赖。
- [x] 重建根目录部署 ZIP 并检查内容和 SHA-256。
- [x] 将公开配置的阿里云主入口更新为 `https://petpet-yun-chat-zqblnbrnfs.cn-hangzhou.fcapp.run/v1/chat`。
- [x] 运行 Python focused/full、阿里云 Node 和 Cloudflare Worker 全部测试。
- [ ] 上传阿里云 ZIP，确认日志只出现智谱请求，不再出现额度跨境请求。
- [x] 更新 [[Petpet 总档案]] 与实施记录。

## 约束

- 不新增依赖。
- 不记录聊天正文、IP 或密钥。
- 不覆盖其他未提交改动。
- 不提交、不推送、不发布版本。

## 关联文档

- [[阿里云本地额度与 Cloudflare 独立额度设计]]
- [[阿里云优先与统一免费额度设计]]
