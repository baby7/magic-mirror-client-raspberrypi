#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymouse import PyMouse
import time

from conf import settings


executable_path = settings.EXECUTABLE_PATH
driver = None


def viw_html():
    m = PyMouse()
    option = Options()
    # option.add_argument('disable_infobars')   //与下面一行效果相同（去除浏览器出现的受控制提示），新版本已失效
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    global driver, executable_path
    driver = webdriver.Chrome(options=option, executable_path=executable_path)
    driver.maximize_window()
    driver.fullscreen_window()
    driver.get(settings.DRIVER_URL)
    time.sleep(3)
    # size = driver.get_window_size()
    m.click(1261, 30)
