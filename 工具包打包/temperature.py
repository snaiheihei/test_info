import json
import requests
# 百度智能语音识别接口封装的库
from aip_speech_text import get_speech_from_text

class Temperature:
	# 数据来源：聚合数据
	__AppKey = "c63d063ffeb1f0a5bf84a4c8e298e717" 
	#建立数据映射 
	Items = { "温度" : "temperature",                
			  "湿度" : "humidity",
			  "天气情况" : "info",
			  "天气标识" : "wid",
			  "风向" : "direct",
			  "风力" : "power",
			  "空气质量指数" : "aqi" }	
	url="http://apis.juhe.cn/simpleWeather/query" 

	def __init__(self,city):  #初始化方法和普通方法原理一样
		self.city=city

	def get_result(self):
		params = {"city":self.city,"key":self.__AppKey}        
		response = requests.get(self.url,params=params).content
		result_data = json.loads(response)

		if result_data:
			# 请求成功
			if result_data['error_code'] == 0:
				result_data_now = result_data["result"]["realtime"]
				self.output_str = "" 

				for key,value in self.Items.items():
					# 增加特俗字符，改善语义停顿 。
					self.output_str += "{}:{}。\n".format(key,result_data_now[value])
				
				return self.output_str
			else :
				print(res["error_code"],res["reason"])
		else :
			print("request api error")

	def baidu_speaker(self):
		get_speech_from_text("天气助手播报"+self.city+self.output_str)


if __name__ == '__main__':
	temp=Temperature("北京")
	print(temp.get_result())
	temp.baidu_speaker()





