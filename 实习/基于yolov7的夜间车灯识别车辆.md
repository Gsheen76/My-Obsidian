
> [!服务器]
> P：172.18.80.6
> user：itssky
> passwd：Itssky@321
> 端口号：2222



```shell
cd /data2/ai/yolov7-main-WFS
python3 train.py \
-- weights weights/yolov7.pt \
-- cfg cfg/training/yolov7_my. yaml
-- data data/my_yolo_dataset.yaml \

-- hyp data/hyp. scratch.custom. yaml
-- epochs 100 \
-- batch-size 4 \
-- img-size 640 640
-- device 0 \
-- name yolo_light_exp1 \
-- workers 4
```

## 1. 项目概述

  

本项目通过检测车辆车灯（前灯 head / 尾灯 tail）来识别车辆，基于 **YOLOv7** 目标检测框架实现。

- **项目根目录**: `/data2/ai/yolov7-main-WFS`

- **数据集目录**: `/data2/ai/yolov7-main-WFS/dataset`

- **检测类别**: 2 类 —— `head`（前灯, class 0）、`tail`（尾灯, class 1）

- **标注工具**: labelImg（VOC XML 格式标注）

- **硬件环境**: 2 × NVIDIA A10（各 23GB 显存）

---

  

## 2. 数据情况

  

### 2.1 原始数据

  

| 项目 | 说明 |

|------|------|

| 图片总数 | 1000 张 .jpg |

| 标注总数 | 510 个 .xml（即可用数据） |

| 图片来源 | 从视频抽帧获得 |

| 标注格式 | labelImg 生成的 VOC XML（`<object><name>...</name><bndbox>...`） |

| 类别分布 | head: 642 个框, tail: 932 个框 |

| 原始数据路径 | `dataset/batch_1` 和 `dataset/batch_2` |

  

### 2.2 数据划分（7:2:1）

  

使用 `dataset/make_dataset.py` 脚本完成 XML→YOLO txt 转换 + 数据集划分：

  

| 划分 | 数量 | 比例 |

|------|------|------|

| train（训练集） | 357 | 70% |

| val（验证集） | 102 | 20% |

| test（测试集） | 51 | 10% |

  

### 2.3 输出数据集结构

  

```

dataset/yolo_dataset_try1/

├── images/

│   ├── train/    # 357 张训练图片

│   ├── val/      # 102 张验证图片

│   └── test/     # 51 张测试图片

├── labels/

│   ├── train/    # 357 个 YOLO txt 标注

│   ├── val/      # 102 个 YOLO txt 标注

│   └── test/     # 51 个 YOLO txt 标注

├── train.txt     # 训练集图片绝对路径列表

├── val.txt       # 验证集图片绝对路径列表

├── test.txt      # 测试集图片绝对路径列表

├── train.cache   # 训练集缓存

└── val.cache     # 验证集缓存

```

  

### 2.4 YOLO 标注格式

  

每行格式：`class_id center_x center_y width height`（坐标归一化到 0~1）

  

示例：

```

0 0.232422 0.309028 0.027344 0.018056   # head

1 0.260547 0.238889 0.017969 0.013889   # tail

```

  

---

  

## 3. 数据处理脚本

  

### 3.1 make_dataset.py（XML 转 YOLO + 数据划分）

  

**路径**: `dataset/make_dataset.py`

  

**功能**:

1. 遍历 `batch_1` 和 `batch_2` 目录，收集所有有 XML 标注的样本

2. 将 VOC XML 格式转换为 YOLO txt 格式（归一化坐标）

3. 按 7:2:1 比例随机划分 train/val/test（random_seed=42 保证可复现）

4. 复制图片到对应目录，生成 YOLO txt 标注文件

5. 生成 train.txt / val.txt / test.txt 路径列表文件

  

**用法**:

```bash

cd /data2/ai/yolov7-main-WFS/dataset

python3 make_dataset.py

```

  

**关键配置**:

```python

src_dirs = [

    "/data2/ai/yolov7-main-WFS/dataset/batch_1",

    "/data2/ai/yolov7-main-WFS/dataset/batch_2",

]

out_root = "/data2/ai/yolov7-main-WFS/dataset/yolo_dataset"

classes = {"head": 0, "tail": 1}

train_ratio = 0.7

val_ratio   = 0.2

test_ratio  = 0.1

random_seed = 42

```

  

> **注意**: 脚本中 `out_root` 默认输出到 `yolo_dataset`，实际数据在 `yolo_dataset_try1` 目录（之前多次实验产生的）。`my_yolo_dataset.yaml` 已指向 `yolo_dataset_try1`。

  

### 3.2 其他数据处理脚本

  

| 脚本 | 功能 |

|------|------|

| `dataset/labelImg2yolo.py` | 单独的 XML→YOLO 转换脚本（原始 Windows 路径版本，未更新） |

| `dataset/mp4_2_pic.py` | 视频抽帧脚本 |

| `dataset/png2jpg.py` | PNG 转 JPG 格式 |

| `dataset/rename_pinyin.py` | 文件名拼音重命名 |

| `dataset/cal_0_txt.py` | 标注统计脚本 |

  

---

  

## 4. 配置文件

  

### 4.1 数据集配置 —— my_yolo_dataset.yaml

  

**路径**: `data/my_yolo_dataset.yaml`

  

```yaml

# 车灯检测数据集 (head/tail) 配置

train: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try1/train.txt

val: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try1/val.txt

test: /data2/ai/yolov7-main-WFS/dataset/yolo_dataset_try1/test.txt

  

nc: 2

names: ["head", "tail"]

```

  

### 4.2 模型配置 —— yolov7_my.yaml

  

**路径**: `cfg/training/yolov7_my.yaml`

  

基于 `cfg/training/yolov7.yaml` 复制修改，仅改动类别数：

  

```yaml

nc: 2  # number of classes (head, tail)，原文件为 nc: 80（COCO）

```

  

其余结构（backbone、head、anchors）与标准 yolov7.yaml 完全一致。

  

### 4.3 超参数 —— hyp.scratch.custom.yaml

  

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

  

## 5. 代码修改记录

  

为兼容 PyTorch 2.6+（`torch.load` 默认 `weights_only=True`），修改了以下文件：

  

### 5.1 train.py

  

```python

# 第71行（修改前）

run_id = torch.load(weights, map_location=device).get('wandb_id') ...

# 第71行（修改后）

run_id = torch.load(weights, map_location=device, weights_only=False).get('wandb_id') ...

  

# 第87行（修改前）

ckpt = torch.load(weights, map_location=device)

# 第87行（修改后）

ckpt = torch.load(weights, map_location=device, weights_only=False)

```

  

### 5.2 utils/datasets.py

  

```python

# 第392行（修改前）

cache, exists = torch.load(cache_path), True

# 第392行（修改后）

cache, exists = torch.load(cache_path, weights_only=False), True

```

  

> `models/experimental.py` 第252行已经是 `weights_only=False`，无需修改。

> `detect.py` 第48行加载 resnet101 的 `torch.load` 未修改（暂不影响训练）。

  

---

  

## 6. 训练

  

### 6.1 训练参数

  

| 参数 | 值 | 说明 |

|------|-----|------|

| weights | weights/yolov7.pt | COCO 预训练权重 |

| cfg | cfg/training/yolov7_my.yaml | 2 类模型配置 |

| data | data/my_yolo_dataset.yaml | 数据集配置 |

| hyp | data/hyp.scratch.custom.yaml | 超参数 |

| epochs | 100 | 训练轮数 |

| batch-size | 4 | 批大小（受显存限制） |

| img-size | 640 640 | 输入尺寸 |

| device | 0 | GPU 0 |

| workers | 4 | 数据加载线程数 |

  

### 6.2 训练命令

  

**前台运行**:

```bash

cd /data2/ai/yolov7-main-WFS

python3 train.py \

  --weights weights/yolov7.pt \

  --cfg cfg/training/yolov7_my.yaml \

  --data data/my_yolo_dataset.yaml \

  --hyp data/hyp.scratch.custom.yaml \

  --epochs 100 \

  --batch-size 4 \

  --img-size 640 640 \

  --device 0 \

  --name yolo_light_exp1 \

  --workers 4

```

  

**tmux 后台运行（推荐）**:

```bash

tmux new-session -d -s yolo_train "cd /data2/ai/yolov7-main-WFS && python3 train.py \

  --weights weights/yolov7.pt \

  --cfg cfg/training/yolov7_my.yaml \

  --data data/my_yolo_dataset.yaml \

  --hyp data/hyp.scratch.custom.yaml \

  --epochs 100 \

  --batch-size 4 \

  --img-size 640 640 \

  --device 0 \

  --name yolo_light_exp1 \

  --workers 4 2>&1 | tee train.log"

```

  

### 6.3 tmux 常用命令

  

```bash

tmux attach -t yolo_train         # 进入 tmux 会话查看实时输出

# 在 tmux 内按 Ctrl+B 然后 D      # 退出 tmux（不停止训练）

tmux ls                           # 查看所有 tmux 会话

tmux kill-session -t yolo_train   # 停止训练并关闭会话

tail -f /data2/ai/yolov7-main-WFS/train.log   # 查看训练日志

```

  

### 6.4 训练状态

  

- **实验名称**: yolo_light_exp16（runs/train 下第16次实验）

- **输出目录**: `runs/train/yolo_light_exp16/`

- **预训练迁移**: 552/566 参数从 yolov7.pt 迁移成功

- **GPU 显存占用**: ~3.73GB / 23GB

- **训练速度**: ~6-7 it/s，每 epoch 约 13 秒

- **初始 loss**: ~0.14（epoch 0），已降到 ~0.08（epoch 4+）

  

### 6.5 训练输出文件

  

```

runs/train/yolo_light_exp16/

├── weights/

│   ├── best.pt          # 最优权重（285MB）

│   ├── last.pt          # 最后一轮权重（285MB）

│   ├── epoch_000.pt     # 第0轮检查点

│   ├── epoch_024.pt     # 第24轮检查点

│   └── init.pt          # 初始化权重（143MB）

├── results.txt          # 每轮训练/验证指标记录

├── hyp.yaml             # 超参数备份

├── opt.yaml             # 训练参数备份

├── train_batch0~9.jpg   # 训练批次可视化

└── events.out.tfevents.*  # TensorBoard 日志

```

  

### 6.6 训练日志查看

  

```bash

# 实时日志

tail -f train.log

  

# TensorBoard（如安装）

tensorboard --logdir runs/train --host 0.0.0.0 --port 6006

  

# 查看每轮指标

cat runs/train/yolo_light_exp16/results.txt

```

  

results.txt 各列含义：

```

Epoch | gpu_mem | box | obj | cls | total | labels | img_size | P | R | mAP@.5 | mAP@.5:.95 | val/box | val/obj | val/cls

```

  

---

  

## 7. 推理/测试

  

### 7.1 检测单张图片

  

```bash

python3 detect.py \

  --weights runs/train/yolo_light_exp16/weights/best.pt \

  --source /path/to/image.jpg \

  --img-size 640 \

  --conf-thres 0.25 \

  --iou-thres 0.45

```

  

### 7.2 测试集评估

  

```bash

python3 test.py \

  --weights runs/train/yolo_light_exp16/weights/best.pt \

  --data data/my_yolo_dataset.yaml \

  --task test \

  --img-size 640 \

  --conf-thres 0.001 \

  --iou-thres 0.65

```

  

### 7.3 视频检测

  

```bash

python3 detect.py \

  --weights runs/train/yolo_light_exp16/weights/best.pt \

  --source /path/to/video.mp4 \

  --img-size 640

```

  

---

  

## 8. 遇到的问题与解决方案

  

| 问题 | 原因 | 解决方案 |

|------|------|----------|

| `torch.load` 报 `weights_only` 错误 | PyTorch 2.6+ 默认 `weights_only=True` | 在 `train.py`、`utils/datasets.py` 中加 `weights_only=False` |

| 数据集找不到（Dataset not found） | yaml 中路径与实际目录名不符 | 修正 yaml 指向 `yolo_dataset_try1`，txt 路径同步修改 |

| 后台进程被杀（nohup 方式） | shell 会话结束时 SIGHUP 传播 | 改用 tmux 运行训练 |

| GPU 显存不足 | vLLM Worker 各占 ~19GB | 使用 batch-size 4，显存占用 ~3.7GB 可正常运行 |

  

---

  

## 9. 目录结构总览

  

```

/data2/ai/yolov7-main-WFS/

├── cfg/

│   └── training/

│       ├── yolov7.yaml          # 原始 80 类配置

│       └── yolov7_my.yaml       # 车灯检测 2 类配置（新建）

├── data/

│   ├── my_yolo_dataset.yaml     # 车灯检测数据集配置（新建）

│   ├── hyp.scratch.custom.yaml  # 超参数

│   └── coco_my.yaml             # 旧的数据集配置（未使用）

├── dataset/

│   ├── batch_1/                 # 原始数据批1（jpg+xml）

│   ├── batch_2/                 # 原始数据批2（jpg+xml）

│   ├── yolo_dataset_try1/       # 划分好的 YOLO 格式数据集

│   │   ├── images/{train,val,test}/

│   │   ├── labels/{train,val,test}/

│   │   └── {train,val,test}.txt

│   ├── make_dataset.py          # XML转YOLO+数据划分脚本（已更新）

│   ├── labelImg2yolo.py         # XML转YOLO脚本（旧版，未更新）

│   └── *.py                     # 其他数据处理脚本

├── weights/

│   └── yolov7.pt                # COCO 预训练权重

├── runs/

│   └── train/

│       └── yolo_light_exp16/    # 当前训练实验

│           ├── weights/best.pt  # 最优模型

│           └── results.txt      # 训练记录

├── train.py                     # 训练入口（已修改 torch.load）

├── test.py                      # 测试/评估脚本

├── detect.py                    # 推理检测脚本

└── train.log                    # 训练日志

```

  

---

  

## 10. 后续计划

  

- [ ] 等训练完成（100 epochs），查看 `results.txt` 分析 mAP 表现

- [ ] 使用 `test.py` 在测试集上评估最佳模型

- [ ] 用 `detect.py` 实际检测视频验证效果

- [ ] 如效果不足，考虑：

  - 增加标注数据

  - 调整超参数（学习率、数据增强等）

  - 增大 batch-size（需 GPU 显存充足时）

  - 尝试 yolov7x 等更大模型