import os
import requests  
from aip_speech_text import  get_speech_from_text

class Constellations(object):
	def __init__(self, arg,date="today"):
		self.arg = arg
		self.date = date
	def get_result(self):
		item ={
		"all": "综合指数", 
		"color": "幸运色", 
		"health": "健康指数",
		"love": "爱情指数",
		"money": "财运指数",
		"number": "幸运数字",
		"QFriend": "速配星座",
		"work": "工作指数",
		# "summary": "今日概述",
		}
		__AppKey = "dfed741d14ac686c1404a63a0d5303b0"
		url = "http://web.juhe.cn:8080/constellation/getAll"
		params = { "key":__AppKey,
					"consName":self.arg,
					"type":self.date
					}
		f=requests.get(url,params=params) #requests模块直接对中文进行了url解析 

		res = f.json()   #响应的json信息可以直接用json方法读出字典数据

		if res:
			if res["error_code"] == 0:
				#请求成功
				self.output_str = ""  
				for key ,value in item.items():
					# 增加特俗字符，改善语义停顿
					self.output_str += "{}:{}。\n".format(value,res[key])
				# print(self.output_str)
				return self.output_str
			else :
				print(res["error_code"],res["reason"])
		else :
			print("request api error")

	def baidu_speaker(self):
		get_speech_from_text(self.arg + self.output_str) #星座和其运势


if __name__ == '__main__':

	data = '白羊座'  
	cons = Constellations(data)          
	print(cons.get_result())
	cons.baidu_speaker()



