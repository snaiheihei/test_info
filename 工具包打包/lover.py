#!/usr/bin/python3
# @Time      : 2019/7/28 15:43
# @Author    : 老杨
# @FileName  : test.py
# @Software  : PyCharm
from tkinter import *
#下载包 或pycharm中安装Easy thinter
from PIL import Image ,ImageTk
#下载包 或pycharm中安装pillow
import tkinter
#简单的图形开发界面的库
import tkinter.messagebox
#对话框模块，弹出对话框框


class Lover(object):

    def __init__(self):
        
        
        #创建一个主窗口
        root=Tk()
        #窗口名字
        root.title('小姐姐，我要向你表白！')
        #窗口的尺寸和位置
        root.geometry("600x500+300+100")
        root.resizable(width=False,height=False)
        #画布控件尺寸 和背景色
        #Canvas用于绘制图形，创建图形编辑器以及实现自定制的小构件类
        cv= Canvas(root, width = 600, height =500, bg = "white")
        #显示cv里面的内容
        cv.pack()
        #获取当前目录下的 名为“2.jpg”的文件,图片名字随便取但是要对应修改哈
        # a = os.path.abspath('2.jpg')
        #打开图片
        image = Image.open('./app_media/lover.jpg')
        #创建一个Tkinter兼容的照片图像（photo image），
        #它可在Tkinter期望一个图像对象的任何地方使用。
        im = ImageTk.PhotoImage(image)
        #设置边框大小，并以图片作为窗口的背景
        cv.create_image(270,190,image = im)
        def oppose():
            # tkinter.messagebox.showinfo弹窗显示文本消息
            # title为窗口标题 ,message为消息；
            tkinter.messagebox.showinfo(title='扎心了！', message='再考虑考虑吧，不要急着回答')
        def agree():
            tkinter.messagebox.showinfo( title="欧耶", message="我不同意咯！")
            tkinter.messagebox.showinfo( title="欧耶", message="别再打扰我了！")
            root.destroy()
        def hesitate ():
            tkinter.messagebox.showinfo(title='别纠结了', message='你完了，你妈让你嫁给我')
            tkinter.messagebox.showinfo(title='别纠结了', message='你爸也是这么说的')
            tkinter.messagebox.showinfo(title='别纠结了', message='你奶奶也让你嫁给我')
            tkinter.messagebox.showinfo(title='别纠结了', message='你哥哥也同意了')
            tkinter.messagebox.showinfo(title='别纠结了', message='你闺蜜说嫁给我没错')
            tkinter.messagebox.showinfo(title='别纠结了', message='你爸说不同意就打你')
            tkinter.messagebox.showinfo(title='别纠结了', message='掉水我先救你')
            tkinter.messagebox.showinfo(title='别纠结了', message='孩子难产我保大')
            tkinter.messagebox.showinfo(title='别纠结了', message='银行卡都给你')
            tkinter.messagebox.showinfo(title='别纠结了', message='接受现实吧，我会对你好的')
        def closeWindow():
            tkinter.messagebox.showerror(title='未作回应',message='小姐姐,请不要逃避!')
            return  False
        root.protocol('WM_DELETE_WINDOW', closeWindow)
        output_label0 = Label(root,text ="实话告诉你吧", font =("仿宋", 16,"bold"))
        #anchor对齐方式 NW西北
        #window= output_label0 给窗口绑定文本output_label0
        cv.create_window(20, 20, anchor=NW, window= output_label0)
        #create_window创建坐标为x1,y1,x2,y2的窗口。
        #"bold"字体样式
        output_label1 = Label(root,text ="我喜欢你很久了", font =("仿宋", 16,"bold"))
        cv.create_window(35, 50, anchor=NW, window= output_label1)
        output_label2 = Label(root,text ="......你看着办吧", font =("仿宋", 16,"bold"))
        cv.create_window(50, 80, anchor=NW, window= output_label2)
        Button1 = Button(root, text="同意", font =("仿宋", 16,"bold"),width=10,height=1,command = agree)
        #command = showDialogOK 点击执行函数showDialogOK()
        cv.create_window(110, 430, anchor=NW, window=Button1)
        Button2 = Button(root,text='考虑一下', font =("仿宋", 16,"bold"),width=10,height=1,command = hesitate )
        #command = showDialogEE 点击执行函数showDialogEE()
        cv.create_window(260, 430, anchor=NW, window=Button2)
        Button3 = Button(root,text='不同意', font =("仿宋", 16,"bold"),width=10,height=1,command = oppose)
        cv.create_window(450, 430, anchor=NW, window=Button3)
        #command = showDialogNO 点击执行函数sshowDialogNO()
        #创建事件循环直到关闭主窗口root
        root.mainloop()

if __name__ == '__main__':
    lover = Lover()