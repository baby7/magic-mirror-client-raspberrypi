#!/usr/bin/python3
import paho.mqtt.publish as publish
import time

from lib import RPi_TH
from lib import RPi_FPM
from conf import settings


# 发送mqtt消息到服务器
def send_mqtt(message):
    publish.single(settings.topic, message, hostname=settings.hostname)
    print("send message success")


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


# 主循环
def sensor():
    while True:
        # 获取温湿度
        temperature, humidity = get_temperature_humidity()
        print(temperature)
        print(humidity)
        # 获取PM2.5指数
        fine_particulate_matter = get_fine_particulate_matter()
        if temperature > -30:
            # 合成数据
            message = {
                'temperature': str(temperature),
                'humidity': str(humidity),
                'fine_particulate_matter': str(fine_particulate_matter)
            }
            # 发送环境数据
            # send_mqtt(message)
            print(message)
        time.sleep(3)