#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aip import AipSpeech
from mutagen.mp3 import MP3
import speech_recognition
import requests
import pygame
import time
# from lib import KRUNKHOMEAPI as kapi
# import homeassistant.remote as koapi
from lib import HomeAssistantAPI as hassapi

from conf import settings

# kapi.api = koapi.API('127.0.0.1', '', 8123)  # HA-API:domain, password, port
# check = kapi.apicheck()

DIALOGUE_DIR = settings.DIALOGUE_DIR


# 百度语音API密钥
client = AipSpeech(settings.BAIDU_APP_ID, settings.BAIDU_API_KEY, settings.BAIDU_SECRET_KEY)

res = requests.get(settings.HOME_LIST)
data = res.json()
switch_list = []
home_list = data["data"]["records"]
for home in home_list:
    switch_list.append({"name": home['word'], "switch_name": home['name']})

# 敏感词判断函数
def filter_words(ask, answer):
    for i in filtered_words_list:
        if i in ask:
            return True
        if i in answer:
            return True
    return False


# 加载过滤词库
with open(DIALOGUE_DIR + 'filtered_words.txt', 'r', encoding='utf8') as f:
    filtered_words = f.read()
filtered_words_list = filtered_words.split('\n')


# 使用语音识别进行录制
def record(rate=16000):
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone(sample_rate=rate) as sour:
        print("未检测到声音")
        audio = r.listen(source=sour)
    with open(DIALOGUE_DIR + "recording.wav", "wb") as recordFile:
        recordFile.write(audio.get_wav_data())
    print("recording completed")


# 使用百度语音作为STT引擎
def listen():
    with open(DIALOGUE_DIR + 'recording.wav', 'rb') as recordFile:
        audio_data = recordFile.read()
    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })
    if result['err_msg'] == 'success.':
        result_text = result["result"][0]
        print("you say: " + result_text)
        return result_text
    else:
        result_text = '没有听清您说的什么'
        return result_text


# 命令判断
def commend(text=""):
    # ************ switch start *************
    for switch in switch_list:
        if judgment_open(text, switch['name']):
            hassapi.open_switch(switch['switch_name'])
            speak("好的")
            return True
        if judgment_close(text, switch['name']):
            hassapi.close_switch(switch['switch_name'])
            speak("好的")
            return True
    # ************* switch end  **************
    # ************* light start **************
    for switch in switch_list:
        if text == (switch['name'] + "最高亮度"):
            hassapi.set_light_brightness(switch['switch_name'], 100)
            speak("好的")
            return True
        if text == (switch['name'] + "最低亮度"):
            hassapi.set_light_brightness(switch['switch_name'], 1)
            speak("好的")
            return True
        if text == (switch['name'] + "最高色温"):
            hassapi.set_light_color_temp(switch['switch_name'], 175)
            speak("好的")
            return True
        if text == (switch['name'] + "最低色温"):
            hassapi.set_light_color_temp(switch['switch_name'], 333)
            speak("好的")
            return True
    # ************* light end   **************
    # ************* sensor start *************
    if text == "室内环境信息" or text == "房间环境信息" or text == "室内温湿度" or text == "房间温湿度":
        temp, hum = hassapi.get_temp_and_hum("dht_sensor_temperature", "dht_sensor_humidity")
        speak("室内当前温度为" + str(int(float(temp))) + "度，湿度为百分之" + str(int(float(hum))))
        return True
    # ************* sensor end   *************
    # ************ control start *************
    control_name = "xiaomi_yaokongqi"
    if text == "我要看电视" or judgment_open(text, "电视") or judgment_close(text, "电视"):
        hassapi.control_box(control_name)
        hassapi.control_tv(control_name)
        speak("好的")
        return True
    if text == "我要吹风扇" or judgment_open(text, "风扇") or judgment_close(text, "风扇"):
        hassapi.control_fan(control_name)
        speak("好的")
        return True
    if text == "风扇风速" or text == "调整风扇风速" or text == "风扇转速" or text == "调整风扇转速":
        hassapi.control_fan_speed(control_name)
        speak("好的")
        return True
    if text == "风扇摇头":
        hassapi.control_fan_head(control_name)
        speak("好的")
        return True
    if text == "空调制冷" or text == "制冷":
        hassapi.control_air_conditioning_cold(control_name)
        speak("好的")
        return True
    if text == "空调除湿" or text == "除湿":
        hassapi.control_air_conditioning_wet(control_name)
        speak("好的")
        return True
    # ************ control end   *************
    return False


# 开启语言判断
def judgment_open(text, entity):
    text = text.replace("给爷儿把", "")
    text = text.replace("给爷把", "")
    text = text.replace("给爷", "")
    if text == ("打开" + entity) or text == ("开" + entity) or text == ("开开" + entity) or text == ("开启" + entity):
        return True
    if text == (entity + "打开") or text == (entity + "开") or text == (entity + "开开") or text == (entity + "开启"):
        return True
    return False


# 关闭语言判断
def judgment_close(text, entity):
    text = text.replace("给爷儿把", "")
    text = text.replace("给爷把", "")
    text = text.replace("给爷", "")
    if text == ("关闭" + entity) or text == ("关" + entity) or text == ("关掉" + entity):
        return True
    if text == (entity + "关闭") or text == (entity + "关") or text == (entity + "关掉"):
        return True
    return False


# 智能对话
def chat(text="", user_id=1):
    url = settings.MANAGE_URL
    data = {
        'userId': user_id,
        'question': text
    }
    r = requests.post(url, data=data)
    result = r.json()
    if result['code'] is 0:
        if result['data'][0] == '这么标准的普通话你竟然听不懂' or result['data'][0] == '我说没什么'\
                or result['data'][0] == '我说没什么!' or result['data'][0] == '我说没什么！'\
                or result['data'][0] == '都说过几遍了，怎么还要问呐' or result['data'][0] == '都说过几遍了,怎么还要问呐':
            return '没听清'
        return result['data'][0]
    return ""


# 百度语音作为TTS引擎
def speak(text=""):
    result = client.synthesis(text, settings.BAIDU_LANGUAGE, 1, {
        'per': settings.BAIDU_PER,
        'spd': settings.BAIDU_SPD,
        'pit': settings.BAIDU_PIT,
        'vol': settings.BAIDU_VOL
    })
    if not isinstance(result, dict):
        with open(DIALOGUE_DIR + 'audio.mp3', 'wb') as audioFile:
            audioFile.write(result)


# 发送消息
def dialogue_success(text="", queue=None):
    json_data = {
        "type": "main_text",
        "text": text
    }
    queue.put(json_data)


# 使用PyGame播放map3格式文件
def play():
    audio_name = DIALOGUE_DIR + "audio.mp3"
    audio = MP3(audio_name)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_name)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
        time.sleep(int(audio.info.length))  # 时长结束后结束播放


# 对话
def dialogue(user_id, queue):
    record()                                        # 录音
    request = listen()                              # 录音转为文本
    if not commend(request):                        # 判断是否为命令
        response = chat(request, user_id)           # 智能对话
        dialogue_success(response, queue)           # 显示文本
        speak(response)                             # 语音合成
    play()                                          # 播放结果
