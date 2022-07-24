import cv2
import numpy as np

img = cv2.imread('line.jpg',cv2.IMREAD_UNCHANGED)
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# back_bgr = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR) #灰度图转回彩色图扩展两个相同通道
# Canny检测会自动转化输入图像为灰度图，输出单通道二值图像
edges = cv2.Canny(img,50,120)
#定义最小直线长度和最小最大直线间隙
minLineLength = 20
maxLineGap = 5
# 霍夫直线变换参考： https://www.jianshu.com/p/ebaf449b434b#fnref1
'''
cv2.HoughLines(),它返回(ρ, θ)值的序列，ρ单位像素，
θ单位弧度。第一个参数，输入的图片是一个二进制图片，在使用hough变换之前，
应用阈值或使用canny边缘检测。第二和第三个参数分别是ρ和θ的精度，第4个参数是阈值，
指可以被认为是一个线条的最小计数值。由于计数值的多少取决于线上的点数，
所以这代表了可以被识别为线的最小长度。
概率哈夫变换:
在哈夫变换中，可以通过2个变量来检测一条线上的点，但花费大量计算。
概率哈夫变换是一个优化的哈夫变换，它不会计算所有的点，而是随机的选取一组足以识别直线的点，
所以我们需要减少阈值。它通过cv2.HoughLinesP()来实现,函数有2个新的参数。minLineLength,maxLineGap

'''
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        #会修改原图像
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)


cv2.imshow('image',edges)
cv2.waitKey()
cv2.imshow('image',img)
cv2.waitKey()
cv2.destroyAllWindows()
