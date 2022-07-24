# -*- coding: utf-8 -*-
# 使用百度提供的pyth SDK
from aip import AipSpeech
from playsound import playsound
import os

APP_ID ="17032866"
API_KEY = "hpqtoC9yTj2UlPIDuX74RQn9"
SECRET_KEY = "5zqIWZCUGWUWrnySXEDvF9RjXZlL1wcg"

speech_client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_speech_from_file(text_path):

    with open(text_path, "r", encoding="utf8") as f:
        text_list = []
        while True:
            text_content = f.read(1024)
            if not text_content:
                break
            text_list.append(text_content)

    result_audio = b""
    # 第一个是文本， 第二个是语言， 第三个是平台，第四个是声音
    for text in text_list:
        print(text)
        result = speech_client.synthesis(text, "zh", 1, {
            "vol": 5,  # 音量
            "spd": 5,  # 语速
            "pit": 6,  # 语调
            "per": 111,  # 基础库 0：女 1：男 3：逍遥 4：小萝莉
        })
        if not isinstance(result, dict):
            #实现分段读取
            with open('audio.mp3', 'wb') as f:
                f.write(result)
            playsound("audio.mp3")
            os.remove("audio.mp3")
            result_audio += result
        else:
            print(result_audio)


def get_speech_from_text(text):

    text_part = len(text) // 200 + 1
    text_list = [text[200 * i: 200 * (i + 1)] for i in range(text_part)]

    result_audio = b""

    for text in text_list:
       
        result = speech_client.synthesis(text,options= {
            "vol": 5,  # 音量
            "spd": 5,  # 语速
            "pit": 6,  # 语调
            "per": 3,  # 精品音库 度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5
        })
       
        if not isinstance(result, dict):
            #由于输入文本较小，实现整段整体读取
            result_audio += result
        else:
            print(result_audio)

    with open('audio.mp3', 'wb') as f:
        f.write(result_audio)

    playsound("audio.mp3")
    os.remove("audio.mp3")

if __name__ == '__main__':
    
    # get_speech_from_file('qiushi.txt')
    get_speech_from_text("你好啊，我们今天来讲故事")  #测试声音
    # playsound("audio.mp3")
    # os.remove("audio.mp3")


'''
参数：
tex 必填  合成的文本，使用UTF-8编码。小于2048个中文字或者英文数字。
spd 选填  语速，取值0-9，默认为5中语速(str or int)
pit 选填  音调，取值0-9，默认为5中语调
vol 选填  音量，取值0-15，默认为5中音量
per 选填  1.基础音库 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
          2.精品音库 度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5

lan 必填  固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh（sdk中已默认填写）
ctp 必填  客户端类型选择，web端填写固定值1

疑问：data = dict(data, **(options or {}))用法
'''


'''
文件整体读取
    for text in text_list:
        print(text)
        result = speech_client.synthesis(text, "zh", 1, {
            "vol": 5,  # 音量
            "spd": 5,  # 语速
            "pit": 9,  # 语调
            "per": 0,  # 0：女 1：男 3：逍遥 4：小萝莉
        })
        if not isinstance(result, dict):
            result_audio += result
        else:
            print(result_audio)

    with open('audio.mp3', 'wb') as f:
        f.write(result_audio)
'''