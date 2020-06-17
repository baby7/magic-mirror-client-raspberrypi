import time
from subprocess import Popen
import os


Popen(args='/home/pi/.local/bin/hass', shell=True)
time.sleep(60)
os.system("cd client-raspberrypi/bin/")
os.system("python3 start.py")
