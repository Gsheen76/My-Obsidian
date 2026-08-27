---
tags:
  - 医学影像
  - CT
  - 深度学习
  - 图像去噪
title: 低剂量CT图像去噪（WGAN-GP与VGG感知损失的对比研究）
type: experiment
summary: 整理低剂量 CT 图像恢复任务中的方法、实验配置和结果。
updated: 2026-08-05
migrated: 2026-08-05
---

> [!summary] Summary
> 整理低剂量 CT 图像恢复任务中的方法、实验配置和结果。

# 1. 论文复现背景

复现论文 *"Low-dose CT image denoising using a generative adversarial network with Wasserstein distance and perceptual loss"* 中的两个核心任务：

- **任务1**: 基于WGAN-GP的CT图像去噪（对抗训练）
- **任务2**: 基于VGG感知损失的CT图像去噪（感知质量优化）

# 2. 方法概述

### 2.1 网络架构

- **Generator (UNet2d)**: 编码器-解码器结构，4层下采样+4层上采样，残差学习（输出 = ReLU(input + residual)）
- **Discriminator (Discriminator2D)**: 5层卷积+全局平均池化，输出Wasserstein距离评分
- **VGG Feature Extractor**: VGG-16前27层，提取5层特征用于感知损失计算

### 2.2 损失函数

| 方法 | 损失函数 | 公式 |
|------|----------|------|
| WGAN-GP | Generator | $L_G = L_{MSE} + 0.01 \times L_{adv}$ |
| WGAN-GP | Discriminator | $L_D = -\mathbb{E}[D(x_r)] + \mathbb{E}[D(x_f)] + 10 \times GP$ |
| VGG Perceptual | Generator | $L = L_{MSE} + 0.02 \times L_{VGG}$ |

- $L_{adv}$: Wasserstein对抗损失（-mean(D(fake))）
- $GP$: 梯度惩罚（gradient penalty）
- $L_{VGG}$: VGG 5层特征MSE之和（输入经高斯平滑预处理）
- Patch切分：Discriminator输入4×4 patch

# 3. 数据集

- **AAPM Low-Dose CT Challenge数据集**
- quarter-dose (LDCT) ↔ full-dose (RDCT) 配对
- 训练集: 2884对 (L109, L291, L192, L286, L143)
- 验证集: 1433对 (L096, L333)
- 图像尺寸: 512×512, DICOM格式

# 4. 训练配置

| 配置 | WGAN-GP | VGG Perceptual |
|------|---------|---------------|
| Batch Size | 4 | 10 |
| Learning Rate (G) | 1e-4 | 1e-4 |
| LR Scheduler | StepLR(100, 0.1) | StepLR(2, 0.95) |
| Optimizer (G) | Adam | Adam |
| Optimizer (D) | Adam(β1=0.5, β2=0.9) | - |
| Max Epochs | 1000 | 100 |
| Early Stopping | patience=50 | patience=20 |

# 5. 训练结果

### 5.1 定量指标

| 方法 | Best Valid MSE | Best Valid SSIM | Best Epoch | 早停Epoch |
|------|---------------|-----------------|------------|----------|
| WGAN-GP | **503.47** | 0.9613 | 14 | 64 |
| VGG Perceptual | 517.46 | **0.9620** | 37 | 57 |

### 5.2 去噪样本指标

| 样本 | LDCT MSE | LDCT SSIM | WGAN-GP MSE | WGAN-GP SSIM | VGG MSE | VGG SSIM |
|------|----------|-----------|-------------|-------------|---------|---------|
| #1 | 1237.00 | 0.9475 | **330.74** | 0.9849 | 359.25 | 0.9847 |
| #2 | 1139.01 | 0.9523 | **317.02** | 0.9861 | 339.93 | 0.9860 |
| #3 | 1180.16 | 0.9517 | **330.69** | 0.9857 | 349.46 | 0.9854 |

### 5.3 分析

- **MSE**: WGAN-GP更低（503 vs 517），说明像素级重建更精确
- **SSIM**: VGG略高（0.962 vs 0.961），感知质量略优
- **训练MSE**: VGG最终训练MSE更低（444 vs 467），但验证MSE更高达成过拟合
- **收敛速度**: WGAN-GP在14 epoch达到最佳，VGG在37 epoch
- **稳定性**: WGAN-GP验证损失波动较大，VGG更平稳

# 6. 可视化结果

- `loss_curves_mse.png`: 训练/验证MSE对比曲线
- `ssim_curves.png`: 验证SSIM对比曲线
- `training_comparison.png`: 2×2综合训练曲线
- `denoising_comparison.png`: 3行×4列去噪效果对比
- `denoising_sample_1/2/3.png`: 单样本详细对比

# 7. 文件结构

```
基于AI的CT图形恢复任务/
├── train_unet_2d_gan.py      # WGAN-GP训练脚本
├── train_unet_2d_vgg.py      # VGG感知损失训练脚本
├── models.py                  # UNet2d + Discriminator2D
├── losses.py                  # VGG特征提取 + 感知损失
├── utils.py                   # SSIM, 高斯平滑, 工具函数
├── datasets/read_dicom_file.py
├── mk_data_list.py            # 数据列表生成
├── train_img.txt / valid_img.txt
├── AAPM图像/                  # DICOM数据
├── runs/
│   ├── UNet2D_GAN_Holder/     # GAN训练日志和检查点
│   └── UNet2D_VGG/            # VGG训练日志和检查点
├── results/                   # 可视化结果
└── visualize.py               # 可视化脚本
```

## 关键概念

- 医学影像、CT、深度学习、图像去噪

## 关联笔记

- [[笔记/知识库/知识库索引]]
- [[笔记/研0/笔记/医学图像重建入门]]
- [[../../../../项目/学习项目/多任务成像/相关论文/四篇学习笔记/生成模型详解]]

## 规划

- [ ] 补充或更新本笔记中的结果、限制与下一步工作。

## 资料来源

- [ ] 补充原始论文、官方文档或数据集链接。
