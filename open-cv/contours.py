import cv2
import numpy as np 

# cv2.pyrDown高斯金字塔参考：https://blog.csdn.net/woainishifu/article/details/62888228
# 降采样的意思其实是把图像的尺寸缩减一半，行和列同时缩减一半。
# 这样缩减会带来的影响就是：原图中那些精细的细节边缘等地方，会因此变得锯齿状，产生失真，
# 因此为了缩小之后图像看起来自然，必须进行平滑，这也就是这个算法为什么在降采样之前
# 先对图像进行了高斯模糊的原因。
'''
img = cv2.pyrDown(cv2.imread('test1.jpg',cv2.IMREAD_UNCHANGED))
back_img = np.full_like(img,0,np.uint8)
# print(img.shape,cv2.imread('1.png',cv2.IMREAD_UNCHANGED).shape)
ret,thresh_image = cv2.threshold(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY),127,255,0)
contours,hier = cv2.findContours(thresh_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    #find bounding box coordinates
    x,y,w,h =cv2.boundingRect(c)
    cv2.rectangle(back_img,(x,y),(x+w,y+h),(0,255,0),2)

    #find minimum area
    rect = cv2.minAreaRect(c)
    # calculate coordinates of the minimum area rectangle
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(back_img,[box],0,(0,0,255),3)

    # calculate center and radius of minimum enclosing Circle
    (x,y),radius = cv2.minEnclosingCircle(c)
    #cast to integers
    center =(int(x),int(y))
    radius = int(radius)
    #draw the circle
    cv2.circle(back_img,center,radius,(0,255,0),2)

cv2.drawContours(back_img,contours,-1,(255,0,0),1)
cv2.imshow('image',back_img)
cv2.waitKey()
cv2.destroyAllWindows()
'''

img = cv2.pyrDown(cv2.imread('test1.jpg',cv2.IMREAD_UNCHANGED))
back_img = np.full_like(img,0,np.uint8)

ret,thresh_image = cv2.threshold(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY),127,255,0)
contours,hier = cv2.findContours(thresh_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#本次操作取的是外轮廓，只有一个轮廓，可以不用循环遍历
for c in contours:
    #计算近似多边形框
    epsilon = 0.01*cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    cv2.drawContours(back_img, [approx], 0, (0, 0, 255), 2)
    #外壳凸出 cv2.drawContours可以在背景图上绘制检测出的任意轮廓(该轮廓必须是列表类型)
    hull = cv2.convexHull(c)
    cv2.drawContours(back_img, [hull], 0, (0, 255,0 ), 2)

cv2.drawContours(back_img,contours,-1,(255,0,0),1)
cv2.imshow('image',back_img)
cv2.waitKey()
cv2.destroyAllWindows()



