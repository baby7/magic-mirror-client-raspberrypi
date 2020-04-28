#!/usr/bin/python3
import os

# 项目根目录路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIALOGUE_DIR = BASE_DIR + '/core/dialogue/'
OPEN_CV_DIR = BASE_DIR + "/core/face_detection/haarcascades/"

# #####################################传感器开始#########################################
# 温湿度传感器BCM接口号
CHANNEL = 17

# 发送MQTT消息的topic及hostname
TOPIC = 'topic_magic_mirror_sensor'
HOSTNAME = '62.234.97.198'
USERNAME = 'sensor_admin'
PASSWORD = 'sensor_admin1'
# #####################################传感器结束#########################################


#
# #####################################浏览器开始#########################################
# 浏览器驱动文件位置
EXECUTABLE_PATH = '/usr/lib/chromium-browser/chromedriver'

# 浏览器要打开的地址
DRIVER_URL = 'https://www.baidu.com'
# #####################################浏览器结束#########################################


#
# #####################################人脸识别开始########################################
# 人脸识别文件名称
FOCUS_FACE = "haarcascade_frontalface_alt"
# #####################################人脸识别结束########################################


#
# ####################################语音对话开始#########################################
# 语音唤醒模型位置
MODEL = DIALOGUE_DIR + 'resources/models/snowboy.umdl'

# 热词唤醒灵敏度
SENSITIVITY = 0.5

# 控制命令关键词列表
COMMAND_LIST = ['笑话', '故事', '天气', '新闻', '成语', '星座', '脑筋急转弯', '歇后语', '绕口令', '顺口溜', '邮编']

# 图灵API密钥
TULING_TURING_KEY = '59e01b844ffc48759e29efa928d974e7'
TULING_URL = 'http://openapi.tuling123.com/openapi/api/v2'
TULING_HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}
# 图灵机器人参数
TULING_DATA = {
    'reqType': 0,
    'perception': {
        'inputText': {
            'text': ''
        },
        'selfInfo': {
            'location': {
                'city': '乌鲁木齐',
                'street': '西山路'
            }
        }
    },
    'userInfo': {
        'apiKey': '',
        'userId': 'starky'
    }
}

# 百度语音API密钥
BAIDU_APP_ID = '16375302'
BAIDU_API_KEY = 'bcFIgL82GlzMxsr72fSmv08e'
BAIDU_SECRET_KEY = 'jGBUnDu22HpaguBA88w2GPRTVacn3T5X'
# 百度语音合成参数
# per:  发音人选择[默认为普通女声]
#       0 为普通女声
#       1 为普通男生
#       3 为情感合成 - 度逍遥
#       4 为情感合成 - 度丫丫
# spd:  语速，取值0 - 15，默认为5中语速
# pit:  音调，取值0 - 15，默认为5中语调
# vol'  音量，取值0 - 15，默认为5中音量
BAIDU_PER = 4
BAIDU_SPD = 4
BAIDU_PIT = 5
BAIDU_VOL = 5
# 百度语音合成语言
BAIDU_LANGUAGE = 'zh'
# ####################################语音对话结束#########################################
