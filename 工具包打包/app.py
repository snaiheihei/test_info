from tkinter import Tk,Button,Entry,Label,Text,END,Listbox,Scrollbar
import tkinter as tk 
import tkinter.messagebox as msgbox
import re
import time

from tkinter import ttk
import os
from playsound import playsound
from PIL import Image ,ImageTk
from pygame import mixer

from fanyi_js import Fanyi
from aip_speech_text import get_speech_from_text
from temperature import Temperature
from xingzuo import Constellations
from chat_robot import Robot_Chat
from viedo_crack import video_play
from lover import Lover
# from cameo import Cameo
import logging

def decorator_1(func):
    def wraper(self,*args,**kwargs):
        self.ent_text.set('')
        func(self,*args,**kwargs)
        self.result_text.delete(1.0,END)
    return wraper


class Win(object):

    def __init__(self):
        self.window = Tk()    #实例Tk窗口对象
        self.window.title("小小工具包")     #设置窗口名称
        self.window.geometry('560x390+550+180') #设置大小
        self.window.resizable(False,False) #禁止窗口大小不可变 (width=False,height=False)(0,0)
        
        self.ent_text=tk.StringVar()  #输入框
        self.ent_text.set('-*-')                             
        self.entry = Entry(self.window,textvariable=self.ent_text,foreground='blue',font='weiruanyahei 12',highlightcolor='green',highlightthickness=1)
        self.entry.place(x=10,y=10,width=250,height=35,anchor='nw')  #anchor='nw'锚点左上角 

        self.but_text=tk.StringVar() #按钮
        self.but_text.set('-*-')
        self.imgBtn = tk.PhotoImage(file='./app_media/button.jpg') #必须加self按钮图片才能显示
        self.button = Button(self.window,image=self.imgBtn,compound='center',overrelief='ridge',font='weiruanyahei',fg='blue',textvariable=self.but_text,command=self.submit)
        self.button.place(x=270,y=10,width=50,height=32)   #文本与图片搭配模式               #按钮文本可变，绑定函数

        self.v=tk.StringVar()  #选择列表
        self.v.set('请选择使用工具')
        self.list_box = ttk.Combobox(self.window,state='readonly',textvariable=self.v) #字符变量对象和image参数一样也许绑定self指向
        self.list_box['values'] = ['翻译词典','天气查询','星座运势','聊天机器人','接球小游戏','音乐播放','表白小游戏','破解视频','视频流cameo']
        self.list_box.bind("<<ComboboxSelected>>",self.select)  #选择列表绑定函数触发事件
        self.list_box.place(x=350,y=10,width=200,height=32)

        self.label_text=tk.StringVar()
        self.label_text.set('-*-hello-*-')
        title_label = Label(self.window,state='active',font='weiruanyahei 12',textvariable=self.label_text)
        title_label.place(x=10,y=55)

        self.result_text = Text(self.window,font='weiruanyahei 12',background='#ccc')
        self.result_text.place(x=10,y=75,width=260,height=280)

        # 1.标签里添加图片
        # self.imgtext = tk.PhotoImage(file='button.jpg')     #制作标签 添加图片
        # image_lable = Label(self.window,image=self.imgtext) #必须加self按钮图片才能显示
        # image_lable.place(x=285,y=75,width=260,height=280)

        '''
        #如果将创建ImageTk.PhotoImage的那句代码放到一个函数中，会出现十分奇葩的现象：图片不显示
        #解决方法是：所有的PhotoImage在mainloop期间必须有引用指向它们。
        #可以将img变量定义成全局变量，总之，必须有引用指向PhotoImage，否则立马回收  类中添加self指向

        想要使用格式png，jpg来添加图片，使用第三方库,这秘籍的名字叫做Pillow。
        '''
        # 2.画布里添加图片
        cv= tk.Canvas(self.window, bg = "white")
        cv.place(x=285,y=75, width =260,height =280)
        
        image = Image.open('./app_media/01.ico')
        self.im = ImageTk.PhotoImage(image)
        #添加图片在画布中位置及锚点
        cv.create_image(0,0,anchor='nw',image = self.im) 

    @decorator_1
    def select(self,data):
        cmd_index=self.list_box.get()
        self.entry.focus_set()   #将焦点设置到输入框，焦点移出下拉列表
        if cmd_index=='翻译词典':
            self.label_text.set('翻译结果：')
            self.but_text.set('查询')        
            get_speech_from_text('请输入查询单词')
           
        if cmd_index=='天气查询':
            self.label_text.set('天气状况：')
            self.but_text.set('查询')
            get_speech_from_text('请输入查询天气城市')

        if cmd_index=='星座运势':
            self.label_text.set('星座运势：')
            self.but_text.set('查询')
            get_speech_from_text('请输入查询星座')

        if cmd_index=='聊天机器人':
            self.label_text.set('陪聊信息：')
            self.but_text.set('发送')
            get_speech_from_text('我们开始聊天吧')

        if cmd_index=='接球小游戏':
            self.label_text.set('开始玩游戏：')
            self.but_text.set('开始')
            get_speech_from_text('开始玩接球小游戏')

        if cmd_index=='音乐播放':
            self.label_text.set('音乐播放：')
            self.but_text.set('播放')
            self.ent_text.set(r'F:\python学习\手势音乐播放\music') 
            get_speech_from_text('添加歌曲文件路径,开始播放音乐')

        if cmd_index=='表白小游戏':
            self.label_text.set('表白小游戏：')
            self.but_text.set('开始')
            get_speech_from_text('点击开始后，只有点击同意,才能关闭窗口')            

        if cmd_index=='破解视频':
            self.label_text.set('破解视频：')
            self.but_text.set('播放')
            get_speech_from_text('请输入播放视频链接')

        if cmd_index=='视频流cameo':
            self.label_text.set('图像处理：')
            self.but_text.set('确认')
            get_speech_from_text('请输入图像过滤指令')
            


    def submit(self):
        cmd_index=self.list_box.get()

        if cmd_index=='翻译词典':
            try:
                                    #self.button.destroy() 可以摧毁已存在控件 
                fanyi =Fanyi()
                #entry里参数如果设置了textvariable 也可以通过变量获取self.ent_text.get()
                content = self.entry.get()   
                data = fanyi.translate(content)
                self.result_text.delete(1.0,END)
                self.result_text.insert(END,data)
                fanyi.read_word()
            except:
                pass

        if cmd_index=='天气查询':
            try:
                content = self.entry.get()
                temp = Temperature(content)
                data = temp.get_result()
                self.result_text.delete(1.0,END)
                self.result_text.insert(END,data)
                temp.baidu_speaker()
            except Exception as e:
                print(e)

        if cmd_index=='星座运势':
            try:
                content = self.entry.get()
                cons = Constellations(content)
                data = cons.get_result()
                # print(data) #输出星座查询信息
                self.result_text.delete(1.0,END)
                self.result_text.insert(END,data)
                cons.baidu_speaker()
            except Exception as e:
                print(e)
                

        if cmd_index=='聊天机器人':
            try:
                content = self.entry.get()
                robot = Robot_Chat(content)
                data = robot.get_result()
                self.result_text.delete(1.0,END)
                self.result_text.insert(END,data)
                robot.baidu_speaker()
            except Exception as e:
                print(e)

        if cmd_index=='接球小游戏':
            try:
                os.system('python xiaoqiu.py')
            except:
                pass

        if cmd_index=='表白小游戏':
            try:
                top=tk.Toplevel()
                top.title('小姐姐，我要向你表白！')
                top.geometry("600x500+100+100")
                top.resizable(width=False,height=False)
                cv= tk.Canvas(top, width = 600, height =500, bg = "white")
                cv.pack()
                image = Image.open('./app_media/lover.jpg')
                self.imtop = ImageTk.PhotoImage(image)
                cv.create_image(270,190,image = self.imtop)
                # cv.focus_set()
                def oppose():
                    msgbox.showinfo(title='扎心了！', message='再考虑考虑吧，不要急着回答')
                def agree():
                    msgbox.showinfo( title="欧耶", message="我不同意咯！")
                    msgbox.showinfo( title="欧耶", message="别再打扰我了！")
                    top.destroy() #摧毁当前窗口
                def hesitate ():
                    msgbox.showinfo(title='别纠结了', message='你完了，你妈让你嫁给我')
                    msgbox.showinfo(title='别纠结了', message='你爸也是这么说的')
                    msgbox.showinfo(title='别纠结了', message='你奶奶也让你嫁给我')
                    msgbox.showinfo(title='别纠结了', message='你哥哥也同意了')
                    msgbox.showinfo(title='别纠结了', message='你闺蜜说嫁给我没错')
                    msgbox.showinfo(title='别纠结了', message='你爸说不同意就打你')
                    msgbox.showinfo(title='别纠结了', message='掉水我先救你')
                    msgbox.showinfo(title='别纠结了', message='孩子难产我保大')
                    msgbox.showinfo(title='别纠结了', message='银行卡都给你')
                    msgbox.showinfo(title='别纠结了', message='接受现实吧，我会对你好的')
                def closeWindow():
                    msgbox.showerror(title='未作回应',message='小姐姐,请不要逃避!')
                    return  False
                top.protocol('WM_DELETE_WINDOW', closeWindow) #改变关闭窗口事件绑定函数
                output_label0 = Label(top,text ="实话告诉你吧", font =("仿宋", 16,"bold"))
                #anchor对齐方式 NW西北
                #window= output_label0 给窗口绑定文本output_label0
                cv.create_window(20, 20, anchor='nw', window= output_label0)
                #create_window创建坐标为x1,y1,x2,y2的窗口。
                #"bold"字体样式
                output_label1 = Label(top,text ="我喜欢你很久了", font =("仿宋", 16,"bold"))
                cv.create_window(35, 50, anchor='nw', window= output_label1)
                output_label2 = Label(top,text ="......你看着办吧", font =("仿宋", 16,"bold"))
                cv.create_window(50, 80, anchor='nw', window= output_label2)
                Button1 = Button(top, text="同意", font =("仿宋", 16,"bold"),width=10,height=1,command = agree)
                #command = showDialogOK 点击执行函数showDialogOK()
                cv.create_window(110, 430, anchor='nw', window=Button1)
                Button2 = Button(top,text='考虑一下', font =("仿宋", 16,"bold"),width=10,height=1,command = hesitate )
                #command = showDialogEE 点击执行函数showDialogEE()
                cv.create_window(260, 430, anchor='nw', window=Button2)
                Button3 = Button(top,text='不同意', font =("仿宋", 16,"bold"),width=10,height=1,command = oppose)
                cv.create_window(450, 430, anchor='nw', window=Button3)
                #command = showDialogNO 点击执行函数sshowDialogNO()
                #创建事件循环直到关闭主窗口root
                top.mainloop()
            except Exception as e:
                print(e)  

        if cmd_index=='音乐播放':
            try:
                path=self.ent_text.get()
                music_source = []
                music_name = []
                music_path_list = os.listdir(path)
                for name in music_path_list:
                    music_path=path+'\\'+name
                    regex = re.compile(r'music\\(.*?).mp3')
                    music = regex.search(music_path).group(1)
                    music_name.append(music)
                    music_source.append(music_path)
                name_path=dict(zip(music_name,music_source))

                mixer.init()
                self.flag=0
                self.current_music_no=0
                self.volume=0.4
                mixer.music.set_volume(self.volume)

                def play():
                    self.flag=0
                    musicer = regex.search(music_source[self.current_music_no]).group(1)
                    self.play_v.set(musicer)
                    mixer.music.load(music_source[self.current_music_no])
                    mixer.music.play()

                def play_pause():
                    if self.flag==0:
                        mixer.music.pause()
                        self.flag+=1
                    else:
                        mixer.music.unpause()
                        self.flag-=1
                def play_last():
                    self.flag=0
                    if self.current_music_no>0:
                        self.current_music_no-=1
                    else:
                        self.current_music_no=len(music_source)-1
                    musicer = regex.search(music_source[self.current_music_no]).group(1)
                    self.play_v.set(musicer)
                    mixer.music.load(music_source[self.current_music_no])
                    mixer.music.play()
                def play_next():
                    self.flag=0
                    if self.current_music_no<len(music_source)-1 :
                        self.current_music_no+=1
                    else:
                        self.current_music_no=0
                    musicer = regex.search(music_source[self.current_music_no]).group(1)
                    self.play_v.set(musicer)
                    mixer.music.load(music_source[self.current_music_no])
                    mixer.music.play()

                def voice_up():
                    if self.volume<1:
                        self.volume+=0.1
                        mixer.music.set_volume(self.volume)
                    else:
                        get_speech_from_text('声音已经最大了')
                        
                def voice_down():
                    if self.volume>0:
                        self.volume-=0.1
                        mixer.music.set_volume(self.volume)
                    else:
                        get_speech_from_text('声音已经最小了')

                def select_music(arg):
                    musicer= music_list_box.get()
                    image_but_pause.focus_set()   #设置焦点为暂停按钮，避免下拉列表选择是焦点落入
                    musicer_path=name_path.get(musicer) #获取列表选择歌曲名得到歌曲路径（字典get）
                    self.current_music_no=music_source.index(musicer_path) #同时更改歌曲指针序号
                    mixer.music.load(musicer_path)
                    mixer.music.play()

                top_palyer=tk.Toplevel()
                top_palyer.title('Music Player！')
                top_palyer.geometry("460x160+800+10")
                top_palyer.resizable(width=False,height=False)

                self.play_img1 = tk.PhotoImage(file='player_image/1.gif')
                image_lable_player = Label(top_palyer,image=self.play_img1)
                image_lable_player.place(x=10,y=50,width=55,height=60)

                self.play_img2 = tk.PhotoImage(file='player_image/2.gif')
                image_but_up = Button(top_palyer,image=self.play_img2,compound='center',font='weiruanyahei 30 bold',text='+',overrelief='ridge',fg='Fuchsia',bg='white',command=voice_up)
                image_but_up.place(x=15,y=15,width=40,height=30)

                image_but_down = Button(top_palyer,image=self.play_img2,compound='center',font='weiruanyahei 30 bold',text='-',overrelief='ridge',fg='Fuchsia',bg='white',command=voice_down)
                image_but_down.place(x=15,y=115,width=40,height=30)

                self.play_img3 = tk.PhotoImage(file='player_image/3.gif')
                image_but_last = Button(top_palyer,image=self.play_img3,overrelief='ridge',bg='Fuchsia',command=play_last)
                image_but_last.place(x=80,y=50,width=60,height=60)

                self.play_img4 = tk.PhotoImage(file='player_image/4.gif')
                image_but_start = Button(top_palyer,image=self.play_img4,overrelief='ridge',bg='Fuchsia',command=play)
                image_but_start.place(x=145,y=50,width=60,height=60)

                self.play_img5 = tk.PhotoImage(file='player_image/5.gif')
                image_but_pause = Button(top_palyer,image=self.play_img5,overrelief='ridge',bg='Fuchsia',command=play_pause)
                image_but_pause.place(x=210,y=50,width=60,height=60)

                self.play_img6 = tk.PhotoImage(file='player_image/6.gif')
                image_but_next = Button(top_palyer,image=self.play_img6,overrelief='ridge',bg='Fuchsia',command=play_next)
                image_but_next.place(x=275,y=50,width=60,height=60)

                self.play_v=tk.StringVar()  #选择列表
                self.play_v.set('歌曲列表')
                music_list_box = ttk.Combobox(top_palyer,state='readonly',takefocus=False,textvariable=self.play_v) #字符变量对象和image参数一样也许绑定self指向
                music_list_box['values'] = music_name
                music_list_box.bind("<<ComboboxSelected>>",select_music)  #选择列表绑定函数触发事件
                music_list_box.place(x=328,y=10,width=120,height=32)

                self.play_img7 = tk.PhotoImage(file='player_image/7.gif')
                image_lable2_player = Label(top_palyer,image=self.play_img7)
                image_lable2_player.place(x=345,y=50,width=80,height=80)            

                # self.play_img8 = tk.PhotoImage(file='player_image/8.gif')
                # image_lable2_player = Label(top_palyer,image=self.play_img8)
                # image_lable2_player.place(x=405,y=135,width=50,height=50) 
                # self.result_text.delete(1.0,END)
                # self.result_text.insert(END,'你好：\n请在输入框中添加歌曲文件路径')
            except:
                pass

        if cmd_index=='破解视频':
            try:
                content = self.entry.get()
                data=video_play(content)
                get_speech_from_text(data)
                self.result_text.delete(1.0,END)
                self.result_text.insert(END,data)
            except Exception as e:
                print(e)

        if cmd_index=='视频流cameo':
            try:
                content = self.entry.get()
                data_list = content.split(' ')
                if len(data_list) == 1:
                    data = data_list[0]
                    Cameo(data2=data).run()
                if len(data_list) == 2 :
                    data1 = data_list[0]
                    data2 = data_list[1]
                    Cameo(data1=data2,data2=data1).run()

            except:
                raise


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    # 忽略警告日志
    # logging.captureWarnings(True)
    app = Win()
    app.run()
    # os.system('python app.py') #同一路径下可用

#歌曲循环播放没有解决 如何指定歌曲队列