#从百度aip上获取图像解析结果
from aip.imageprocess import AipImageProcess
#解码网络返回的图片数据
import base64
#展示返回的图像
from PIL import Image
#读取本地图像数据并编码成bytes类型传输，或者俘获摄像头抓取图片并编码 
import cv2

class ImgProcess(object):

	def __init__(self):

		appId, apiKey, secretKey = '17040087','7YToK0PSaKoMUXgVXAuF2qyo','B7hna1XZDVE49Yr3WaX16qCPYaqOjfRq'
		self.image_client = AipImageProcess(appId, apiKey, secretKey)

	def process(self,func_key,options=None,img_path=None):

		if img_path:
			# with open(img_path,'rb') as f :
			# 	img_data =f.read()
			#使用cv2读取本地图片数据，编码传输
			img_data_array = cv2.imread(img_path)
			img_data = cv2.imencode('.png',img_data_array)[1].tobytes()
		else:
			try:
				cameracapture = cv2.VideoCapture(0)
				ret,frame = cameracapture.read()
				if ret:
					#讲从cv2中<class 'numpy.ndarray'>数组编码成传输数据<class 'bytes'>
					img_data = cv2.imencode('.png',frame)[1].tobytes()
				else:
					print('摄像头打开失败')
			except:
				exit('摄像头有问题')
		function = {
				'图片无损放大':self.image_client.imageQualityEnhance,
				'图片对比度增强':self.image_client.contrastEnhance,
				'黑白图像上色':self.image_client.colourize,
				'图像去雾':self.image_client.dehaze,
				'拉伸图像恢复':self.image_client.stretch_restore,
				'图像风格转换':self.image_client.style_trans }
		styles = {
			'卡通画风格':{'option':'cartoon'},
		  	'素描风格':{'option':'pencil'},
		  	'油画风格（即将上线）':{'option':'painting'}}
		style = styles.get(options)
		func=function.get(func_key)
		self.response = func(img_data,options=style)

	def save_show(self,img_path):

		if 'error_code' in self.response :
			print(self.response)
		elif 'image' in self.response:
			data = base64.b64decode(self.response['image'])
			#使用文件句柄 写入更方便直接
			with open(img_path,'wb') as f:
				f.write(data)

			# img_new_array = cv2.imread(img_path)
			# cv2.imshow('newframe',img_new_array)
			# cv2.waitKey()
			# cv2.destroyAllWindows()

			img_show = Image.open(img_path)
			print('你的图片转换好了，请查看：',img_show.format,img_show.mode,img_show.size)
			img_show.show()
		else:
			pass


if __name__ == '__main__':

	app = ImgProcess()
	app.process('图片无损放大',img_path=None,options=None)
	app.save_show('22.jpg')







'''
#base64 64个字符A-Z(26个),a-z,0-9+/

Base 64 Encoding有什么用？举个简单的例子，你使用SMTP协议 
（Simple Mail Transfer Protocol 简单邮件传输协议）来发送邮件。
因为这个协议是基于文本的协议，所以如果邮件中包含一幅图片，
我们知道图片的存储格式是二进制数据（binary data），而非文本格式，
我们必须将二进制的数据编码成文本格式，这时候Base 64 Encoding就派上用场了。

base64其实不是安全领域下的加密解密算法。虽然有时候经常看到所谓的base64加密解密。
其实base64只能算是一个编码算法，对数据内容进行编码来适合传输。
虽然base64编码过后原文也变成不能看到的字符格式，但是这种方式很初级，很简单。
'''