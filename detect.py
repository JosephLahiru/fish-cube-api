# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license

import os
import sys
from pathlib import Path

import torch

# Model
from models.common import DetectMultiBackend

# Dataloader
from utils.dataloaders import LoadImages

# General
from utils.general import (check_img_size, non_max_suppression, scale_boxes, xyxy2xywh)

# Torch Utils
from utils.torch_utils import select_device, smart_inference_mode


# (Other imports and utility functions)

@smart_inference_mode()
def run(
    weights='yolov5s.pt',  # model path
    source='data/images',  # file/dir/URL/glob
    imgsz=(640, 640),  # inference size (height, width)
    conf_thres=0.25,  # confidence threshold
    iou_thres=0.45,  # NMS IOU threshold
    max_det=1000,  # maximum detections per image
    device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
    classes=None,  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False,  # class-agnostic NMS
    augment=False,  # augmented inference
    half=False,  # use FP16 half-precision inference
):
    # Initialize
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=False, data=None, fp16=half)
    stride, names = model.stride, model.names
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=model.pt)
    bs = 1  # batch_size

    # Run inference
    model.warmup(imgsz=(1 if model.pt else bs, 3, *imgsz))  # warmup
    detected_objects = []

    for path, im, im0s, vid_cap, s in dataset:
        im = torch.from_numpy(im).to(device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        # Inference
        pred = model(im, augment=augment)
        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0s.shape).round()

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)  # integer class
                    label = f'{names[c]} {conf:.2f}'
                    detected_objects.append((names[c], f'{conf:.2f}'))

    return detected_objects


# Example usage from another script (e.g., main.py)
# from detect import run
# results = run(weights='path/to/weights.pt', source='path/to/source')
# print(results)
