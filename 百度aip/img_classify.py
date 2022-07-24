from aip.imageclassify import AipImageClassify
import cv2 


#现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片
class ImgClassify(object):

	def __init__(self):

		appId, apiKey, secretKey = '17040087','7YToK0PSaKoMUXgVXAuF2qyo','B7hna1XZDVE49Yr3WaX16qCPYaqOjfRq'
		self.img_client = AipImageClassify(appId, apiKey, secretKey)

	def imgprocess(self,func_key,img_path=None): 
		if img_path:
			with open(img_path,'rb') as f :
				img_data = f.read()
		else:
			try:
				cameracapture = cv2.VideoCapture(0)
				ret,frame = cameracapture.read()
				if ret :
					img_data = cv2.imencode('.png',frame)[1].tobytes()
				else:
					print('打开摄像头失败')
			except:
				exit('摄像头有问题')

		#菜品和logo可以添加自己的检索库具体使用参见百度官方技术文档 https://ai.baidu.com/docs#/ImageClassify-API/722911c0
		function = {
				'通用物体识别':self.img_client.advancedGeneral,  
				'菜品识别':self.img_client.dishDetect,          
				'logo商标识别':self.img_client.logoSearch,
				'动物识别':self.img_client.animalDetect,
				'植物识别':self.img_client.plantDetect,
				'花卉识别':self.img_client.flower,        
				'食材识别':self.img_client.ingredient,
				'地标识别':self.img_client.landmark,
				'红酒识别':self.img_client.redwine,
				'货币识别':self.img_client.currency,
				'车辆识别':self.img_client.carDetect,
				 }
		#车辆检测，车流统计（邀测），车辆属性识别（邀测），车辆外观损伤识别，车辆分割（邀测）可根据需求开通权限使用
		func = function.get(func_key)

		#设置检索参数,根据需求可调。
		num = {
			'通用物体识别':{'baike_num':1},          #baike_num0~5
		  	'菜品识别':{'baike_num':1,'top_num':1,'filter_threshold':0.95}, #返回结果top n,默认5.filter_threshold默认0.95，可以通过该参数调节识别效果，降低非菜识别率.baike_num 0~10
		  	'logo商标识别':{'custom_lib':False},    #是否只检索用户子库，true则只检索用户子库，false(默认)为检索底库+用户子库
		  	'动物识别':{'baike_num':1,'top_num':1}, #baike_num0~10  top_num 	1-10返回预测得分top结果数，如果为空或小于等于0默认为5；如果大于20默认20
		  	'植物识别':{'baike_num':1},             #baike_num0~5
		  	'花卉识别':{'baike_num':1,'top_num':1}, #baike_num0~10  top_num 返回结果top n，默认5。
		  	'食材识别':{'top_num':1},               #top_num 返回预测得分top结果数，如果为空或小于等于0默认为5；如果大于20默认20
		  	'车型识别':{'baike_num':1,'top_num':1}, #baike_num0~10  top_num 返回结果top n，默认5。如果大于20默认20
		  	# '地标识别':None, 
		  	# '红酒识别':None, 
		  	# '货币识别':None,  #字典中get方法，如果key不存在就返回设置缺失值，如果不设置则返回None
		  	}
		
		option_num = num.get(func_key)
		self.response = func(img_data,options=option_num)

	def save_show(self):
		if "error_code" in self.response :
			print(self.response)
		else:
			data = self.response['result'] 
			print(data)
			return data


if __name__ == '__main__':
	app = ImgClassify()
	# app.imgprocess('菜品识别',img_path=None)
	# app.imgprocess('动物识别',img_path=None)
	app.imgprocess('植物识别',img_path=None)
	# app.imgprocess('地标识别',img_path=None)
	# app.imgprocess('花卉识别',img_path=None) #已并入植物识别中
	# app.imgprocess('货币识别',img_path='111.jpg')
	# app.imgprocess('红酒识别',img_path=None)
	# app.imgprocess('车型识别',img_path=None)
	# app.imgprocess('食材识别',img_path=None)
	# app.imgprocess('通用物体识别',img_path=None)
	# app.imgprocess('logo商标识别',img_path=None)
	app.save_show()

