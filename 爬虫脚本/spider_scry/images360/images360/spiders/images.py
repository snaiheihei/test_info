# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
from images360.items import Images360Item


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def start_requests(self):
        data  = {'ch':'photography','listtype':'new','temp':1}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1,self.settings.get('MAX_PAGE')+1):
            data['sn'] = page*30
            params = urlencode(data)
            url = base_url+params
            yield scrapy.Request(url,self.parse)

    def parse(self, response):
        print(response)
        result = json.loads(response.text)
        for image in result['list']:
            item = Images360Item()
            item['Id'] = image.get('id')
            item['url'] = image.get('imgurl')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            print('请求图片信息成功')
            yield item


       # http://m2.quanjing.com/2m/irish_rm001/isish1817841.jpg
       # https://p0.ssl.qhimgs1.com/bdr/326__/t01a9e11720c9189b04.jpg