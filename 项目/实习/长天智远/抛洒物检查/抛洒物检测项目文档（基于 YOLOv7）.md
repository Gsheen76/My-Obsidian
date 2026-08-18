---

tags:

  - yolo

  - object-detection

  - cv

  - 项目文档

aliases:

  - 抛洒物检测

  - 抛洒物目标检测

created: 2026-08-11

updated: 2026-08-18

---

  

# 抛洒物检测项目文档（基于 YOLOv7）

  

## 概述

  

本项目基于 **YOLOv7** 框架检测高速公路路面上的抛洒物/障碍物（锥桶、抛洒物、标线、箭头、阴影等），从已有 3 类抛洒物模型 `/data2/ai/weight/best_drip_1280.pt` 迁移，先训练阶段1（100 轮）验证可行性，再从阶段1 best 权重续训阶段2（200 轮）提升精度。

  

| 项目 | 说明 |

|------|------|

| 项目根目录 | `/data2/ai/yolov7-main-WFS` |

| 源数据目录 | `/data2/ai/dataset_drip`（images2 / labels2，VOC XML） |

| 数据集目录 | `dataset/yolo_dataset_drop`（7:2:1 划分） |

| 检测类别 | 5 类 —— `cone bucket`(0)、`throwing materials`(1)、`yinying`(2)、`line`(3)、`arrow`(4) |

| 初始权重 | `/data2/ai/weight/best_drip_1280.pt`（3 类，nc=3 → nc=5 迁移） |

| 硬件环境 | 2 × NVIDIA A10（各 23GB 显存） |

| 当前最佳模型 | `runs_drop/drop_train2/weights/best.pt`（阶段2 最终，200 轮） |

| 训练配置 | batch 8（每卡 4）、img-size 1280、device 0,1 |

| 测试集最终指标 | Precision=0.903 / Recall=0.953 / **F1=0.927**（IoU=0.5，269 图） |

  

> [!note] 评估口径

> 本项目的"测试集指标"均为 `eval_drop_test.py` 对 detect.py 输出（conf=0.25, IoU=0.5）逐框比对计算，非官方 test.py 的 mAP 曲线指标；两类口径不可直接比较。

  

---

  

## 项目时间线

  

```mermaid

gantt

    title 抛洒物检测项目历程

    dateFormat YYYY-MM-DD

    section 数据处理

    dataset_drip 读取与清洗      :done, d1, 2026-08-11, 2d

    7:2:1 数据划分               :done, d2, after d1, 1d

    section 训练

    阶段1 100轮 (drop_train)     :done, t1, 2026-08-14, 2d

    阶段2 200轮 至172轮(中断)    :done, t2, after t1, 2d

    系统重启/两次resume失败       :done, t3, 2026-08-17, 1d

    阶段2 resume 续跑至199轮      :done, t4, 2026-08-17, 1d

    section 评估

    测试集最终评估                :done, e1, 2026-08-18, 1d

```

  

> [!warning] 中断事故

> 阶段2 训练于 2026-08-16 20:20 中断（tmux 会话丢失，停于 172/199），期间系统于 08-17 09:56 重启；两次 nohup resume 静默失败，最终以 `setsid` + `--workers 4` 成功续跑，08-18 00:09 完成 199/199。

  

---

  

## 数据情况

  

### 数据来源与清洗

  

| 数据批次 | 图片来源 | 标注方式 | 说明 |

|----------|----------|----------|------|

| `/data2/ai/dataset_drip/images2` | 监控视频抽帧 | VOC XML 人工标注 | 4212 张 jpg，其中 2679 张有标注 |

| `/data2/ai/dataset_drip/labels2` | - | labelImg | 1533 张无标注图片未使用 |

  

**源数据类别统计：**

  

| 类别 | 框数 |

|------|------|

| line（标线） | 95306 |

| throwing materials（抛洒物） | 3875 |

| cone bucket（锥形桶） | 3584 |

| arrow（箭头） | 2656 |

| yinying（阴影） | 73 |

| `\`（异常类） | 1 |

  

> [!caution] 清洗记录

> 异常类别 `\`（`labels2/video_351_240.xml`，1 个对象）不属于 5 类体系，删除该对象（49→48），原 XML 已备份为 `.bak`。`make_drop_dataset.py` 转换时也只保留 5 类白名单。

  

> [!warning] 弱类提示

> yinying 全库仅 73 框（训练集 39 框），是严重的长尾类别。阶段1 测试集 Recall=0.000（4 框全漏）；阶段2 提升至 0.667（4/6）。若要进一步优化需补充该类数据。

  

### 数据划分（7:2:1）

  

使用 `dataset/make_drop_dataset.py`（seed=42 可复现）完成 XML→YOLO txt 转换 + 划分，输出 `dataset/yolo_dataset_drop/`：

  

| 划分 | 图片数 | 说明 |

|------|--------|------|

| train | 1875 | 训练集 |

| val | 535 | 验证集 |

| test | 269 | 测试集（评估用） |

  

**训练集框分布：**

  

| 类别 | 框数 |

|------|------|

| line | 66969 |

| throwing materials | 2673 |

| cone bucket | 2399 |

| arrow | 1815 |

| yinying | 39 |

  

### 输出数据集结构

  

```tree

dataset/yolo_dataset_drop/

├── images/

│   ├── train/    # 1875 张训练图片

│   ├── val/      # 535 张验证图片

│   └── test/     # 269 张测试图片

├── labels/

│   ├── train/    # YOLO txt 标注

│   ├── val/      # YOLO txt 标注

│   └── test/     # YOLO txt 标注

├── train.txt     # 训练集图片绝对路径列表

├── val.txt       # 验证集图片绝对路径列表

└── test.txt      # 测试集图片绝对路径列表

```

  

### YOLO 标注格式

  

每行格式：`class_id center_x center_y width height`（坐标归一化到 0~1）

  

```yaml

0 0.325781 0.481944 0.023438 0.048611   # cone bucket

3 0.741406 0.609722 0.015625 0.006944   # line

```

  

---

  

## 数据处理脚本

  

### make_drop_dataset.py（XML 转 YOLO + 数据划分）

  

**路径**: `dataset/make_drop_dataset.py`

  

**功能**:

1. 遍历 `dataset_drip/images2` + `labels2`，仅保留有 XML 的图片

2. 将 VOC XML 转换为 YOLO txt（归一化坐标），仅保留 5 类白名单（自动丢弃异常类）

3. 按 7:2:1 随机划分 train/val/test（random_seed=42 可复现）

4. 复制图片 + 生成 txt 标注 + 生成 train/val/test.txt 路径列表

  

**用法**:

  

```bash

cd /data2/ai/yolov7-main-WFS

python3 dataset/make_drop_dataset.py

```

  

### eval_drop_test.py（测试集逐框评估）

  

**路径**: `eval_drop_test.py`

  

**功能**: 对比 GT（`dataset/yolo_dataset_drop/labels/test`）与 detect.py 输出 txt（6 列带 conf，脚本按前 5 列处理），贪心匹配 IoU≥0.5 计算 TP/FP/FN、Precision/Recall/F1 及每类 Recall。

  

**用法**:

  

```bash

python3 eval_drop_test.py   # DET_DIR 在脚本顶部，指向对应 detect 输出 labels 目录

```

  

---

  

## 配置文件

  

### 数据集配置 —— my_drop_dataset.yaml

  

**路径**: `data/my_drop_dataset.yaml`

  

```yaml

train: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_drop/train.txt

val: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_drop/val.txt

nc: 5

names: ["cone bucket", "throwing materials", "yinying", "line", "arrow"]

```

  

### 模型配置 —— yolov7_drop.yaml

  

**路径**: `cfg/training/yolov7_drop.yaml`

  

基于标准 `cfg/training/yolov7.yaml` 复制修改，仅改动类别数：

  

```yaml

nc: 5  # number of classes (drip)

```

  

backbone / head / anchors 与标准 yolov7 完全一致（depth/width multiple 1.0）。

  

### 超参数

  

沿用 YOLOv7 默认超参 `data/hyp.scratch.yaml`，未自定义。

  

---

  

## 代码修改记录

  

为兼容 PyTorch 2.6+（`torch.load` 默认 `weights_only=True`），修改与 [[车灯检测]] 项目一致：

  

| 文件 | 修改内容 |

|------|----------|

| `train.py` (71/87) | `torch.load(...)` → 加 `weights_only=False` |

| `utils/datasets.py` (392) | 同上 |

| `utils/general.py` (802) | 同上 |

  

> [!important] 类别数迁移

> 初始权重 `/data2/ai/weight/best_drip_1280.pt` 为 3 类（nc=3），本项目 5 类。train.py 的 `intersect_dicts` 自动跳过 head 层不匹配参数：阶段1 Transferred 552/566，阶段2 564/566（head 已从阶段1 学得，直接复用）。

  

---

  

## 训练记录

  

### 各阶段结果对比（验证集）

  

| 指标 | 阶段1 (100轮) | 阶段2 (200轮) | 阶段2 中断点(172) |

|------|---------------|---------------|-------------------|

| 实验目录 | `drop_train` | `drop_train2` | 同左 |

| 初始权重 | best_drip_1280.pt | 阶段1 best.pt | - |

| epochs | 100 | 200 | 172/199 |

| batch | 4→8 | 8 | 8 |

| img-size | 1280 | 1280 | 1280 |

| Precision | 0.718 | **0.907** | 0.911 |

| Recall | 0.679 | **0.849** | 0.841 |

| mAP@.5 | 0.664 | **0.824** | 0.839 |

| mAP@.5:.95 | 0.442 | **0.518** | 0.533 |

  

> [!tip] 关键节点

> - **阶段1**：从 3 类权重迁移 + 100 轮训练验证可行，测试集 F1=0.911，但 yinying 全漏（R=0.000）

> - **阶段2**：从阶段1 best 权重续训 200 轮，mAP@.5 0.664→0.824，yinying 测试集 Recall 0→0.667

> - 中断点 172 轮曾达 mAP@.5=0.839（全流程峰值），最终 199 轮 0.824 为收敛稳定值

  

**阶段2 关键轮次曲线：**

  

| epoch | Precision | Recall | mAP@.5 | mAP@.5:.95 |

|-------|-----------|--------|--------|------------|

| 0（续训起点） | 0.709 | 0.677 | 0.658 | 0.441 |

| 49 | 0.880 | 0.754 | 0.741 | 0.473 |

| 99 | 0.912 | 0.815 | 0.818 | 0.517 |

| 149 | 0.902 | 0.834 | 0.814 | 0.526 |

| **199（最终）** | **0.907** | **0.849** | **0.824** | **0.518** |

  

> [!success] 最佳模型

> 阶段2 最终 `runs_drop/drop_train2/weights/best.pt`

> 测试集（269 图, conf=0.25, IoU=0.5）: Precision=0.903 Recall=0.953 **F1=0.927**

  

### 测试集最终评估（阶段2）

  

**总体：** TP=10326 / FP=1109 / FN=511 → Precision=0.9030 / Recall=0.9528 / F1=0.9273

  

| 类别 | TP | FN | Recall | vs 阶段1 |

|------|-----|-----|--------|----------|

| line | 9285 | 374 | **0.961** | 0.956 |

| throwing materials | 371 | 37 | **0.909** | 0.845 ↑ |

| arrow | 313 | 42 | **0.882** | 0.873 |

| cone bucket | 353 | 56 | **0.863** | 0.849 |

| **yinying** | 4 | 2 | **0.667** | 0.000 ↑↑ |

  

检测效果图：`runs_drop/drop_test_final/`（269 张，含标注框与标签）。

  

> [!note] 已知漏检

> `video_279_585.jpg` GT 有 1 框但检测输出为空，属漏检案例（测试集全部漏检中仅此 1 张全空）。

  

### 第一阶段训练（drop_train）—— 100 轮

  

- 数据集: yolo_dataset_drop（train 1875 / val 535 / test 269）

- 初始权重: `/data2/ai/weight/best_drip_1280.pt`（3 类），迁移 552/566

- epochs: 100，batch-size: 4 → **8**（用户要求 batch 8，显存 12.6G/卡），img-size: 1280

- 训练完成 100/100，best.pt fitness=0.46977

  

**测试集结果（conf=0.25, IoU=0.5）：** Precision=0.880 / Recall=0.944 / F1=0.911（yinying R=0.000）

检测输出：`runs_drop/drop_test_infer/`

  

### 第二阶段训练（drop_train2）—— 200 轮（含中断恢复）

  

- 初始权重: 阶段1 best.pt（用户要求从最好模型续跑 200 轮）

- epochs: 200，batch-size: 8，img-size: 1280，迁移 564/566

- 每轮约 20-30 分钟（235 iters，约 5-8s/it）

  

**中断与恢复经过：**

  

| 时间 | 事件 |

|------|------|

| 08-15 晚 | 阶段2 启动 |

| 08-16 20:20 | tmux 会话丢失，训练停于 172/199（last.pt 已保存） |

| 08-17 09:56 | **系统重启**（内核 5.15.0-187，顺带杀掉所有残留进程） |

| 08-17 10:19 | 第1次 nohup resume 启动即失败（日志 0 字节） |

| 08-17 11:03 | 第2次 nohup resume 跑 6 个 batch 后静默消失（无报错，非 OOM） |

| 08-17 14:49 | 第3次 `setsid` + `--workers 4` resume 成功 |

| 08-18 00:09 | 训练完成 199/199，best.pt / last.pt 落盘 |

  

> [!important] 恢复方法

> `--resume` 指向 `last.pt` 即可从断点续跑（轮次/优化器状态全部保留）。resume 读取 checkpoint 内保存的 opt（epochs=200、batch 8、1280、device 0,1、project runs_drop、name drop_train2），无需再传这些参数。

  

### 训练命令

  

```bash

# 阶段1（首训）

cd /data2/ai/yolov7-main-WFS

python3 train.py \

  --weights /data2/ai/weight/best_drip_1280.pt \

  --cfg cfg/training/yolov7_drop.yaml \

  --data data/my_drop_dataset.yaml \

  --epochs 100 \

  --batch-size 8 \

  --img-size 1280 1280 \

  --device 0,1 \

  --project runs_drop --name drop_train \

  --workers 4

  

# 阶段2（从阶段1 best 续训）

python3 train.py \

  --weights runs_drop/drop_train/weights/best.pt \

  --cfg cfg/training/yolov7_drop.yaml \

  --data data/my_drop_dataset.yaml \

  --epochs 200 \

  --batch-size 8 \

  --img-size 1280 1280 \

  --device 0,1 \

  --project runs_drop --name drop_train2

  

# 断点恢复（推荐 setsid，避免会话/终端退出被杀）

setsid nohup python3 -u train.py \

  --resume runs_drop/drop_train2/weights/last.pt \

  --device 0,1 --workers 4 \

  > runs_drop/train_drop_resume3.log 2>&1 < /dev/null &

  

# 监控

tail -f runs_drop/train_drop_resume3.log

```

  

> [!warning] 运行环境教训

> - tmux / 普通 nohup 在本机均出现过会话丢失或进程静默消失，`setsid nohup ... < /dev/null` 最稳

> - 系统存在无人值守重启风险（内核从 5.15.0-186 升级到 187），长训练必须断点可恢复（last.pt 每轮都存）

  

---

  

## 推理 / 测试

  

### 测试集检测

  

```bash

cd /data2/ai/yolov7-main-WFS

python3 detect.py \

  --weights runs_drop/drop_train2/weights/best.pt \

  --source dataset/yolo_dataset_drop/images/test \

  --img-size 1280 \

  --conf-thres 0.25 \

  --device 1 \

  --save-txt --save-conf \

  --project runs_drop --name drop_test_final --exist-ok

  

# 评估（先改 eval_drop_test.py 的 DET_DIR 指向上述输出 labels 目录）

python3 eval_drop_test.py

```

  

### 单张图片检测

  

```bash

python3 detect.py \

  --weights runs_drop/drop_train2/weights/best.pt \

  --source /path/to/image.jpg \

  --img-size 1280 --conf-thres 0.25 --device 1

```

  

> [!info] detect 输出格式

> detect.py 保存的 txt 为 6 列（含 conf）：`class conf cx cy w h`；GT 为 5 列。`eval_drop_test.py` 只取前 5 列，兼容。

  

---

  

## 相关实验：强光抑制滤波（已搁置）

  

在抛洒物任务前，为处理监控强光/过曝场景做过滤波实验：

  

- `filter_glare.py`：`homomorphic(gamma_h=0.6, gamma_l=0.75, cutoff=0.15, ds=4)` 与 `guided_glare(r=16, eps=0.02, compress=2.2, detail=1.15, ds=4)`

- 两者均带 `hl_thresh=190, hl_feather=30`：**仅压缩 V>190 高亮区**（160-190 为羽化过渡带），暗区改动 0.000%

- `run_red_filter.py` 批处理 → `run_red_homomorphic/`、`run_red_guided/` 各 248 图（xml 同步）

  

**车灯检测（exp16）对比：**

  

| 处理 | 检出框数 |

|------|----------|

| 原图 | 229 |

| 强光抑制(仅高亮) | 97 |

| 同态滤波 | 87 |

| 引导滤波 | 105 |

  

> [!caution] 结论（搁置原因）

> 抑制强光后车灯类检测数大幅下降——车灯本身处于高亮区，压光会连带削弱目标特征。该方案对"防过曝"有利但对目标检测不利，暂不引入训练/推理流程。脚本保留备用。

  

---

  

## 遇到的问题与解决方案

  

| 问题 | 原因 | 解决方案 |

|------|------|----------|

| 源数据存在异常类别 `\` | 标注误填类别名 | 删除该对象，XML 备份 `.bak`；转换脚本白名单过滤 |

| yinying 测试集 R=0.000 | 训练集仅 39 框，长尾过弱 | 阶段2 加训 200 轮后提升至 0.667 |

| 阶段1 训练过慢 | batch 4 利用率低 | 改 batch 8（双卡各 4，12.6G/卡）重跑 |

| 阶段2 中断于 172/199 | tmux 会话丢失（原因不明） | `--resume last.pt` 断点续跑 |

| 系统重启杀进程 | 内核 5.15.0-186→187 自动升级重启 | resume 恢复；长训练依赖 last.pt 每轮存档 |

| 两次 nohup resume 静默失败 | 第1次日志 0 字节；第2次跑 6 batch 消失（无报错、非 OOM） | 改用 `setsid nohup ... < /dev/null` + `--workers 4` 成功 |

| `torch.load` 报 `weights_only` 错误 | PyTorch 2.6+ 默认 `weights_only=True` | 多处加 `weights_only=False`（见代码修改记录） |

| 类别数不匹配 (nc=3 → nc=5) | 初始权重 head 层维度不同 | `intersect_dicts` 自动跳过不匹配层，head 从头训练 |

  

---

  

## 目录结构总览

  

```tree

/data2/ai/yolov7-main-WFS/

├── cfg/training/

│   └── yolov7_drop.yaml            # 抛洒物 5 类配置

├── data/

│   └── my_drop_dataset.yaml        # 抛洒物数据集配置

├── dataset/

│   ├── make_drop_dataset.py        # XML→YOLO + 7:2:1 划分

│   └── yolo_dataset_drop/          # 划分后数据集（train 1875 / val 535 / test 269）

├── eval_drop_test.py               # 测试集逐框评估脚本

├── runs_drop/

│   ├── drop_train/                 # 阶段1训练（100轮）

│   │   └── weights/best.pt

│   ├── drop_train2/                # 阶段2训练（200轮, 最终 best.pt）

│   │   ├── weights/best.pt  last.pt  epoch_*.pt

│   │   └── results.txt  曲线图

│   ├── drop_test_infer/            # 阶段1测试集检测输出

│   ├── drop_test_final/            # 阶段2测试集检测输出（最终评估）

│   ├── train_drop_resume.log       # 失败 resume 日志（0 字节）

│   ├── train_drop_resume2.log      # 失败 resume 日志（停于 6/235 batch）

│   └── train_drop_resume3.log      # 成功 resume 日志

├── filter_glare.py                 # 强光抑制滤波（同态/引导, 已搁置）

├── run_red_filter.py               # 滤波批处理脚本

├── run_red_homomorphic/            # 滤波产物（248图）

├── run_red_guided/                 # 滤波产物（248图）

├── train.py / detect.py / test.py  # yolov7 主程序

└── 车灯检测.md / 抛洒物检测.md       # 项目文档

  

/data2/ai/dataset_drip/             # 源数据

├── images2/                        # 4212 张 jpg

└── labels2/                        # 2679 个 XML（含 1 个 .bak 备份）

  

/data2/ai/weight/best_drip_1280.pt  # 初始 3 类权重（迁移来源）

```

  

---

  

## 后续计划

  

### 已完成

  

- [x] dataset_drip 读取与清洗（4212 图 / 2679 XML，清除异常类 `\`）

- [x] 7:2:1 数据划分 yolo_dataset_drop（train 1875 / val 535 / test 269）

- [x] 阶段1 训练 100 轮（mAP@.5=0.664，测试集 F1=0.911）

- [x] 阶段2 训练 200 轮（含中断 + resume 恢复，mAP@.5=0.824）

- [x] 测试集最终评估（P=0.903 / R=0.953 / F1=0.927，yinying 0→0.667）

  

### 进行中 / 待办

  

- [ ] 真实监控视频检测验证（`/data2/ai/video/` 下 4 个 mp4 已列为候选源）

- [ ] 补充 yinying（阴影）类训练数据，缓解长尾（当前测试集仅 6 框、2 漏检）

- [ ] 如精度有进一步提升需求，从阶段2 best.pt 启动阶段3 续训

- [ ] 导出部署（export.py 导出 ONNX / TensorRT）

- [ ] 强光抑制滤波方案是否在训练增强中引入（当前实验显示会削弱检测，已搁置）

  

---

  

> [!quote] 项目文档版本

> 最后更新: 2026-08-18

> 维护者: ai

> 相关文件: [[车灯检测]] · [[make_drop_dataset.py]] · [[eval_drop_test.py]]