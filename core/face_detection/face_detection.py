#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import cv2
import time
from conf import settings
import requests

path = settings.OPEN_CV_DIR    # open-cv文件夹位置
focus = settings.FOCUS_FACE     # 人脸识别文件名称
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
        face_path = str(int(round(time.time() * 1000))) + ".png"
        cv2.imwrite(face_path, image)
        emotion_recognition(face_path)
    else:
        print("no face detected")


# 进行情绪识别
def emotion_recognition(face_path):
    url = "http://3cw0735693.qicp.vip/emotionRecognition"
    file = open(face_path, 'rb')
    # 拼接参数
    files = {'file': (str(int(round(time.time() * 1000))), file, 'image/jpg')}
    # 发送请求
    print("send face data success")
    res = requests.post(url, files=files)
    # 获取服务器返回的信息
    print(res.json())
    file.close()
    os.remove(face_path)


def face_detection():
    cap = cv2.VideoCapture(0)               # 从摄像头中取得视频
    while cap.isOpened():
        ret, frame = cap.read()             # 读取帧摄像头
        if ret is True:
            # 输出当前帧
            recognition(frame)
        else:
            break
        time.sleep(3)
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

face_detection()