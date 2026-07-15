
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


