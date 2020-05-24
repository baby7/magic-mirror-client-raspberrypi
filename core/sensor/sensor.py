#!/usr/bin/python3
import paho.mqtt.publish as publish
import requests
import time

from lib import RPi_TH
from lib import RPi_FPM
from lib import configurationUtil
from conf import settings

queue = None


# 发送mqtt消息到服务器
def send_mqtt(message):
    publish.single(settings.TOPIC, message, hostname=settings.HOSTNAME,
                   auth={'username': settings.USERNAME, 'password': settings.PASSWORD})
    print("send message success" + message)


# 获取温湿度
def get_temperature_humidity():
    temperature, humidity, check, tmp = RPi_TH.get_temperature_humidity(settings.CHANNEL)
    if check == tmp:
        print("right[temperature:"+str(temperature)+",humidity:" + str(humidity) + ']')
        return temperature, humidity
    else:
        print("error:[temperature:"+str(temperature)+",humidity:"+str(humidity)+",check:"+str(check)+",tmp:"+str(tmp))
        return -30, -30


# 获取PM2.5(细颗粒物)指数
def get_fine_particulate_matter():
    fine_particulate_matter = 0
    return fine_particulate_matter


# 发送消息
def sensor_success(data={}):
    json_data = {
        "type": "sensor_data",
        "data": data
    }
    queue.put(json_data)


# 检查及修改hass核心配置文件
def check_update_configuration(user_id):
    res = requests.get(settings.HOME_LIST + str(user_id))
    data = res.json()
    switch_list = []
    home_list = data["data"]["records"]
    for home in home_list:
        switch = {
            "platform": home["platform"],
            "name": home["name"],
            "host": home["host"],
            "token": home["token"],
            "model": home["model"]
        }
        switch_list.append(switch)
    configurationUtil.edit_switch_all(switch_list)


# 主循环
def sensor(user_id, new_queue):
    global queue
    queue = new_queue
    num = 0
    while True:
        # 获取温湿度
        temperature, humidity = get_temperature_humidity()
        # 获取PM2.5指数
        # fine_particulate_matter = get_fine_particulate_matter()
        if temperature > -30:
            # 合成数据
            message = {
                "userId": user_id,
                'temp': str(temperature),
                'humidity': str(humidity),
                "createTime": int(round(time.time() * 1000))
            }
            # 发送面板数据
            sensor_success(message)
            # 发送环境数据
            send_mqtt(str(message))
        num = num + 1
        if num == 3:
            num = 0
            check_update_configuration(user_id)
        time.sleep(3)
