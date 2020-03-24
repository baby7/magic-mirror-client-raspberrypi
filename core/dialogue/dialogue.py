#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aip import AipSpeech
from mutagen.mp3 import MP3
import speech_recognition as sr
import random
import requests
import pygame
import json
import time

from conf import settings


# 百度语音API密钥
client = AipSpeech(settings.BAIDU_APP_ID, settings.BAIDU_API_KEY, settings.BAIDU_SECRET_KEY)
# 图灵API密钥
TURING_KEY = settings.TULING_TURING_KEY
URL = settings.TULING_URL
HEADERS = settings.TULING_HEADERS
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


# 加载语料库和过滤词库
with open(settings.DIALOGUE_DIR + 'filtered_words.txt', 'r', encoding='utf8') as f:
    filtered_words = f.read()
with open(settings.DIALOGUE_DIR + 'mrening.conv', "r", encoding='utf8') as f:
    mrening = f.read()
filtered_words_list = filtered_words.split('\n')
dialogues_list = mrening.split('E')


# 对语料库进行处理，条理化后加载到内存中
index = 0
dialogues_good_list = []
for dialogues in dialogues_list:
    index = index + 1
    if index % 4540 == 0:
        print(str(int((index/454000) * 100)) + '%')     # 进度显示[树莓派较慢，为了不造成卡死的假象]
    dialogue = dialogues.split('M ')
    if len(dialogue) is 3:
        dialogues_good_list.append([dialogue[1].replace('\n', ''), dialogue[2].replace('\n', '')])
dialogues_list = None   # 释放内存


# 前置对话
def preposition_dialogue(word):
    # 命令前置判断
    for command in command_list:
        if command in word:
            return ''
    # 语料库搜索[可以使用fuzzywuzzy进行语句相似度查询，但是树莓派承受不住...]
    dialogues_good_list_word = []
    for dialogues_good in dialogues_good_list:
        if dialogues_good[0] == word:
            if not filter_words(dialogues_good[0], dialogues_good[1]):
                dialogues_good_list_word.append(dialogues_good)
    if len(dialogues_good_list_word) > 0:
        # 随机抽一条回复
        result = dialogues_good_list_word[random.randint(0, len(dialogues_good_list_word) - 1)][1]
        print("local robot say: " + result)
        return result
    else:
        return ''


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


# 图灵聊天机器人(后续切换为后端接口)
def robot(text=""):
    data = settings.TULING_DATA
    data["userInfo"]["apiKey"] = TURING_KEY
    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)
    result = response_dict["results"][0]["values"]["text"]
    print("remote robot say: " + result)
    return result


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
def dialogue():
    rec()                                       # 录音
    request = listen()                          # 语音转为文本
    response = preposition_dialogue(request)    # 进行前置判断对话
    if response == '':
        response = robot(request)               # 智能对话
    speak(response)                             # 语音合成
    play()                                      # 播放
