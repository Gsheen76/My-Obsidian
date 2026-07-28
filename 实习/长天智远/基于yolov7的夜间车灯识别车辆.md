---
tags:
  - yolo
  - vehicle-detection
  - cv
  - 项目文档
aliases:
  - 车灯检测
  - 车辆车灯检测
created: 2026-07-06
updated: 2026-07-27
---
## 概述

本项目通过检测车辆车灯（前灯 head / 尾灯 tail）来识别车辆，基于 **YOLOv7** 目标检测框架实现。采用 **"训练 → 预标注 → 人工审核 → 扩充数据 → 再训练"** 的迭代式数据扩充策略，逐步提升模型精度。

| 项目 | 说明 |
|------|------|
| 项目根目录 | `/data2/ai/yolov7-main-WFS` |
| 数据集目录 | `/data2/ai/yolov7-main-WFS/dataset` |
| 检测类别 | 2 类 —— `head`（前灯, class 0）、`tail`（尾灯, class 1） |
| 标注工具 | labelImg（VOC XML 格式标注） |
| 硬件环境 | 2 × NVIDIA A10（各 23GB 显存，被 vLLM 占用部分显存） |
| 当前最佳模型 | `runs/train/yolo_light_exp7/weights/best.pt`（mAP@.5=0.880） |

---

## 项目时间线

```mermaid
gantt
    title 车灯检测项目迭代历程
    dateFormat YYYY-MM-DD
    section 人工标注
    batch_1~2 手动标注           :done, a1, 2026-07-06, 3d
    batch_3~6 手动标注           :done, a2, after a1, 4d
    batch_7~9 手动标注           :done, a3, after a2, 5d
    section 训练迭代
    第1轮 exp16 (try1, 510)      :done, t1, 2026-07-06, 1d
    第2轮 exp2 (try2, 990)       :done, t2, after t1, 1d
    第3轮 exp3 (try3, 1041)      :done, t3, after t2, 1d
    第4轮 exp4 (try3, 150ep)     :done, t4, after t3, 1d
    第5轮 exp5 (try4, 1505)      :done, t5, after t4, 1d
    第6轮 exp6 (1280, 200ep)     :done, t6, after t5, 1d
    section 预标注+审核
    首次预标注尝试(弃用)         :done, p1, after t4, 1d
    用exp6模型预标注dataset2     :done, p2, after t6, 2d
    审核batch_1~4并入训练集      :done, p3, after p2, 2d
    section 扩充训练
    第7轮 exp7 (try5, 2476)     :done, t7, after p3, 1d
    审核剩余预标注(进行中)      :active, p4, after t7, 3d
    第8轮 exp8 (try6, 预计4000+) :planned, t8, after p4, 1d
```

---

## 数据情况

### 数据来源与标注方式

| 数据批次 | 图片来源 | 标注方式 | 说明 |
|----------|----------|----------|------|
| `dataset/batch_1~9` | 视频抽帧 | 纯人工标注 | 原始训练数据，1505 个有效标注 |
| `dataset/dataset2/batch_1~4` | 视频抽帧 | **预标注 + 人工审核** | exp6 模型预标注，人工审核修正，971 个有效标注，已并入 try5 |
| `/data2/ai/dataset2/batch_1~9` | 视频抽帧 | **预标注 + 人工审核** | exp7 模型预标注，2742 个 XML，**待审核**，用于下一轮扩充 |

> [!warning] 注意
> batch 中没有 XML 的图片是主动放弃的废图（无车灯或不可识别），**不可使用**。

### 各 batch 有效标注统计

**原始人工标注数据（`dataset/batch_1~9`）：**

| 目录 | jpg | 有效 xml |
|------|-----|---------|
| batch_1 | 500 | 235 |
| batch_2 | 500 | 224 |
| batch_3 | 500 | 165 |
| batch_4 | 500 | 145 |
| batch_5 | 500 | 170 |
| batch_6 | 288 | 102 |
| batch_7 | 500 | 166 |
| batch_8 | 500 | 142 |
| batch_9 | 500 | 156 |
| **小计** | **3788** | **1505** |

**预标注审核后数据（`dataset/dataset2/batch_1~4`，已并入训练集）：**

| 目录 | jpg | 预标注 xml | 审核后有效 |
|------|-----|-----------|-----------|
| batch_1 | 500 | 331 | 271 |
| batch_2 | 500 | 328 | 283 |
| batch_3 | 500 | 322 | 257 |
| batch_4 | 300 | 204 | 160 |
| **小计** | **1800** | **1185** | **971** |

> [!info] 预标注审核通过率
> 1185 个预标注框经人工审核后保留 971 个，通过率 82%。审核主要工作：删除误检框、修正偏移框、补充漏检框。

**预标注待审核数据（`/data2/ai/dataset2/batch_1~9`，用于下一轮扩充）：**

| 目录 | jpg | 预标注 xml |
|------|-----|-----------|
| batch_1 | 500 | 331 |
| batch_2 | 500 | 328 |
| batch_3 | 500 | 322 |
| batch_4 | 300 | 204 |
| batch_5 | 500 | 336 |
| batch_6 | 500 | 308 |
| batch_7 | 500 | 336 |
| batch_8 | 421 | 254 |
| batch_9 | 500 | 323 |
| **小计** | **4221** | **2742** |

**汇总：**

| 数据来源 | jpg | 有效标注 | 状态 |
|----------|-----|---------|------|
| 原始人工标注 | 3788 | 1505 | ✅ 已用于训练 |
| 预标注审核后 (dataset2) | 1800 | 971 | ✅ 已用于训练 |
| 预标注待审核 (/data2/ai/dataset2) | 4221 | 2742 | ⏳ 待人工审核 |
| **总计** | **9809** | **5218** | |

> [!info] 历史数据清理记录
> - batch_1: 263 → 235（删除 28 个空标注 XML）
> - batch_2: 247 → 224（删除 23 个空标注 XML）
> - batch_3/4/5: 无空标注
> - batch_7~9 原放入 `wait_for_tag_dataset/`，首次预标注效果不佳改手动标注，后随模型提升预标注质量改善

### 数据划分（7:2:1）

使用 `dataset/make_dataset.py` 脚本完成 XML→YOLO txt 转换 + 数据集划分。

各轮训练数据集：

| 数据集 | 来源 | 有效标注 | train | val | test | 训练轮次 |
|--------|------|---------|-------|-----|------|---------|
| yolo_dataset_try1 | batch_1~2 | 510 | 357 | 102 | 51 | 第1轮 |
| yolo_dataset_try2 | batch_1~5 | 990 | 693 | 198 | 99 | 第2轮 |
| yolo_dataset_try3 | batch_1~6 | 1041 | 728 | 208 | 105 | 第3轮 / 第4轮 |
| yolo_dataset_try4 | batch_1~9 | 1505 | 1053 | 301 | 151 | 第5轮 / 第6轮 |
| **yolo_dataset_try5** | **batch_1~9 + dataset2** | **2476** | **1733** | **495** | **248** | **第7轮** |
| yolo_dataset_try6 | + 审核后预标注 | 预计4000+ | - | - | - | 第8轮（计划） |

### 输出数据集结构

当前训练使用：`dataset/yolo_dataset_try5/`

```tree
dataset/yolo_dataset_try5/
├── images/
│   ├── train/    # 1733 张训练图片
│   ├── val/      # 495 张验证图片
│   └── test/     # 248 张测试图片
├── labels/
│   ├── train/    # 1733 个 YOLO txt 标注
│   ├── val/      # 495 个 YOLO txt 标注
│   └── test/     # 248 个 YOLO txt 标注
├── train.txt     # 训练集图片绝对路径列表
├── val.txt       # 验证集图片绝对路径列表
├── test.txt      # 测试集图片绝对路径列表
├── train.cache   # 训练集缓存
└── val.cache     # 验证集缓存
```

### YOLO 标注格式

每行格式：`class_id center_x center_y width height`（坐标归一化到 0~1）

```yaml
0 0.232422 0.309028 0.027344 0.018056   # head
1 0.260547 0.238889 0.017969 0.013889   # tail
```

---

## 数据处理脚本

### make_dataset.py（XML 转 YOLO + 数据划分）

**路径**: `dataset/make_dataset.py`

**功能**:
1. 遍历多个 batch 目录，收集所有有 XML 标注的样本
2. 将 VOC XML 格式转换为 YOLO txt 格式（归一化坐标）
3. 按 7:2:1 比例随机划分 train/val/test（random_seed=42 保证可复现）
4. 复制图片到对应目录，生成 YOLO txt 标注文件
5. 生成 train.txt / val.txt / test.txt 路径列表文件

**用法**:

```bash
cd /data2/ai/yolov7-main-WFS/dataset
python3 make_dataset.py
```

**当前配置**（指向 batch_1~9 + dataset2/batch_1~4，输出 try5）:

```python
src_dirs = [
    "/data2/ai/yolov7-main-WFS/dataset/batch_1" ~ "batch_9",
    "/data2/ai/yolov7-main-WFS/dataset/dataset2/batch_1" ~ "batch_4",
]
out_root = "/data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try5"
classes = {"head": 0, "tail": 1}
train_ratio = 0.7
val_ratio   = 0.2
test_ratio  = 0.1
random_seed = 42
```

### analyze_test.py（逐张测试分析）

**路径**: `dataset/analyze_test.py`

**功能**: 对测试集逐张对比 GT 真实标注 vs 预测结果，计算 TP/FP/FN，输出每张图的状态（全漏检/有漏检/完全匹配等）。

### yolo2xml.py（YOLO txt 转 labelImg XML）

**路径**: `dataset/yolo2xml.py`

**功能**: 将 detect.py 输出的 YOLO txt 标注转换为 labelImg 可读的 VOC XML 格式，供人工审核预标注结果。

> [!important] 预标注核心工具
> 这是预标注流水线的关键环节：`detect.py` 推理生成 txt → `yolo2xml.py` 转为 XML → 导入 labelImg 人工审核。

### 预标注流水线（detect.py + yolo2xml.py）

**工作流程**:

```bash
# 1. 用 best.pt 对新图片批量推理，保存 txt 结果
python3 detect.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --source /data2/ai/dataset2/batch_1 \
  --img-size 1280 \
  --conf-thres 0.25 \
  --iou-thres 0.45 \
  --device 1 \
  --save-txt --save-conf --exist-ok

# 2. 将 txt 转为 labelImg XML
python3 dataset/yolo2xml.py

# 3. XML 放回对应 batch 目录，用 labelImg 打开审核
```

> [!success] 预标注成效
> - 第一次预标注（exp4 模型，640 分辨率）：检出率 43%，误检多，审核成本高，**弃用**
> - 第二次预标注（exp6 模型，1280 分辨率）：检出率 65%，框精度大幅改善，**成功**
> - 审核后 dataset2/batch_1~4（971 样本）并入 try5，第7轮训练 mAP 从 0.810 提升至 0.880

### 首次预标注尝试（已弃用）

曾用 `pre_annotate.py` 脚本 + exp4 best.pt 对 batch_7~9 进行预标注：

| 方案 | 参数 | 结果 | 评价 |
|------|------|------|------|
| 方案1 | conf=0.25, img-size=640 | 646/1500 张有框（43%） | 检出率太低 |
| 方案2 | conf=0.1, img-size=1280 | 1368/1500 张有框 | 误检太多 |

> [!caution] 弃用原因
> exp4 模型精度不足（mAP@.5=0.488），小目标检出率低，预标注框偏移严重。`pre_annotate.py` 脚本本身也有坐标转换 bug 和 git 下载错误。后改用 detect.py 原生推理 + yolo2xml.py 转换，问题解决。

### 其他数据处理脚本

| 脚本 | 功能 |
|------|------|
| `dataset/labelImg2yolo.py` | 单独的 XML→YOLO 转换脚本（原始 Windows 路径版本，未更新） |
| `dataset/mp4_2_pic.py` | 视频抽帧脚本 |
| `dataset/png2jpg.py` | PNG 转 JPG 格式 |
| `dataset/rename_pinyin.py` | 文件名拼音重命名 |
| `dataset/cal_0_txt.py` | 标注统计脚本 |
| `dataset/pre_annotate.py` | 早期预标注脚本（已弃用，保留备用） |

---

## 配置文件

### 数据集配置 —— my_yolo_dataset.yaml

**路径**: `data/my_yolo_dataset.yaml`

```yaml
# 车灯检测数据集 (head/tail) 配置
train: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try5/train.txt
val: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try5/val.txt
test: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try5/test.txt

nc: 2
names: ["head", "tail"]
```

### 模型配置 —— yolov7_my.yaml

**路径**: `cfg/training/yolov7_my.yaml`

基于 `cfg/training/yolov7.yaml` 复制修改，仅改动类别数：

```yaml
nc: 2  # number of classes (head, tail)，原文件为 nc: 80（COCO）
```

其余结构（backbone、head、anchors）与标准 yolov7.yaml 完全一致。

### 超参数 —— hyp.scratch.custom.yaml

**路径**: `data/hyp.scratch.custom.yaml`

使用 YOLOv7 自定义训练超参数，主要参数：

| 参数 | 值 | 说明 |
|------|-----|------|
| lr0 | 0.01 | 初始学习率 |
| lrf | 0.1 | 最终学习率衰减系数 |
| momentum | 0.937 | SGD 动量 |
| weight_decay | 0.0005 | 权重衰减 |
| warmup_epochs | 3.0 | 预热轮数 |
| box | 0.05 | 框回归损失权重 |
| cls | 0.3 | 分类损失权重 |
| obj | 0.7 | 置信度损失权重 |
| mosaic | 1.0 | 马赛克增强概率 |
| fliplr | 0.5 | 水平翻转概率 |
| hsv_h/s/v | 0.015/0.7/0.4 | HSV 颜色扰动 |

---

## 代码修改记录

为兼容 PyTorch 2.6+（`torch.load` 默认 `weights_only=True`），修改了以下文件：

| 文件 | 行号 | 修改内容 |
|------|------|----------|
| `train.py` | 71 | `torch.load(...)` → `torch.load(..., weights_only=False)` |
| `train.py` | 87 | `torch.load(weights, map_location=device)` → 加 `weights_only=False` |
| `utils/datasets.py` | 392 | `torch.load(cache_path)` → 加 `weights_only=False` |
| `utils/general.py` | 802 | `torch.load(f, map_location=...)` → 加 `weights_only=False` |
| `models/experimental.py` | 252 | 已自带 `weights_only=False`，无需修改 |

> [!note]
> `detect.py` 第48行加载 resnet101 的 `torch.load` 未修改（暂不影响训练）。

---

## 训练记录

### 各轮训练结果对比

| 指标 | 第1轮 | 第2轮 | 第3轮 | 第4轮 | 第5轮 | 第6轮 | **第7轮** |
|------|-------|-------|-------|-------|-------|------|----------|
| 实验 | exp16 | exp2 | exp3 | exp4 | exp5 | exp6 | **exp7** |
| 数据集 | try1 | try2 | try3 | try3 | try4 | try4 | **try5** |
| 训练集 | 357 | 693 | 728 | 728 | 1053 | 1053 | **1733** |
| 数据来源 | 人工 | 人工 | 人工 | 人工 | 人工 | 人工 | **人工+预标注** |
| epochs | 100 | 100 | 96(断) | 150 | 150 | 200 | **200** |
| img-size | 640 | 640 | 640 | 640 | 640 | 1280 | **1280** |
| batch | 4 | 4 | 4 | 4 | 4 | 2 | **2** |
| **mAP@.5** | 0.224 | 0.341 | 0.351 | 0.488 | 0.766 | 0.810 | **0.880** |
| mAP@.5:.95 | 0.069 | 0.118 | 0.120 | 0.176 | 0.329 | 0.363 | **0.498** |
| Precision | 0.443 | 0.406 | 0.628 | 0.546 | 0.826 | 0.745 | **0.807** |
| Recall | 0.283 | 0.390 | 0.301 | 0.540 | 0.693 | 0.808 | **0.865** |
| head mAP@.5 | 0.241 | 0.467 | 0.425 | 0.554 | 0.841 | 0.847 | **0.900** |
| tail mAP@.5 | 0.206 | 0.214 | 0.278 | 0.421 | 0.691 | 0.772 | **0.860** |
| 推理速度 | 12.8ms | 10.3ms | 9.5ms | 9.3ms | 7.0ms | 16.6ms | **14.5ms** |

> [!tip] 关键节点
> - **第5轮**：mAP 突破 0.766，模型首次可用于预标注
> - **第6轮**：img-size 升至 1280，mAP 0.810，预标注检出率达 65%
> - **第7轮**：首次使用预标注审核数据（+971样本），mAP 0.880，验证预标注扩充策略有效

> [!success] 最佳模型
> 第七轮 `runs/train/yolo_light_exp7/weights/best.pt`
> 测试评估: conf-thres=0.001, iou-thres=0.65, img-size 1280

**逐张检测分析（conf=0.25）:**
- TP: 481, FP: 227, FN: 44
- Precision: 0.68, Recall: 0.92
- head Recall: 0.91 | tail Recall: 0.92（两类别均衡）
- 完全匹配: 102张(41.1%) | 全漏检: 10张(4.0%)

**第7轮 vs 第6轮 关键提升：**

| 指标 | 第6轮 | 第7轮 | 提升幅度 |
|------|-------|-------|---------|
| mAP@.5 | 0.810 | 0.880 | **+8.6%** |
| mAP@.5:.95 | 0.363 | 0.498 | **+37%** |
| Recall | 0.808 | 0.865 | **+7%** |
| tail mAP@.5 | 0.772 | 0.860 | **+11.4%** |
| 训练集规模 | 1053 | 1733 | **+64.7%** |

> [!quote] 预标注扩充验证
> 第7轮实验直接证明了预标注策略的有效性：模型训练越多，预标注质量越高，人工审核成本越低，形成正向循环。

---

### 第一轮训练（yolo_light_exp16）—— 510 样本

- 数据集: yolo_dataset_try1（510 样本，train 357 / val 102 / test 51）
- epochs: 100，batch-size: 4，img-size: 640
- 预训练参数迁移: 552/566
- 训练完成 100/100 epochs

**逐张分析（conf-thres=0.25, IoU=0.5）:**
- 总GT: 148, TP: 24, FP: 22, FN: 124
- Precision: 0.52, Recall: 0.16
- 全漏检: 31张 | 有漏检: 11张 | 完全匹配: 2张
- 分析报告: `runs/detect/test_results/analysis.txt`

### 第二轮训练（yolo_light_exp2）—— 990 样本

- 数据集: yolo_dataset_try2（990 样本，train 693 / val 198 / test 99）
- epochs: 100，batch-size: 4，img-size: 640
- 训练完成 100/100 epochs

**逐张分析（conf-thres=0.25, IoU=0.5）:**
- 总GT: 262, TP: 80, FP: 94, FN: 182
- Precision: 0.46, Recall: 0.31

### 第三轮训练（yolo_light_exp3）—— 1041 样本

- 数据集: yolo_dataset_try3（1041 样本，train 728 / val 208 / test 105）
- epochs: 100，batch-size: 4，img-size: 640
- 训练在 epoch 96 被中断，但 best.pt 已保存

### 第四轮训练（yolo_light_exp4）—— 增加 epochs

- 数据集: yolo_dataset_try3（1041 样本，train 728 / val 208 / test 105）
- epochs: **150**，batch-size: 4，img-size: 640
- GPU: 1，训练日志: `train4.log`，tmux 会话: `yolo_train4`
- 训练完成 150/150 epochs

**测试集结果:**

| 类别 | P | R | mAP@.5 | mAP@.5:.95 |
|------|-----|-----|--------|------------|
| all | 0.546 | 0.540 | 0.488 | 0.176 |
| head | 0.588 | 0.611 | 0.554 | 0.212 |
| tail | 0.505 | 0.469 | 0.421 | 0.140 |

### 第五轮训练（yolo_light_exp5）—— 1505 样本

- 数据集: yolo_dataset_try4（1505 样本，train 1053 / val 301 / test 151）
- epochs: 150，batch-size 4，img-size 640
- 训练完成 150/150 epochs，无过拟合
- 详细分析: `runs/train/yolo_light_exp5/数据分析报告.md`

**测试集结果（conf=0.001, iou=0.65）:**

| 类别 | P | R | mAP@.5 | mAP@.5:.95 |
|------|-----|-----|--------|------------|
| all | 0.826 | 0.693 | 0.766 | 0.329 |
| head | 0.827 | 0.786 | 0.841 | 0.393 |
| tail | 0.825 | 0.600 | 0.691 | 0.266 |

### 第六轮训练（yolo_light_exp6）—— img-size 1280

- 数据集: yolo_dataset_try4（1505 样本，train 1053 / val 301 / test 151）
- epochs: **200**，batch-size: 2，**img-size: 1280**
- GPU: 1，训练日志: `train6.log`，tmux 会话: `yolo_train6`
- 训练完成 200/200 epochs

**核心改进**：提高输入分辨率至 1280 以改善小目标检测

**测试集结果（conf=0.001, iou=0.65, img-size 1280）:**

| 类别 | P | R | mAP@.5 | mAP@.5:.95 |
|------|-----|-----|--------|------------|
| all | 0.745 | **0.808** | **0.810** | **0.363** |
| head | 0.785 | 0.822 | 0.847 | 0.412 |
| tail | 0.704 | 0.793 | 0.772 | 0.315 |

> [!info] 模型达到可用阈值
> mAP@.5=0.810 时预标注检出率达 65%，人工审核成本可接受，开始预标注扩充流程。

### 第七轮训练（yolo_light_exp7）—— 当前最佳

- 数据集: yolo_dataset_try5（2476 样本，train 1733 / val 495 / test 248）
- epochs: **200**，batch-size: 2，**img-size: 1280**
- GPU: 1，训练日志: `train7.log`，tmux 会话: `yolo_train7`
- 训练完成 200/200 epochs

**核心改进**：首次使用预标注审核数据（dataset2/batch_1~4，+971 样本），总训练集达 1733

**测试集结果（conf=0.001, iou=0.65, img-size 1280）:**

| 类别 | P | R | mAP@.5 | mAP@.5:.95 |
|------|-----|-----|--------|------------|
| all | **0.807** | **0.865** | **0.880** | **0.498** |
| head | 0.829 | 0.872 | **0.900** | 0.513 |
| tail | 0.784 | 0.857 | **0.860** | 0.482 |

**逐张检测分析（conf=0.25）:**

| 指标 | 值 |
|------|-----|
| TP | 481 |
| FP | 227 |
| FN | 44 |
| Precision | 0.68 |
| Recall | 0.92 |
| head R | 0.91 |
| tail R | 0.92 |
| 完全匹配 | 102张(41.1%) |
| 全漏检 | 10张(4.0%) |

---

### 训练命令

**tmux 后台运行（推荐）**:

```bash
tmux new-session -d -s yolo_train7 "cd /data2/ai/yolov7-main-WFS && python3 train.py \
  --weights weights/yolov7.pt \
  --cfg cfg/training/yolov7_my.yaml \
  --data data/my_yolo_dataset.yaml \
  --hyp data/hyp.scratch.custom.yaml \
  --epochs 200 \
  --batch-size 2 \
  --img-size 1280 1280 \
  --device 1 \
  --name yolo_light_exp7 \
  --workers 4 2>&1 | tee train7.log"
```

### tmux 常用命令

```bash
tmux attach -t yolo_train7       # 进入 tmux 会话查看实时输出
# 在 tmux 内按 Ctrl+B 然后 D       # 退出 tmux（不停止训练）
tmux ls                           # 查看所有 tmux 会话
tmux kill-session -t yolo_train7 # 停止训练并关闭会话
tail -f /data2/ai/yolov7-main-WFS/train7.log   # 查看训练日志
```

---

## 推理/测试

### 检测单张图片

```bash
python3 detect.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --source /path/to/image.jpg \
  --img-size 1280 \
  --conf-thres 0.25 \
  --iou-thres 0.45 \
  --device 1
```

### 测试集评估

```bash
python3 test.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --data data/my_yolo_dataset.yaml \
  --task test \
  --img-size 1280 \
  --conf-thres 0.001 \
  --iou-thres 0.65 \
  --device 1 \
  --batch-size 8
```

### 逐张检测分析

```bash
# 1. detect.py 推理并保存结果
python3 detect.py --weights runs/train/yolo_light_exp7/weights/best.pt \
  --source dataset/yolo_dataset_try5/images/test \
  --img-size 1280 --conf-thres 0.25 --iou-thres 0.45 \
  --device 1 --name test_results7 --save-txt --save-conf --exist-ok

# 2. 逐张分析
python3 dataset/analyze_test.py
```

### 视频检测

```bash
python3 detect.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --source /path/to/video.mp4 \
  --img-size 1280 \
  --device 1
```

### 模型导出（计划）

```bash
# 导出 ONNX
python3 export.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --grid --simplify \
  --include onnx

# 导出 TensorRT（需部署环境支持）
python3 export.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --include engine \
  --device 0
```

---

## 预标注策略

### 迭代式数据扩充核心思路

```mermaid
flowchart LR
    A[人工标注初始数据] --> B[训练模型]
    B --> C[模型推理预标注新数据]
    C --> D[人工审核预标注结果]
    D --> E[合并扩充训练集]
    E --> B
    B --> F{mAP达标?}
    F -->|否| C
    F -->|是| G[导出模型部署]
```

### 两次预标注对比

| 项目 | 第一次（弃用） | 第二次（成功） |
|------|--------------|--------------|
| 使用模型 | exp4 best.pt (mAP=0.488) | exp6 best.pt (mAP=0.810) |
| 推理工具 | `pre_annotate.py` 自定义脚本 | `detect.py` 原生推理 |
| 转换工具 | 脚本内嵌（坐标有 bug） | `yolo2xml.py` 独立转换 |
| img-size | 640 / 1280 | 1280 |
| conf 阈值 | 0.25 / 0.1 | 0.25 |
| 目标数据 | batch_7~9 (1500张) | /data2/ai/dataset2 (4221张) |
| 检出率 | 43% / 91%(误检多) | 65% |
| 误检情况 | 严重 | 可接受 |
| 审核成本 | 极高（不如手动标注） | 中等（可接受） |
| 结果 | **弃用** | **成功，971样本已并入训练** |

> [!tip] 经验总结
> 1. 模型 mAP@.5 需达到 **0.8 以上**，预标注才具有实用价值
> 2. 使用 `detect.py` 原生推理比自定义脚本更可靠（避免坐标转换 bug）
> 3. img-size 1280 对小目标（车灯）检出率提升显著
> 4. 人工审核仍不可省略，但预标注大幅减少画框工作量

### 预标注流水线（detect.py + yolo2xml.py）

```bash
# 1. 用 best.pt 对新图片批量推理，保存 txt 结果
python3 detect.py \
  --weights runs/train/yolo_light_exp7/weights/best.pt \
  --source /data2/ai/dataset2/batch_1 \
  --img-size 1280 \
  --conf-thres 0.25 \
  --iou-thres 0.45 \
  --device 1 \
  --save-txt --save-conf --exist-ok

# 2. 将 txt 转为 labelImg XML
python3 dataset/yolo2xml.py

# 3. XML 放回对应 batch 目录，用 labelImg 打开审核
```

---

## 遇到的问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `torch.load` 报 `weights_only` 错误 | PyTorch 2.6+ 默认 `weights_only=True` | 在多个文件中加 `weights_only=False` |
| 数据集找不到（Dataset not found） | yaml 中路径与实际目录名不符 | 修正 yaml 指向正确目录，txt 路径同步修改 |
| 后台进程被杀（nohup 方式） | shell 会话结束时 SIGHUP 传播 | 改用 tmux 运行训练 |
| GPU 显存不足 | vLLM Worker 各占 ~14GB | 使用 batch-size 2，GPU 1 显存较空 |
| 空标注 XML 残留 | labelImg 清空标注后仍生成空 XML | 脚本扫描删除无 `<object>` 的 XML |
| 首次预标注失败 | exp4 模型精度不足(mAP=0.488) | 模型提升至 mAP=0.810 后重新预标注 |
| `pre_annotate.py` 坐标偏移 | 脚本内坐标转换逻辑有 bug | 改用 detect.py 原生推理 + yolo2xml.py 独立转换 |
| `attempt_load` 报 git 错误 | 非 git 仓库，attempt_download 失败 | detect.py 原生调用无需 attempt_download |

---

## 目录结构总览

```tree
/data2/ai/yolov7-main-WFS/
├── cfg/training/
│   ├── yolov7.yaml               # 原始 80 类配置
│   └── yolov7_my.yaml            # 车灯检测 2 类配置
├── data/
│   ├── my_yolo_dataset.yaml      # 数据集配置（当前指向 try5）
│   ├── hyp.scratch.custom.yaml   # 超参数
│   └── coco_my.yaml              # 旧的数据集配置（未使用）
├── dataset/
│   ├── batch_1/                  # 原始人工标注（235 有效）
│   ├── batch_2/                  # 原始人工标注（224 有效）
│   ├── batch_3/                  # 原始人工标注（165 有效）
│   ├── batch_4/                  # 原始人工标注（145 有效）
│   ├── batch_5/                  # 原始人工标注（170 有效）
│   ├── batch_6/                  # 原始人工标注（102 有效）
│   ├── batch_7/                  # 原始人工标注（166 有效）
│   ├── batch_8/                  # 原始人工标注（142 有效）
│   ├── batch_9/                  # 原始人工标注（156 有效）
│   ├── dataset2/
│   │   ├── batch_1/              # 预标注审核后（271 有效）
│   │   ├── batch_2/              # 预标注审核后（283 有效）
│   │   ├── batch_3/              # 预标注审核后（257 有效）
│   │   └── batch_4/              # 预标注审核后（160 有效）
│   ├── wait_for_tag_dataset/     # 废弃（首次预标注失败数据）
│   ├── yolo_dataset_try1/        # 第一轮数据集（510 样本）
│   ├── yolo_dataset_try2/        # 第二轮数据集（990 样本）
│   ├── yolo_dataset_try3/        # 第三/四轮数据集（1041 样本）
│   ├── yolo_dataset_try4/        # 第五/六轮数据集（1505 样本）
│   ├── yolo_dataset_try5/        # 第七轮数据集（2476 样本，当前最佳）
│   ├── make_dataset.py           # XML→YOLO + 数据划分脚本
│   ├── analyze_test.py           # 逐张测试分析脚本
│   ├── yolo2xml.py               # YOLO txt → labelImg XML 转换脚本
│   └── pre_annotate.py           # 早期预标注脚本（已弃用，保留备用）
├── weights/
│   └── yolov7.pt                 # COCO 预训练权重
├── runs/
│   ├── train/
│   │   ├── yolo_light_exp16/     # 第一轮训练
│   │   ├── yolo_light_exp2/      # 第二轮训练
│   │   ├── yolo_light_exp3/      # 第三轮训练
│   │   ├── yolo_light_exp4/      # 第四轮训练
│   │   ├── yolo_light_exp5/      # 第五轮训练（640, 1505样本）
│   │   ├── yolo_light_exp6/      # 第六轮训练（1280, 200轮）
│   │   └── yolo_light_exp7/      # 第七轮训练（1280, 2476样本, 当前最佳）
│   ├── test/
│   │   ├── exp/ ~ exp5/          # 第1-5轮测试
│   │   ├── exp7/                 # 第六轮测试
│   │   └── exp8/                 # 第七轮测试
│   └── detect/
│       ├── test_results/         # 第1轮逐张检测
│       ├── test_results2/        # 第2轮逐张检测
│       ├── test_results5/        # 第5轮逐张检测
│       ├── test_results6/        # 第6轮逐张检测
│       └── test_results7/        # 第7轮逐张检测（当前最佳）
├── train.py                      # 训练入口（已修改 torch.load）
├── test.py                       # 测试/评估脚本
├── detect.py                     # 推理检测脚本
├── export.py                     # 模型导出脚本（ONNX/TensorRT）
├── 第一周.txt                    # 第一周工作总结
├── 车灯检测.md                   # 本文档
└── train*.log                    # 各轮训练日志

/data2/ai/dataset2/               # 预标注数据（独立目录，待审核）
├── batch_1/                      # 331 XML
├── batch_2/                      # 328 XML
├── batch_3/                      # 322 XML
├── batch_4/                      # 204 XML
├── batch_5/                      # 336 XML
├── batch_6/                      # 308 XML
├── batch_7/                      # 336 XML
├── batch_8/                      # 254 XML
└── batch_9/                      # 323 XML
```

---

## 后续计划

### 已完成

- [x] batch_1~9 纯人工标注（1505 个有效标注）
- [x] 第1~4轮训练：mAP@.5 从 0.224 提升至 0.488
- [x] 第5轮训练（640, 1505样本）mAP@.5=0.766
- [x] 第6轮训练（1280, 200ep）mAP@.5=0.810，模型可用于预标注
- [x] 用 exp6 模型对 /data2/ai/dataset2 预标注（2742 XML）
- [x] 审核 dataset2/batch_1~4（971 样本）并入训练集
- [x] 第7轮训练（1280, 200ep, 1733样本）mAP@.5=0.880

### 进行中 / 待办

- [ ] 审核剩余预标注数据（/data2/ai/dataset2/batch_1~9, 2742 XML），预计扩充至 4000+ 样本
- [ ] 生成 yolo_dataset_try6，启动第8轮训练（1280, 200ep, 预计 1 天）
- [ ] 第8轮训练后测试集评估与逐张分析
- [ ] 调优 conf 阈值（0.3 / 0.4）平衡 Precision 与 Recall
- [ ] 用 best.pt 在实际视频上验证检测效果，验证时序一致性
- [ ] 如效果达标，导出模型（export.py 导出 ONNX/TensorRT），部署到推理环境

---

> [!quote] 项目文档版本
> 最后更新: 2026-07-27
> 维护者: ai
> 相关文件: [[make_dataset.py]] · [[analyze_test.py]] · [[yolo2xml.py]] · [[pre_annotate.py]]