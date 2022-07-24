import cv2
import numpy as np 
import utils

def strokeEdges(src,dst,blurKsize = 7,edgeKsize = 5):
    if blurKsize>=3:
        #模糊函数，输入图像可以是彩图将图像模糊（中值法），blurKsize越大越模糊
		# 做边缘检测前需转灰度图才有意义
        # blurredSrc = cv2.medianBlur(src,edgeKsize)
        blurredSrc = cv2.GaussianBlur(src,(11,11),0)
        grayScr = cv2.cvtColor(blurredSrc,cv2.COLOR_BGR2GRAY)
    else:
        grayScr = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    #转化为灰度图进行边缘检测（拉普拉斯算子（调和算子））
    cv2.Laplacian(grayScr,cv2.CV_8U,grayScr,ksize=edgeKsize)

    #标准化翻转透明 转换成黑色边缘和白色背景的图像（0~1之间浮点型数组）
    normalizedInverseAlpha = (1 / 255) * (255 - grayScr)

    #源图像分离单通道函数 对每通道做*normalizedInverseAlpha
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel*normalizedInverseAlpha
    # 通道合并处理  注意呈现的是dst图像BGR叠加边缘检测（黑色边缘，白色背景）
    cv2.merge(channels,dst)

#卷积滤波
class ConvolutionFilter(object):
	"""a filter that applies a convolution to V (or all of BGR)"""
	def __init__(self, kernel):
		self._kernel = kernel

	def apply(self,src,dst):
		'''apply the filter with a BGR or gray source/destination(目标) '''
		'''
		filter2D
		src	原图像  当ddepth=-1时，表示输出图像与原图像有相同的深度。
		dst	目标图像，与原图像尺寸和通过数相同  kernel	卷积核（或相当于相关核），单通道浮点矩阵;
		如果想在图像不同的通道使用不同的kernel，可以先使用split()函数将图像通道事先分开。
		'''
		cv2.filter2D(src,-1,self._kernel,dst)


class SharpenFilter(ConvolutionFilter):
	"""a sharpen filter with a 1-pixel radius"""
	def __init__(self):

		kernel =np.array( [[-1,-1,-1],
				  		   [-1,9,-1],
				  		   [-1,-1,-1]])
		ConvolutionFilter.__init__(self,kernel)


class FindEdgesFilter(ConvolutionFilter):
	"""an edge-finding filter with a 1-pixel radius"""
	def __init__(self):

		kernel =np.array( [[-1,-1,-1],
				  		   [-1,8,-1],
				  		   [-1,-1,-1]])
		ConvolutionFilter.__init__(self,kernel)

		
class BlurFilter_1(ConvolutionFilter):
	"""a blur filter with a 2-pixel radius  均指平滑"""
	#为了达到模糊的效果，通常权重和应该为1，而邻近的权重为正
	def __init__(self):

		kernel =np.array( [[0.04,0.04,0.04,0.04,0.04],
				  		   [0.04,0.04,0.04,0.04,0.04],
				  		   [0.04,0.04,0.04,0.04,0.04],
				  		   [0.04,0.04,0.04,0.04,0.04],
				  		   [0.04,0.04,0.04,0.04,0.04]])
		ConvolutionFilter.__init__(self,kernel)


class BlurFilter(ConvolutionFilter):
	"""a sharpen filter with a 1-pixel radius 高斯平滑 个人体验效果更好"""
	def __init__(self):

		kernel =np.array( [[1/16,2/16,1/16],
				  		   [2/16,4/16,2/16],
				  		   [1/16,2/16,1/16]])
		ConvolutionFilter.__init__(self,kernel)


class EmbossFilter(ConvolutionFilter):
	"""an emboss(浮雕，凸出) filter with a 1-pixel radius """
	def __init__(self):
		#卷积核中心数字可修改像素亮度 越趋近于0越达到边缘检测的效果
		kernel =np.array( [[-2,-1,0],
				  		   [-1,0.8,1],
				  		   [0,1,2]])
		ConvolutionFilter.__init__(self,kernel)
		



if __name__ == '__main__':
	frame1 = cv2.imread('11.jpg')
	frame2 = cv2.imread('22.jpg')
	strokeEdges(frame1,frame1)
	# cv2.imshow('final',frame1)

	# cv2.waitKey()
	# cv2.destroyAllWindows()

	# sharpen = SharpenFilter()
	# sharpen.apply(frame1,frame1)

	# blur_img = BlurFilter()
	# blur_img.apply(frame1,frame1)
	# strokeEdges(frame1,frame1)
	# find_edges = FindEdgesFilter()
	# find_edges.apply(frame1,frame1)


	# emboss_img = EmbossFilter()
	# emboss_img.apply(frame1,frame1)

	#canny边缘检测
	# frame1 = cv2.Canny(frame1,200,300)

	cv2.imshow('final',frame1)
	cv2.waitKey()
	cv2.destroyAllWindows()

'''
卷积核
[1/9,1/9/,1/9
 1/9,1/9/,1/9
 1/9,1/9/,1/9] 平滑均指滤波:该卷积核的作用在于取九个值的平均值代替中间像素值，所以起到的平滑的效果
 
 [1/16，2/16，1/16
  2/16，4/16，2/16
  1/16，2/16，1/16] 高斯平滑：高斯平滑水平和垂直方向呈现高斯分布，更突出了中心点在像素平滑后的权重，
                     相比于均值滤波而言，有着更好的平滑效果。
                     
[-1,-1,-1],  [0,-1,0
[-1,9,-1],   -1,5,-1
[-1,-1,-1]    0,-1,0]
图像锐化:该卷积利用的其实是图像中的边缘信息有着比周围像素更高的对比度，而经过卷积之后
进一步增强了这种对比度，从而使图像显得棱角分明、画面清晰，起到锐化图像的效果。
[-1,0,1   [-1,-1,-1
 -1,0,1    0,0,0
 -1,0,1]   1,1,1]
 水平梯度卷积核  垂直梯度卷积核
 梯度Prewitt卷积核与Soble卷积核的选定是类似的，都是对水平边缘或垂直边缘有比较好的检测效果。
 
 [-1,0,1   [-1,-2,-1
  -2,0,2    0,0,0
 -1,0,1]    1,2,1]
 Soble边缘检测: Soble与上述卷积核不同之处在于，Soble更强调了和边缘相邻的像素点对边缘的影响。
 
[1,1,1], 
[1,8,-1],  
[1,1,1]
梯度Laplacian：Laplacian也是一种锐化方法，同时也可以做边缘检测，而且边缘检测的应用中
               并不局限于水平方向或垂直方向，这是Laplacian与soble的区别。
'''