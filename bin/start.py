#!/usr/bin/python3
import os
import sys

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))  # 返回不带文件名的目录名
print(os.path.abspath(__file__))  # 返回当前程序的绝对路径\
print(__file__)  # 返回当前程序的相对路径/
# 添加环境变量
sys.path.append(BASE_DIR)
from core import main

main.start()
