---
tags:
  - 工具
  - 机器学习
title: OpenBayes操作
type: note
summary: 记录在 OpenBayes 上上传数据和运行机器学习任务的操作步骤。
updated: 2026-08-05
migrated: 2026-08-05
---

> [!summary] Summary
> 记录在 OpenBayes 上上传数据和运行机器学习任务的操作步骤。

# 1. bayes上传数据
#### （1）创建新的数据集

```
bayes data create 数据集名字
```

#### （2）创建一个空的数据集版本 

```
bayes data new-version 数据集ID
```

#### （3） 通过命令行直接上传文件夹

```
bayes data upload 数据集ID -v 版本号 -p 数据集路径
```

## 关键概念

- 工具、机器学习

## 关联笔记

- [[../知识库/知识库索引]]
