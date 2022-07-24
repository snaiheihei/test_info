# -*- coding: utf-8 -*-
import requests 
import re
import json

def get_one_page(url):
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
	responce = requests.get(url,headers = header)
	# print(responce.status_code)
	if responce.status_code == 200:
		return responce.content.decode()
	return None
def parse_one_page(html):
	pattern_1 = re.compile('<div class="number"><em>(.*?)</em>',re.S)
	num = re.findall(pattern_1,html)

	pattern_2 = re.compile('<div class="mov_pic".*?title="(.*?)/.*?<img.*?src="(.*?)".*?</div>',re.S)
	name_img = re.findall(pattern_2,html)

	for i,j in zip(num,name_img):
		yield {
				'index':i,
				'name':j[0],
				'img':j[1]
			}
def write_to_file(data):
	# with open('result.txt','a',encoding = 'utf-8') as f:
	# 	f.write(json.dumps(data,ensure_ascii=False)+'\n')
	with open('result.json','a',encoding = 'utf-8') as f:
		f.write(json.dumps(data,ensure_ascii=False)+'\n')
	

if __name__ == '__main__':
	for i in range(1,11):
		if i == 1:
			url = 'http://www.mtime.com/top/movie/top100/'
		else:
			url = 'http://www.mtime.com/top/movie/top100/index-' + str(i) +'.html'

		html = get_one_page(url)
		data = parse_one_page(html)
		print(url,'写入第%d页内容'%i)
		for i in data:
			write_to_file(i)


'''
观察规律，提取出正则表达式
<div class="number"><em>(.*?)</em>
<div class="mov_pic".*?title="(.*?)/.*?<img.*?src="(.*?)".*?</div>
<div class="mov_point".*?"total">(.*?)</span>.*?"total2">(.*?)</span>

'''