#!/usr/bin/python3
from multiprocessing import Process, Queue

import core.view_html.view_html as view_html
import core.face_detection.face_detection as face_detection
import core.dialogue.snowboy as snowboy
import core.sensor.sensor as sensor


def start():
    print("Start to 4 process...")
    try:
        # 获取用户信息
        user_id = "1"
        # 队列
        queue = Queue()
        # 启动显示视图线程
        print("Start the view html process")
        p_viw_html = Process(target=view_html.viw_html, args=(queue,))
        p_viw_html.start()
        # 启动人脸识别线程
        print("Start the face recognition process")
        p_face_detection = Process(target=face_detection.face_detection)
        p_face_detection.start()
        # 启动语音识别线程
        print("Start the speech recognition process")
        p_snowboy = Process(target=snowboy.snowboy, args=(user_id, queue))
        p_snowboy.start()
        # 启动传感器线程
        print("Start the sensor process")
        p_sensor = Process(target=sensor.sensor, args=(user_id, queue))
        p_sensor.start()
    except Exception as e:
        print("Unexpected error:", e)
    while 1:
        pass
