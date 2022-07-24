# -*- coding: utf-8 -*-
import scrapy


class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['httpbin.org','baidu.com']
    start_urls = ['http://httpbin.org/']

    def parse(self, response):
        print(response,response.encoding,'\n',response.status,response.url)
        # print(response.request)
        # print(response.urljoin)
        # print(response.selector)
        # print(response.text)
        # self.logger.debug(response.status)
        yield scrapy.Request('http://www.httpbin.org/',callback=self.parse)
