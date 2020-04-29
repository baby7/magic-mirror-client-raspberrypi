#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
from conf import settings

path = settings.OPEN_CV_DIR    # open-cv文件夹位置
focus = settings.FOCUS_FACE     # 人脸识别文件名称
print(path + focus + ".xml")
# 创建 classifier
clf = cv2.CascadeClassifier(path + focus + ".xml")


# 识别
def recognition(image):
    global clf
    # 设定灰度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 识别
    faces = clf.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # 判断是否有人脸
    if not len(faces) is 0:
        something()
    else:
        print("Null")


# something
def something():
    print("检测到人脸")


def face_detection():
    cap = cv2.VideoCapture(0)               # 从摄像头中取得视频
    while cap.isOpened():
        ret, frame = cap.read()             # 读取帧摄像头
        if ret is True:
            # 输出当前帧
            recognition(frame)
            time.sleep(1)
        else:
            break
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
