from aip.bodyanalysis import AipBodyAnalysis
import cv2 
import base64
from PIL import Image 
import os

class Body(object):

	def __init__(self):

		appId, apiKey, secretKey = '16950263','7TytBlO1d4RFCn9SObskRuCR','M670medKybo4g310lsHt85EoScxCUiaA'
		self.img_client = AipBodyAnalysis(appId, apiKey, secretKey)
	
	def imgprocess(self,func_key,img_path=None):

		if img_path:
			with open(img_path,'rb') as f :
				img_data = f.read()
		else:
			try:
				cameracapture = cv2.VideoCapture(0)
				ret,frame = cameracapture.read()
				if ret:
					img_data = cv2.imencode('.png',frame)[1].tobytes()
				else:
					print('打开摄像头失败')
			except:
				exit('摄像头有问题')

		function = {
				'人体关键点识别':self.img_client.bodyAnalysis,  
				'人体检测与属性识别':self.img_client.bodyAttr,          
				'人流量统计':self.img_client.bodyNum,
				'手势识别':self.img_client.gesture,
				'人像分割':self.img_client.bodySeg,
				'驾驶行为分析':self.img_client.driverBehavior,        
				# '人流量统计-动态版':self.img_client.bodyTracking,
				 }

		fun = function.get(func_key)  
		options = {
			'人体检测与属性识别':{'type':"gender,age,headwear,glasses,orientation,upper_wear,smoke,lower_cut"},       
		  	'人流量统计':{'area':None,'show':True}, #是否输出渲染的图片，默认不返回，选true时返回渲染后的图片(base64)，其它无效值或为空则默认false
		  	'人像分割':{'type':'scoremap,foreground'}, # labelmap 二值图像，需二次处理方能查看分割效果  scoremap - 人像前景灰度图  foreground - 人像前景抠图，透明背景
		  	'驾驶行为分析':{'type':'smoke,cellphone,not_buckling_up,both_hands_leaving_wheel,not_facing_front'},
		  	#'人流量统计-动态版':{"case_id":"11","case_init":False,"show":True,"area":100},
		  	}
		option_type = options.get(func_key,None)

		self.response = fun(img_data,options=option_type)   #'人流量统计-动态版'添加dynamic=True

	def save_show(self):
		if "error_code" in self.response :
			print(self.response)
		else:

			data = self.response
			if 'image' in data:
				image_data = base64.b64decode(data.get('image')) 
				with open('99.jpg','wb') as f:
					f.write(image_data)
				img_show = Image.open('99.jpg')
				del data['image']
				print('经过渲染的图片：',img_show.format,img_show.mode,img_show.size)
				img_show.show()
				os.remove('99.jpg')

			if 'foreground'in data:
				image_data = base64.b64decode(data.get('foreground')) 
				with open('98.jpg','wb') as f:
					f.write(image_data)
				img_show = Image.open('98.jpg')
				del data['foreground']
				print('人像前景抠图，透明背景：',img_show.format,img_show.mode,img_show.size)
				img_show.show()
				os.remove('98.jpg')
			if 'scoremap'in data:
				image_data = base64.b64decode(data.get('scoremap')) 
				with open('97.jpg','wb') as f:
					f.write(image_data)
				img_show = Image.open('97.jpg')
				del data['scoremap']
				print('人像前景灰度图：',img_show.format,img_show.mode,img_show.size)
				img_show.show()
				os.remove('97.jpg')			

			print(data)
			return data


if __name__ == '__main__':
	app = Body()
	# app.imgprocess('人体关键点识别')
	# app.imgprocess('人体检测与属性识别')
	# app.imgprocess('人流量统计')
	# app.imgprocess('手势识别')
	app.imgprocess('人像分割')
	# app.imgprocess('驾驶行为分析')
	app.save_show()