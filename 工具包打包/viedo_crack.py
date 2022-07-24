# 1.URL 解析包
from urllib import parse

# 2.TK 消息盒子包 当程序运行错误时 将错误以弹窗的形式告诉用户
import  tkinter.messagebox as msgbox

# 3.控制浏览器的包 当用户点击了播放的时候 会调用webbrower 自动的去启动浏览器
import webbrowser

# 4.正则表达式 判断用户输入的网址是否有错误
import re


def video_play(url):
    # 视频解析网址地址
    port = 'http://www.wmxz.wang/video.php?url='

    # 做判断 因为防止用户输入非域名
    if re.match(r'^https?:/{2}\w.+$', url):
        # 拿到用户输入的视频地址
        ip  = url

        # 视频播放地址编码
        ip = parse.quote_plus(ip)

        # 自动打开浏览器
        webbrowser.open(port + ip)

        return '你好：\n请在浏览器中观看免费电影'
    else:
        return '你好：\n请输入正确视频链接,使用ctrl+V'


