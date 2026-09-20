---
tags:
  - 扩散模型
  - 深度学习
  - 论文
  - 多任务学习
title: 论文6：高分辨率图像合成与潜空间扩散模型（LDM）
type: paper
summary: 梳理 LDM 如何用两阶段"感知压缩 + 潜空间扩散"把扩散模型从像素空间搬进潜空间，及其拼接/cross-attention 两种条件注入机制、CFG 引导与各任务实验结论。
updated: 2026-09-20
---

> [!summary] Summary
> 梳理 LDM（Stable Diffusion 底座论文）的两阶段设计：第一阶段自编码器负责感知压缩，第二阶段条件扩散在潜空间负责语义生成；重点拆解 cross-attention 条件注入公式、classifier-free guidance、下采样倍率 f 的消融结论，以及对我课题（多条件 CT/MRI 可控转换）的直接启发。

> [!info]
> [High-Resolution Image Synthesis with Latent Diffusion Models]
> 发表日期：2021-12-20（arXiv v1）；会议版 CVPR 2022
> 会议：IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2022)
> 出版商：IEEE/CVF
> DOI：[10.1109/CVPR52688.2022.01042](https://doi.org/10.1109/CVPR52688.2022.01042)
> 来源：[https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
> 代码：[https://github.com/CompVis/latent-diffusion](https://github.com/CompVis/latent-diffusion)
> 原文 PDF 与全部插图已存：`assets/论文6：高分辨率图像合成与潜空间扩散模型（LDM）/`

# 论文6：高分辨率图像合成与潜空间扩散模型（LDM）

## Abstract 摘要

扩散模型（DM）通过把图像生成过程分解为一系列去噪自编码器的顺序应用，在图像数据上取得了 SOTA 合成结果，且其公式化天然支持不重训练的引导机制（guidance）。但 DM 通常**直接在像素空间**运行：训练强大 DM 往往消耗数百 GPU 天，推理又因顺序的多步评估而昂贵。为在保持质量的同时降低算力门槛，本文方法将**感知压缩**与**语义生成**两个阶段显式解耦：先用自编码器把图像压进潜空间，再在该潜空间训练扩散模型（LDM）。依托cross-attention 条件机制，LDM 可以灵活接入各类条件。LDM 在图像修复和类条件图像合成上取得新 SOTA，在无条件生成、文本到图像、超分辨率上极具竞争力，同时相比像素 DM 大幅降低计算需求。该论文即 Stable Diffusion 的底座论文。

## 1. Introduction 引言

### 1.1 像素空间扩散的两大痛点

- **训练贵**：最强大的像素 DM（如 ADM）训练需要 **150–1000 V100 天**；只有少数机构能负担，且碳足迹巨大。
- **推理贵**：同一网络要顺序执行大量去噪步（25–1000 步），反复在高维 RGB 空间做函数评估。例如 A100 上生成 5 万张图约需 **5 天**。

### 1.2 已有压缩路线的问题

- **GAN**：对抗训练难以扩展到复杂多模态分布，多样性受限。
- **两阶段离散潜空间 + 自回归 Transformer**（VQGAN + DALL·E 路线）：为让 Transformer 消化，需要**激进的空域下采样**（f=16 甚至 64），重建上界被压低，细节失真；且放弃了图像的二维邻域归纳偏置（全靠 attention）。

### 1.3 本文核心观察

数字图像的绝大部分比特对应**感知上不可见的细节**（高频纹理）；语义内容占的自由度其实很低。因此：

$$\text{图像生成} = \underbrace{\text{感知压缩}}_{\text{去掉不可感知的冗余}} + \underbrace{\text{语义生成}}_{\text{对真正的内容建模}}$$

扩散模型对空间数据有**优秀的归纳偏置**（UNet + 2D 卷积），不需要像自回归路线那样激进下采样来迁就架构——只需"适度"压缩（f=4~16）去掉感知冗余即可。既省算力，又不伤重建上界（图 1 证据：f=4 重建 PSNR 27.4 / R-FID 0.58，远好于 DALL·E 所用 f=8 的 22.8/32.01 和 VQGAN f=16 的 19.9/4.98）。

![[fig1-自编码器重建对比.png]]
*图 1：不同下采样倍率下自编码器的重建对比（DIV2K 512²）。轻压缩（f=4）保住重建上界，重压缩（f=16）细节已明显丢失——这是 LDM 选择"适度压缩"的直接证据。*

## 2. Method 方法

### 2.1 整体框架：两阶段解耦

![[fig2-感知与语义压缩.png]]
*图 2：感知压缩与语义压缩的解耦示意。数字图像的大部分比特编码感知细节（左），先用第一阶段自编码器处理；扩散模型只在压缩后的语义空间建模（右）。*

```text
第一阶段（感知压缩，训练后冻结）：
  x ──E──> z = E(x) ∈ R^(h×w×c)     f = H/h = W/w（下采样倍率）
  z ──D──> x̃ = D(E(x))               重建

第二阶段（语义生成）：
  z₀ ──前向加噪──> z_t ──ε_θ(·, t, 条件) 去噪──> ẑ ──D──> x̂
```

关键设计决策：**扩散模型不在像素 x 上训练，而在冻结自编码器的潜变量 z 上训练**。像素级细节由 D 一次性恢复，扩散专注学语义分布。

### 2.2 第一阶段：感知压缩自编码器

**基本结构**：编码器 E 把 $x \in \mathbb{R}^{H \times W \times 3}$ 下采样为 $z = E(x) \in \mathbb{R}^{h \times w \times c}$，下采样倍率 $f = H/h = W/w$，实验 $f \in \{2^m\}$。

**训练损失**：纯 $L_2/L_1$ 重建会使图像过度模糊，因此采用三项联合：

$$\mathcal{L}_{Autoencoder} = \mathcal{L}_{rec} + \lambda_{perceptual}\,\mathcal{L}_{perceptual} + \lambda_{adv}\,\mathcal{L}_{adv} + \lambda_{reg}\,\mathcal{L}_{reg}$$

- $\mathcal{L}_{rec}$：像素重建（$L_1$）；
- $\mathcal{L}_{perceptual}$：感知损失（VGG 特征匹配），约束感知相似而非逐像素相同；
- $\mathcal{L}_{adv}$：PatchGAN 对抗损失，逼出照片级锐度；
- $\mathcal{L}_{reg}$：潜空间正则（见下）。

**两种潜空间正则**（防止潜空间任意高方差、便于扩散建模）：

| 正则 | 机制 | 特点 |
|---|---|---|
| **KL-reg** | 对学习到的潜变量施加轻微 KL 惩罚，拉向标准正态 $\mathcal{N}(0, I)$（类似 VAE） | 连续潜空间；重建略好；可控生成（如 SD 的 KL-8） |
| **VQ-reg** | 在解码器内置一层向量量化（VQ）码本（可理解为"量化层被解码器吸收"的 VQGAN） | 离散码本；论文主实验默认（VQ 版采样质量更好） |

正则强度刻意调小：不追求严格先验，只要潜空间"不过分发逸"——**潜空间略微发散反而对扩散友好**（避免所有样本挤在一条细流形上，让加噪/去噪有施展空间）。

**实验结论（4.1 + 图 5/6）**：

- 压缩率是精度-效率权衡的核心旋钮：**LDM-4/8 处在最优区间**；
- 像素版 LDM-1 与 LDM-8 在 ImageNet 上训练 2M 步后 **FID 差距达 38**；
- 压缩过头（LDM-32+）则第一段重建损失过大，整体质量上限受限；
- VQ 正则的 LDM 采样质量优于 KL 正则（尽管 KL 版重建略好，见补充 Tab. 8）。

![[fig5-下采样倍率消融.png]]
*图 5：ImageNet 类条件 LDM 在不同下采样倍率 f 下的训练曲线（2M 步）。LDM-1（像素级）在同等算力预算下被大幅拉开；f∈[4,16] 是甜点区。*

![[fig6-推理速度与质量权衡.png]]
*图 6：推理速度 vs 样本质量（CelebA-HQ 左 / ImageNet 右）。DDIM 步数 {10,20,50,100,200} 从右往左。LDM-{4-8} 在速度-质量权衡上全面占优。*

### 2.3 第二阶段：潜空间扩散模型

在冻结的潜空间上，沿用 [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文1：去噪扩散概率模型（DDPM）|DDPM]] / [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文2：通过随机微分方程进行基于分数的生成建模|Score-SDE]] 的离散时间扩散框架（对应论文 Sec. 3.4/3.6），训练一个时序条件 UNet $\epsilon_\theta(z_t, t)$ 预测噪声：

$$\mathcal{L}_{LDM} = \mathbb{E}_{\mathcal{E}(x), \epsilon \sim \mathcal{N}(0,1), t}\left[ \left\| \epsilon - \epsilon_\theta(z_t, t) \right\|_2^2 \right]$$

与前作唯一的区别：$x$ 换成 $z = \mathcal{E}(x)$，其余加噪调度、ε-预测目标、采样器（DDIM 为主）全部继承。

**UNet 细节**：

- 主干由 2D 卷积残差块构成，GroupNorm + SiLU；在多个分辨率层级插入 self-attention（继承 ADM 的实践）；
- 时间步 t 经正弦位置嵌入后投影进各残差块（类 Transformer 位置编码）；
- "big" 版（修复实验）：注意力放三层特征层级、用 BigGAN 残差块做上/下采样，387M 参数（普通版 215M）；
- 第一阶段可去掉 attention（VQ-LDM-4 无注意力版）以降低高分辨率解码的显存。

**为何潜空间扩散便宜**：以 f=4、3 通道 RGB → 4 通道潜变量为例，512×512×3 ≈ 78.6 万维变成 128×128×4 ≈ 6.5 万维；扩散每步算力与显存近似线性于维度，训练/推理整体成本下降一到两个数量级，同时卷积的平移等变性让模型可以**卷积式滑窗外推到训练分辨率之外**（256² 训练 → 512×1024 采样，图 8 语义合成实验）。

### 2.4 条件机制：拼接与 cross-attention（本文最核心的方法贡献）

DM 通过条件去噪自编码器 $\epsilon_\theta(z_t, t, y)$ 学 $p(z \mid y)$ 实现可控生成。论文给出两类注入方式：

![[fig3-条件注入机制架构.png]]
*图 3：两种条件注入机制。上：拼接式（concatenation）——空间对齐的条件（如降采样后的语义图/低分辨率图）直接与 $z_t$ 沿通道维拼接后进 UNet；下：cross-attention——任意模态条件 y 先经领域编码器 $\tau_\theta(y)$ 变成 token 序列，再在 UNet 中间层做交叉注意力注入。*

**方式一：拼接（concatenation）**。适用于**空间对齐**的条件（语义图、掩码+已知区域、低分辨率图）：把条件降采样到潜变量分辨率后与 $z_t$ 在通道维 concat，UNet 输入通道相应加宽。用于语义合成、超分、修复。

**方式二：cross-attention（通用机制）**。处理**非空间对齐/任意模态**的条件（文本、类别、布局框、参数向量）：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right) V$$

$$Q = W_Q^{(i)} \cdot \varphi_i(z_t), \quad K = W_K^{(i)} \cdot \tau_\theta(y), \quad V = W_V^{(i)} \cdot \tau_\theta(y)$$

- $\tau_\theta$：领域专用条件编码器，把 $y$ 投影为中间表示 $\tau_\theta(y) \in \mathbb{R}^{M \times d_\tau}$（如文本用 Transformer，布局用小 CNN+展平成 token）；
- $\varphi_i(z_t) \in \mathbb{R}^{N \times d_\epsilon^i}$：UNet 第 $i$ 层中间特征（展平为 token）；
- $W_Q^{(i)} \in \mathbb{R}^{d \times d_\epsilon^i}$，$W_K^{(i)}, W_V^{(i)} \in \mathbb{R}^{d \times d_\tau}$：可学习投影矩阵；
- cross-attention 输出以残差形式并回主干，$\tau_\theta$ 与 $\epsilon_\theta$ **联合端到端训练**。

条件 LDM 的完整目标（式 3）：

$$\mathcal{L}_{LDM} := \mathbb{E}_{\mathcal{E}(x), y, \epsilon \sim \mathcal{N}(0,1), t}\left[ \left\| \epsilon - \epsilon_\theta(z_t, t, \tau_\theta(y)) \right\|_2^2 \right]$$

**这个设计的价值**：条件注入与 UNet 主干解耦，同一主干可以挂不同 $\tau_\theta$ 接不同模态条件；注意力让每个空间位置自行决定"看条件的哪一段"，是多条件融合的天然容器。

### 2.5 Classifier-Free Guidance（CFG）

训练时以一定概率把条件 $y$ 替换为空条件 $\varnothing$（等价同时学无条件模型），采样时外推两个噪声预测之差：

$$\tilde{\epsilon}_\theta(z_t, c) = \epsilon_\theta(z_t, \varnothing) + w \cdot \left[\epsilon_\theta(z_t, c) - \epsilon_\theta(z_t, \varnothing)\right]$$

- $w=1$ 退化为普通条件采样；$w>1$ 沿"条件方向"外推，牺牲多样性换条件遵从度与样本质量；
- 类条件 ImageNet 上用 $w=1.5$ 即把 FID 从 10.56 拉到 **3.60**（表 3）；文本条件 COCO 上 FID 从 23.35 → **12.61**（表 2）。

## 3. Experiments 实验

### 3.1 压缩率消融（最重要的实验）

见 2.2 图 5/6：**f∈[4,16] 甜点区**；LDM-1 与 LDM-8 差距 FID 38；LDM-32 过压缩伤上界。

### 3.2 无条件生成（256²，表 1，VQ 正则）

| 数据集 | 方法 | FID ↓ | Precision/Recall |
|---|---|---|---|
| CelebA-HQ | StyleGAN / ProjectedGAN | 4.16 / 3.08 | 0.71/0.46 · 0.65/0.46 |
| CelebA-HQ | **LDM-4（200 步 DDIM）** | **4.98** | 0.73/0.50 |
| FFHQ | **LDM-8（KL）** | **4.02** | 0.64/0.52 |
| LSUN-Churches | ADM / **LDM-4** | 1.90 / 2.95 | — |

与 GAN 系仍有差距但已高度竞争，recall（多样性）普遍更好。

![[fig4-各数据集生成样例.png]]
*图 4：LDM 在 CelebA-HQ / FFHQ / LSUN-Churches / LSUN-Bedrooms / 类条件 ImageNet 上的 256² 生成样例。*

### 3.3 类条件 ImageNet（表 3，CFG scale=1.5）

| 方法 | FID ↓ | IS ↑ | P/R | 参数量 |
|---|---|---|---|---|
| BigGAN-deep | 6.95 | 203.6 | 0.87/0.28 | 340M |
| ADM / ADM-G | 10.94 / 4.59 | 100.98 / 186.7 | — | 554M / 608M |
| **LDM-4 / LDM-4-G** | 10.56 / **3.60** | 103.5 / **247.7** | 0.71/0.62 · 0.87/0.48 | **400M** |

LDM-4-G 以 400M 参数、无分类器引导，FID 3.60 超过 ADM-G（4.59，608M）——新 SOTA。

### 3.4 文本到图像（COCO 零样本，表 2）

| 方法 | FID ↓ | IS ↑ |
|---|---|---|
| DALL·E / CogView / Lafite | 27.50 / 27.10 / 26.94 | 17.9 / 18.2 / 26.0 |
| **LDM-KL-8 / +G（w=1.5）** | 23.35 / **12.61** | 19.9 / **26.6** |

文本条件 $\tau_\theta$ 用预训练 CLIP 文本 Transformer；CFG 把 FID 近乎减半。

### 3.5 卷积式采样与分辨率外推（4.3.2）

拼接式条件不改变网络的空间结构 → 256² 训练的语义合成模型可直接滑窗外推到 **512×1024** 风景图生成（图 8），无需重训练——这是像素级全局 attention 路线（DALL·E）做不到的。

### 3.6 超分辨率与修复

- **×4 超分（ImageNet-Val 256²，表 4）**：低分辨率图上采样后与 $z_t$ 拼接。LDM-SR 纹理真实感优于 SR3，但精细连贯结构（如重复图案）不如 SR3；big 版（552M，100 步）FID 2.4†，A100 上 4.5 s/图；带引导 50 步版（184M）仅 0.38 s/图。
- **修复（4.5，表 7）**：掩码 + 被掩图像拼接进网络；采样时每步做潜层融合（已知区域保持 noised 版本）。big+finetune 版（387M）FID 9.39（40–50% 掩码比例），用户研究中整体优于 LaMa，且可**组合多对象场景合成**（cross-attention 的功劳）。

## 4. 结论与局限

**结论**：把感知压缩交给自编码器、把语义生成交给潜空间扩散，DM 的算力门槛下降一到两个数量级；cross-attention 条件机制 + CFG 使一个统一框架覆盖无条件/类/文本/布局/超分/修复六类任务，类条件与修复刷新 SOTA。

**局限**：

- 两阶段训练非端到端：第一阶段重建误差是生成质量的硬上界，编码器无法根据下游扩散需求自适应；
- 潜空间正则的取舍（KL vs VQ）仍是经验性权衡；
- 依赖预训练文本编码器（CLIP），文本理解能力受制于它；
- 高频细节完全交给解码器，极端压缩下细节失真（f=32）。

## 关键概念

- **感知压缩 / 语义压缩**：图像生成可分解的两个子问题；LDM 把前者交给 autoencoder、后者交给 diffusion，是全文一切设计的出发点。
- **下采样倍率 f**：第一阶段压缩率的唯一旋钮；f∈[4,16] 为甜点区，权衡重建上界与扩散算力。
- **KL-reg / VQ-reg**：潜空间两种正则；KL 连续（可控生成主流），VQ 离散（论文主实验默认，采样质量更优）。
- **cross-attention 条件注入**：$\tau_\theta(y) \to K/V$、UNet 特征 $\to Q$ 的通用条件接口，任意模态条件可插拔，多条件融合的容器。
- **拼接式注入**：空间对齐条件（图到图任务）直接通道拼接，保留卷积平移等变性，支持分辨率外推。
- **CFG**：条件/无条件噪声预测差值外推，$w$ 控制条件遵从度与多样性的权衡。

## 对我们课题的启发

1. **主模型直接对标**：我们规划的条件 LDM（VAE + 条件扩散主干）就是本文架构；实验顺序也应复刻——先单独训练并冻结 CT/MRI 的第一阶段 VAE（评估重建 PSNR/SSIM 与潜空间统计），再训潜空间条件 UNet。
2. **f 的选择对 CT 尤其重要**：CT 的 HU 定量值与细微结构（骨小梁、小病灶）对重建误差敏感，f=4（甚至 f=2）比自然图像更稳妥；需在 4×5090 上做与图 5 对应的压缩率消融（CT 切片 512×512）。
3. **六轴条件向量的注入方式选型**：论文给出了两条路——空间对齐条件（源图像潜变量）走**拼接**，参数类标量条件（mAs/视角数/弧段/r/SOD/SDD，即 [[项目/学习项目/研究生阶段/多任务成像/条件参数体系|条件参数体系]] 六轴）可走 **cross-attention**（每轴一个 token，$\tau_\theta$ 用小 MLP/Transformer）或参考 [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文5：CT重建与PDF参数依赖框架|论文5 PDF]] 的 FiLM 逐通道调制。标量参数条件下 FiLM/AdaLN 类注入通常比 cross-attention 更直接，可作为对照实验。
4. **未见条件组合泛化**：CFG 的差值外推提示了一个思路——把"目标条件向量 − 源条件向量"的方向性信息显式利用（与我们小复刻中"条件差向量驱动转换"的假设一致）；训练时对六轴条件做随机 dropout（5%–10%）保留无条件分支，是获得插值/外推能力的必要手段。
5. **工程对齐**：服务器 diffusers 的 `AutoencoderKL` + `UNet2DConditionModel` + `cross_attention_kwargs` 就是本文两个阶段的实现；直接复用，重点改造 $\tau_\theta$。

## 关联笔记

- [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文1：去噪扩散概率模型（DDPM）|论文1：去噪扩散概率模型（DDPM）]]：第二阶段扩散目标函数的来源。
- [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文2：通过随机微分方程进行基于分数的生成建模|论文2：Score-SDE]]：扩散框架的连续时间理论与条件生成视角。
- [[项目/学习项目/研究生阶段/多任务成像/相关论文/论文5：CT重建与PDF参数依赖框架|论文5：CT重建与PDF参数依赖框架]]：FiLM 条件调制 vs 本文 cross-attention，两种条件注入路线的对照。
- [[项目/学习项目/研究生阶段/多任务成像/初始规划|初始规划]]：本笔记是主模型（条件潜空间扩散）的原型文献。
- [[项目/学习项目/研究生阶段/多任务成像/条件参数体系|条件参数体系]]：六轴条件进入 $\tau_\theta$ 的具体载体。
- [[笔记/知识库/知识库索引]]：全库主题索引。

## 资料来源

- 原文 PDF：`assets/论文6：高分辨率图像合成与潜空间扩散模型（LDM）/LDM论文-CVPR2022.pdf`（CVPR 相机就绪版，12 页正文）
- arXiv 完整版（45 页含附录）：[arXiv:2112.10752](https://arxiv.org/abs/2112.10752)
- CVF 开放获取：[openaccess.thecvf.com](https://openaccess.thecvf.com/content/CVPR2022/papers/Rombach_High-Resolution_Image_Synthesis_With_Latent_Diffusion_Models_CVPR_2022_paper.pdf)
