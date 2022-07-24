from pyquery import PyQuery as pq 
import requests
import json
import pandas as pd
# import pymysql

def get_one_page(url):
	header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
	responce = requests.get(url,headers = header)
	if responce.status_code == 200:
		return responce.content.decode()
	else:
		return None

def parse_one_page(html):
	doc = pq(html)

	num = doc('.number em')
	index = []
	for i in num.items():
		index.append(i.text())

	title = doc('.mov_pic a')
	name = []
	for i in title.items():
		name.append(i.attr('title'))
	name = [i.split('/')[0] for i in name ]

	pic = doc.find('.img_box')
	img = []
	for i in pic.items():
		img.append(i.attr.src)

	point = doc.find('.point')
	score = []
	for i in point.items():
		score.append(i.text())

	for item in zip(index,name,score,img):
		yield {
				'index':item[0],
				'name':item[1],
				'score':item[2],
				'img':item[3]
		}


def write_to_file(data):
	with open('result.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(data,ensure_ascii=False) + '\n')

	with open('result.json','a',encoding = 'utf-8') as f:
		f.write(json.dumps(data,ensure_ascii=False)+'\n')

def write_sql(data,aql=None,args=None): #方便扩展
	con = pymysql.connect(host='192.168.0.122',user='root',password='123456',database='dingce_demo',charset='utf8')
	cur = con.cursor()
	sql = "insert into movie values(%s,%s,%s,%s)"
	args = (data['index'],data['name'],data['score'],data['img'])
	try:
		cur.execute(sql,args)
		con.commit()
	except Exception as e:
		con.rollback()
		print(e)
	finally:
		con.close()



if __name__ == '__main__':
	# 所有数据字典列表，方便pandas使用
	dic_pd = []

	for i in range(1,11):
		if i == 1:
			url = 'http://www.mtime.com/top/movie/top100/'
		else:
			url = 'http://www.mtime.com/top/movie/top100/index-' + str(i) +'.html'

		html = get_one_page(url)
		result = parse_one_page(html)
		print(url,'写入第%d页内容'%i)
		for data in result:
			# 写入csv为pandas提供数据
			# dic_pd.append(data)
			# 写入.txt .json文件
			write_to_file(data)
			# 写入到mysql中
			# write_sql(data)

	# 使用pandas将字典列表整体写入csv文件
	# data = pd.DataFrame(dic_pd)
	# data.index = data.pop('index')
	# data.to_csv('result.csv',encoding='utf-8')


