import time
import requests
import hashlib
import random

class Fanyi(object):

	def __init__(self):
		
		self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
		self.headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
					'Referer': 'http://fanyi.youdao.com/',
					'Cookie': 'OUTFOX_SEARCH_USER_ID=-715609565@10.169.0.83; JSESSIONID=aaa933YC_a6tX9j9JwtZw; OUTFOX_SEARCH_USER_ID_NCOO=1189895985.893742; ___rl__test__cookies=1566955764835'
		}

	def translate(self,word):
		'''
		从网页请求js信息中 解析参数形成 构造参数
		时间戳 md5数据加密（将不定长二进制字符串加成成定长32位字符串）
		ts salt sign
		'''
		self.word = word
		timestamp = time.time()*1000
		salt = str(timestamp)+str(random.randint(0,10))
		temp = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
		sign = hashlib.md5(temp.encode()).hexdigest()

		data = {
				'i': self.word,
				'from': 'AUTO',
				'to': 'AUTO',
				'smartresult': 'dict',
				'client': 'fanyideskweb',
				'salt': salt,
				'sign': sign,
				'ts': timestamp,
				'bv': '53539dde41bde18f4a71bb075fcf2e66',
				'doctype': 'json',
				'version': '2.1',
				'keyfrom': 'fanyi.web',
				'action': 'FY_BY_REALTlME',
		}

		response = requests.post(self.url,data=data,headers=self.headers).json()
		
		result = response['translateResult'][0][0]['tgt']
		return result
	def read_word(self):
		from playsound import playsound  #传入一个本地文件
		from os import remove
		url = 'http://tts.youdao.com/fanyivoice?'
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
		words = ' '.join([x.strip() for x in self.word.split(' ')]) #一般字符串处理流程（此步可以去掉）
		wd = {'word':words}
		response = requests.get(url,headers=headers,params=wd).content
		with open('audio1.mp3','wb') as f:
			f.write(response)
		playsound('audio1.mp3')
		remove('audio1.mp3')






if __name__ == '__main__':
	fanyi = Fanyi()
	print(fanyi.translate('Everybody is good'))
	fanyi.read_word()




'''
请求音频文件分析：

http://tts.youdao.com/fanyivoice?word=hello&le=eng&keyfrom=speaker-target
http://tts.youdao.com/fanyivoice?word=Everybody%20is%20good&le=eng&keyfrom=speaker-target

'''


'''
js 中函数 返回formdata所需的参数

var r = function(e) {
        var t = n.md5(navigator.appVersion)
          , r = "" + (new Date).getTime()  字符串类型时间戳
          , i = r + parseInt(10 * Math.random(), 10);  r+ 0到10的随机数
        return {
            ts: r,  时间戳
            bv: t,  n.md5(navigator.appVersion)
            salt: i,  时间戳+0到10的随机数
            sign: n.md5("fanyideskweb" + e + i + "n%A-rKaT5fb[Gy?;N5@Tj")
        }


fromdata中不同信息比对 构造不同信息的方法
salt: 15669564904583
sign: 4c4a8cd08077429925f404a147d905e5
ts: 1566956490458

2.
salt: 15669564911046
sign: 4605ceb64ec4d226aab32361f8908c51
ts: 1566956491104

'''
