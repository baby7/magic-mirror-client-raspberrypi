#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymouse import PyMouse
import time

from conf import settings


executable_path = settings.EXECUTABLE_PATH
driver = None


# 修改页面欢迎语
def change_main_word(word=""):
    # 定位“立即注册”位置，修改target属性值为空，让新打开的链接显示在同一个窗口
    js = 'document.getElementsByClassName("title-msg")[0].innerHTML ="' + word + '"'
    driver.execute_script(js)  # 执行js语句


# 主循环
def viw_html():
    m = PyMouse()
    option = Options()
    # option.add_argument('disable_infobars')   #与下面一行效果相同（去除浏览器出现的受控制提示），新版本已失效
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    global driver, executable_path
    driver = webdriver.Chrome(options=option, executable_path=executable_path)
    driver.maximize_window()
    driver.get(settings.DRIVER_URL)
    driver.fullscreen_window()
    time.sleep(3)
    # size = driver.get_window_size()
    # m.click(1261, 30)
