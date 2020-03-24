# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from pymouse import PyMouse
# import time
#
#
# m = PyMouse()
# chrome_options = Options()
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
# browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/lib/chromium-browser/chromedriver")
# browser.maximize_window()
# browser.fullscreen_window()
# browser.get("http://www.baidu.com")
# time.sleep(3)
# size = browser.get_window_size()
# m.click(1261, 30)

from fuzzywuzzy import fuzz

text1 = "你好"
text2 = "你好啊"

print(fuzz.ratio(text1, text2))
# 74
