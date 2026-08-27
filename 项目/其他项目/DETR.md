---
tags:
  - 项目
  - 目标检测
  - Transformer
title: DETR
type: project
summary: 记录项目的定位、实现结构、当前状态和后续工作。
updated: 2026-08-05
migrated: 2026-08-05
---

> [!summary] Summary
> 记录项目的定位、实现结构、当前状态和后续工作。

# DETR

$$
\renewcommand{\arraystretch}{1.1}
\begin{array}{c c c c c c c c c c c}
\hline
\textbf{Config} & \textbf{L} & \textbf{Q} & \textbf{mAP} & \textbf{AP50} & \textbf{AP75} & \textbf{AP}_{\text{small}} & \textbf{AP}_{\text{large}} & \textbf{↓ runtime} & \textbf{Memory} \\
\hline
\text{Baseline}    & 6 & 100 & \mathbf{39.89\%} & \mathbf{59.60\%} & \mathbf{42.20\%} & 19.05\%  & \mathbf{58.63\%} & -        & 21.2\,\text{GB} \\
\text{Balanced}    & 4 & 100 & 39.40\% & 59.35\% & 41.16\% & \mathbf{19.41\%} & 58.56\% & \downarrow 13.3\% & 18.3\,\text{GB} \\
\text{Lite} & 4 & 50  & 37.24\% & 56.29\% & 39.33\% & 16.60\% & 55.17\% & \downarrow 26.7\% & 16.4\,\text{GB} \\
\hline
\end{array}
$$

## 关键概念

- 项目、目标检测、Transformer

## 关联笔记

- [[../../笔记/知识库/知识库索引]]

## 规划

- [ ] 补充或更新本笔记中的结果、限制与下一步工作。
