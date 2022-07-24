from aip.imageprocess import AipImageProcess 
import base64


appId, apiKey, secretKey = '17040087','7YToK0PSaKoMUXgVXAuF2qyo','B7hna1XZDVE49Yr3WaX16qCPYaqOjfRq'
image_client = AipImageProcess(appId, apiKey, secretKey)
function = {'图片无损放大':image_client.imageQualityEnhance,
			'图片对比度增强':image_client.contrastEnhance,
			'黑白图像上色':image_client.colourize,
			'拉伸图像恢复':image_client.stretch_restore,
			'图像风格转换':image_client.style_trans}

styles = {'卡通画风格':{'option':'cartoon'},
		  '素描风格':{'option':'pencil'},
		  '油画风格（即将上线）':{'option':'painting'}}
						                           

def run(opath,spath,fun,option=None):
	with open(opath,'rb') as f1:
		image=f1.read()

# image=f1.read()
# print(image)   图片以二进制读入是字节码形式
# print(base64.b64encode(b'hello'))  #base64.b64encode(字节码)
# data1=base64.b64encode(image).decode()     #b'/9j/4AAQSkZJRgABAQAAAQABA  base64字节码可以解码成字符串
# print(type(data1))
# data2=base64.b64decode(data1)    #b64decode 方法讲base64加密的数据还原成字节码 b'xx'  图片等形式的二进制不可以被解码成str 
# print(data2)	
	try:
		result=fun(image,options=option)
		data=base64.b64decode(result['image'])
		with open(spath,'wb') as f2:
			f2.write(data)
	except:
		print(result)


if __name__ == '__main__':
	
	# run('cc.jpg','01.jpg',function['图片无损放大'])
	# run('cc.jpg','02.jpg',function['图片对比度增强'])
	# run('smallcc.jpg','03.jpg',function['黑白图像上色'])
	# run('03.jpg','04.jpg',function['图像风格转换'],option=styles['卡通画风格'])
	run('cc.jpg','05.jpg',function['图像风格转换'],option=styles['素描风格'])






'''
图像色彩还原测试
if True:
	import numpy as np
	from PIL import Image
	img = Image.open(r"1.jpg")
	img2 = img.convert('L')
	img2.show()
	img2.save(r"2.jpg")

'''





#将图片部分区域改色
if False:
	import numpy as np
	from PIL import Image
	img = Image.open(r"aa.jpg")
	print(img.format)
	print(img.mode)
	print(img.size)
	arr1=np.array(img)
	print(arr1.ndim)
	print(arr1.shape)
	print(arr1.dtype)
	print(len(arr1[0]))

#array数据的切片
	# for row in range(123):
	# 	for col in range(500):
	# 		arr1[row][col]=74
	arr1[:123,:500]=74

	# for row in range(1550,1620):
	# 	for col in range(745,1080):
	# 		arr1[row][col]=217
	arr1[1550:1620,745:1080]=217

	new_im = Image.fromarray(arr1)
	new_im.show()
	new_im.save(r"aa0.jpg")

