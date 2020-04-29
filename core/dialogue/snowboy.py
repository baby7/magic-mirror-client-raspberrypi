import threading as td
import signal

from conf import settings
from core.dialogue import dialogue
from core.dialogue import snowboydecoder


interrupted = False
my_user_id = 1


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# 语音识别回调
def speech_recognition():
    t = td.Thread(target=snowboydecoder.play_audio_file)    # 声音响应
    t.start()
    global my_user_id
    dialogue.dialogue(my_user_id)                 # 语音识别程序


# 主程序
def snowboy(user_id):
    global interrupted, my_user_id
    model = settings.MODEL
    my_user_id = user_id

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=settings.SENSITIVITY)
    print('Listening... Press Ctrl+C to exit')

    detector.start(detected_callback=speech_recognition,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()
