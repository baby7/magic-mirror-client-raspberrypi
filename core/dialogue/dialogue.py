#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aip import AipSpeech
from mutagen.mp3 import MP3
import speech_recognition as sr
import requests
import pygame
import time
from lib import KRUNKHOMEAPI as kapi
import homeassistant.remote as koapi

from conf import settings

kapi.api = koapi.API('127.0.0.1', '', 8123)  # HA-API:domain, password, port
check = kapi.apicheck()


# 百度语音API密钥
client = AipSpeech(settings.BAIDU_APP_ID, settings.BAIDU_API_KEY, settings.BAIDU_SECRET_KEY)
# 命令控制关键词列表
command_list = settings.COMMAND_LIST


# 敏感词判断函数
def filter_words(ask, answer):
    for i in filtered_words_list:
        if i in ask:
            return True
        if i in answer:
            return True
    return False


# 加载过滤词库
with open(settings.DIALOGUE_DIR + 'filtered_words.txt', 'r', encoding='utf8') as f:
    filtered_words = f.read()
filtered_words_list = filtered_words.split('\n')


# 使用语音识别进行录制
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source=source)
    with open(settings.DIALOGUE_DIR + "recording.wav", "wb") as file:
        file.write(audio.get_wav_data())
    print("recording completed")


# 使用百度语音作为STT引擎
def listen():
    with open(settings.DIALOGUE_DIR + 'recording.wav', 'rb') as file:
        audio_data = file.read()
    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1536,
    })
    result_text = result["result"][0]
    print("you say: " + result_text)
    return result_text


# 命令判断
def commend(text=""):
    if text == "打开开关":
        if check:
            domain = 'switch'
            kapi.turn_on_all(domain)
        kapi.endscript()
        speak("已经" + text)
        return True
    if text == "关闭开关":
        if check:
            domain = 'switch'
            kapi.turn_off_all(domain)
        kapi.endscript()
        speak("已经" + text)
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
        with open(settings.DIALOGUE_DIR + 'audio.mp3', 'wb') as file:
            file.write(result)


# 发送消息
def dialogue_success(text="", queue=None):
    json_data = {
        "type": "main_text",
        "text": text
    }
    queue.put(json_data)


# 使用PyGame播放map3格式文件
def play():
    audio_name = settings.DIALOGUE_DIR + "audio.mp3"
    audio = MP3(audio_name)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_name)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
        time.sleep(int(audio.info.length))  # 时长结束后结束播放


# 对话
def dialogue(user_id, queue):
    rec()                                       # 录音
    request = listen()                          # 语音转为文本
    if not commend(request):
        response = chat(request, user_id)           # 智能对话
        dialogue_success(response, queue)           # 显示文本
        speak(response)                             # 语音合成
    play()                                          # 播放
