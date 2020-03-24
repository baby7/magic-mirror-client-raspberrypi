import threading as td
import signal

from conf import settings
from core.dialogue import dialogue
from core.dialogue import snowboydecoder


interrupted = False


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
    dialogue.dialogue()                 # 语音识别程序


# 主程序
def snowboy():
    global interrupted
    model = settings.MODEL

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=settings.SENSITIVITY)
    print('Listening... Press Ctrl+C to exit')

    # main loop
    # detector.start(detected_callback=snowboydecoder.play_audio_file,
    #                interrupt_check=interrupt_callback,
    #                sleep_time=0.03)
    detector.start(detected_callback=speech_recognition,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()
