# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

class Img360Pipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        print(results)
        image_path = [x['path'] for ok,x in results if ok]
        print('第1管道开始处理item信息')
        if not image_path:
            raise DropItem('Image Downloaded Failed')
        return item


    def get_media_requests(self, item, info):
        print('第1管道发动下载请求',item['thumb'])

        yield Request(item['thumb'])


class Images360Pipeline(object):
    def process_item(self, item, spider):
        print('第2管道开始处理item信息')
        return item




