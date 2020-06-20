#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from pymouse import PyMouse
import time

from conf import settings


executable_path = settings.EXECUTABLE_PATH
driver = None


# 修改页面欢迎语
def change_main_word(word=""):
    js = 'document.getElementsByClassName("title-msg")[0].innerHTML ="' + word + '"'
    driver.execute_script(js)


# 修改当前环境数据
def change_sensor_data(data={}):
    temp = data['temp']
    humidity = data['humidity']
    js = 'document.getElementById("hide_temp").innerHTML ="' + temp + '"'
    driver.execute_script(js)
    js = 'document.getElementById("hide_humidity").innerHTML ="' + humidity + '"'
    driver.execute_script(js)


# 主循环
def viw_html(queue):
    # m = PyMouse()
    option = Options()
    # option.add_argument('disable_infobars')   # 与下面一行效果相同（去除浏览器出现的受控制提示），新版本已失效
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    global driver, executable_path
    driver = webdriver.Chrome(options=option, executable_path=executable_path)
    driver.maximize_window()
    driver.get(settings.DRIVER_URL)
    driver.fullscreen_window()
    time.sleep(3)
    # size = driver.get_window_size()
    # m.click(1261, 30)
    while True:
        json_data = queue.get()
        if json_data['type'] == 'main_text':
            change_main_word(json_data['text'])
        elif json_data['type'] == 'sensor_data':
            change_sensor_data(json_data['data'])
