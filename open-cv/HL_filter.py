import cv2
import numpy as np
from scipy import ndimage
'''
#定义卷积核
kernel_3x3 = np.array([[-1,-1,-1],
                        [-1,8,-1],
                        [-1,-1,-1]])
kernel_5x5 = np.array([[-1,-1,-1,-1,-1],
                        [-1,1,2,1,-1],
                        [-1,2,4,2,-1],
                        [-1,1,2,1,-1],
                        [-1,-1,-1,-1,-1]])
img = cv2.imread('1.jpg',0)

k3 = ndimage.convolve(img,kernel_3x3)
k5 = ndimage.convolve(img,kernel_5x5)
blurred = cv2.GaussianBlur(img,(11,11),0)
g_hpf = img - blurred

cv2.imshow('3x3',k3)
cv2.imshow('5x5',k5)
cv2.imshow('g_hpf',g_hpf)

cv2.waitKey()
cv2.destroyAllWindows()
'''
'''
卷积核：卷积核的大小一般是奇数，这样的话它是按照中间的像素点中心对称的，
        所以卷积核一般都是3x3，5x5或者7x7。有中心了，也有了半径的称呼，
        例如5x5大小的核的半径就是2。
平滑，模糊，去燥，锐化，边缘提取等等工作，其实都可以通过卷积操作来完成
'''

img = cv2.imread('1.jpg')
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.Laplacian(gray_img,cv2.CV_8U,gray_img,5)

normalizedInverseAlpha = (1/255)*(255-gray_img)
# cv2.imshow('123',gray_img)

chanels = cv2.split(img)
for chanel in chanels:
    chanel[:] = chanel*normalizedInverseAlpha
    # cv2.imshow('22',chanel)
edge_img=cv2.merge(chanels)
cv2.imwrite('edge.jpg',0)


cv2.imshow('final',edge_img)
cv2.waitKey()
cv2.destroyAllWindows()
