# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from taobao.items import TaobaoItem


class TaoSpider(scrapy.Spider):
    name = 'tao'
    allowed_domains = ['www.taobao.com']
    start_urls = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1,self.settings.get('MAX_PAGE')+1):
                url = self.start_urls + quote(keyword)
                #scrapy有对request对象去重功能
                yield scrapy.Request(url,callback=self.parse,meta={'page':page},dont_filter=True)



    def parse(self, response):
        print(response)
        products = response.xpath('//*[@class="m-itemlist"]//div[@class="items"]/div[contains(@class,"item")]')
        for product in products:
            item = TaobaoItem()
            item['price'] = ''.join(product.xpath('.//div[contains(@class,"price")]//text()').extract()).strip()
            item['title'] = ''.join(product.xpath('.//a[@class="J_ClickStat"]//text()').extract()).strip()
            item['shop'] = ''.join(product.xpath('.//a[contains(@class,"shopname")]//text()').extract()).strip()
            item['image'] = product.xpath('.//img[@class="J_ItemPic img"]/@data-src').extract_first()
            item['deal'] = product.xpath('.//div[@class="deal-cnt"]/text()').extract_first()
            yield item
