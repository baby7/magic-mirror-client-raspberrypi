import time
from subprocess import Popen
import os


Popen(args='/home/pi/.local/bin/hass', shell=True)
time.sleep(60)
os.system("python3 client-raspberrypi/bin/start.py")
