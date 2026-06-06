# 1. 研究任务

将低剂量CT图像（quarter_1mm）恢复为常规剂量CT图像（full_1mm）质量，在降低辐射剂量的同时保持图像诊断质量。
- **输入**：低剂量CT图像（含噪声和伪影）
- **输出**：去噪恢复后的CT图像
- **Ground Truth**：常规剂量CT图像

# 2. 方法

### 2.1 论文参考
- *Low-Dose CT with a Residual Encoder-Decoder Convolutional Neural Network* (Chen et al., 2017)
- *Deep Convolutional Neural Network for Inverse Problems in Imaging* (Jin et al., 2017)

### 2.2 网络结构

FBPConvNet 基于编码器-解码器（U-Net）架构，采用**残差学习**策略：
```
output = ReLU(x + net(x))
```
网络学习噪声/伪影（残差），而非直接学习全量映射，训练更高效。

|模块|结构|通道数|
|---|---|---|
|Encoder 1|Conv3×3→ReLU × 2|1 → 64|
|Encoder 2|MaxPool + Conv×2|64 → 128|
|Encoder 3|MaxPool + Conv×2|128 → 256|
|Encoder 4|MaxPool + Conv×2|256 → 512|
|Bottleneck|Conv×2|512 → 1024|
|Decoder 4|ConvTranspose + Skip + Conv×2|1024 → 512|
|Decoder 3|ConvTranspose + Skip + Conv×2|512 → 256|
|Decoder 2|ConvTranspose + Skip + Conv×2|256 → 128|
|Decoder 1|ConvTranspose + Skip + Conv×2|128 → 64|
|Output Conv|Conv 1×1|64 → 1|

**关键设计**：

- **Skip Connection**：保留细节信息，避免深层网络丢失空间特征

- **残差学习**：学习残差（噪声）比直接学习全量映射更高效

- **参数量**：31M

  

## 3. 数据集

  

**AAPM Low-Dose CT Challenge 数据集**：

  

| 分割 | 病人编号 | 切片数量 |

|------|---------|---------|

| 训练集 | L109, L192, L286, L143 | 2028 对 |

| 验证集 | L096, L333 | 1433 对 |

| 测试集 | L310, L067 | — |

  

每对图像：quarter_1mm（低剂量）↔ full_1mm（常规剂量）

  

## 4. 训练配置

  

| 项目 | 设置 |

|------|------|

| 优化器 | Adam (lr=1e-4) |

| 损失函数 | MSE + 0.1 × (1 - SSIM) |

| 学习率策略 | StepLR (step=10, γ=0.5) |

| Batch Size | 4 |

| Early Stopping | patience=15 |

| 最佳模型 | epoch 11 |

  

## 5. 训练曲线分析

  

- **MSE Loss**：训练MSE从634持续下降至357；验证MSE在epoch 11达到最低446.6后开始上升

- **SSIM**：验证SSIM在epoch 11达到最高值0.9666后逐步下降

- **结论**：epoch 11为最佳模型，之后出现过拟合趋势

  

![训练曲线](runs/FBPConvNet/results/training_curves.png)

  

## 6. 测试结果

  

### 6.1 定量指标（测试集：L310 + L067）

  

| 指标 | 低剂量CT | FBPConvNet | 提升 |

|------|---------|-----------|------|

| PSNR (dB) | 35.26 ± 1.55 | **40.56 ± 1.39** | **+5.31** |

| SSIM | 0.8312 ± 0.0434 | **0.9436 ± 0.0154** | **+0.1124** |

  

### 6.2 各病人结果

  

| 病人 | LDCT PSNR | Pred PSNR | LDCT SSIM | Pred SSIM |

|------|-----------|-----------|-----------|-----------|

| L310 | 34.84 | 40.43 | 0.8147 | 0.9392 |

| L067 | 35.65 | 40.69 | 0.8468 | 0.9478 |

  

### 6.3 可视化对比

  

![PSNR/SSIM分布](runs/FBPConvNet/results/metrics_histogram.png)

  

典型切片对比示例（从左到右：Ground Truth / Low Dose / FBPConvNet / |GT-LDCT| / |GT-Pred|）：

  

![L310示例](runs/FBPConvNet/results/L310_slice267.png)

  

## 7. 结论与展望

  

### 结论

- FBPConvNet 可有效去除低剂量CT图像噪声，PSNR提升5.31 dB，SSIM提升0.1124

- 残差学习策略使网络收敛更快、更稳定

- 模型在epoch 11后出现过拟合，说明数据集规模（4个训练病人）有限

  

### 改进方向

- **数据增强**：旋转、翻转等增加训练数据多样性

- **损失函数**：引入感知损失（VGG perceptual loss）

- **网络改进**：增加深度注意力机制、残差密集块

- **训练策略**：使用Cosine Annealing学习率、更大batch size

  

## 8. 文件结构

  

```

AICT/

├── models.py                  # FBPConvNet 模型定义

├── train_fbpconvnet.py        # 训练脚本（含 early stopping）

├── visualize_fbpconvnet.py    # 推理 + 可视化脚本

├── plot_training_curves.py    # 训练曲线绘制脚本

├── mk_data_list.py            # 数据列表生成

├── datasets/

│   ├── __init__.py

│   └── read_dicom_file.py     # DICOM 数据读取

├── losses.py                  # 损失函数

├── utils.py                   # 工具函数

└── runs/FBPConvNet/

    ├── checkpoints/            # 模型 checkpoint (epoch 10-31)

    ├── best_model/

    │   └── best_model.dat      # 最佳模型 (epoch 11)

    └── results/

        ├── training_curves.png   # 训练曲线

        ├── metrics_histogram.png # PSNR/SSIM 分布

        ├── L310_slice*.png       # L310 病人切片对比

        ├── L067_slice*.png       # L067 病人切片对比

        └── metrics.txt            # 定量指标记录

```