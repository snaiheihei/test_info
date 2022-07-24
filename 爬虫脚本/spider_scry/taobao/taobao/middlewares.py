# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class TaobaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.
        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.
        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            print('第一批爬虫发动请求')
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from logging import  getLogger
import time

# PhantomJS是一个基于Webkit的"无界面"(headless)浏览器，它会把网站加载到内存并执行页面上的JavaScript，
# 因为不会展示图形界面，所以运行起来比完整的浏览器更高效。 注：PhantomJS宣布暂停开发

class TaobaoDownloaderMiddleware(object):

    def __init__(self,timeout=30):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        #使谷歌浏览器呈无界面模式（暂时不设置cookie）
        # self._chrome_options = Options()
        # self._chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1200,650)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser,timeout)

    def __del__(self):
        #不管是手动调用del还是由Python自动回收都会触发__del__方法执行。
        self.browser.close()
        print('selenium关闭了')

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        self.logger.debug('Chrome is staring')
        print(self.logger)
        page = request.meta.get('page',1)
        try:
            self.browser.get(request.url)
            if page>1:
                input = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainsrp-pager"]//input')))
                summit = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mainsrp-pager"]//*[@class="btn J_Submit"]')))
                input.clear()
                input.send_keys(page)
                summit.click()
            self.wait.until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="mainsrp-pager"]//*[@class="item active"]/span'),str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
            time.sleep(1)
            return HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8',status='200')
        except TimeoutException:
            return HtmlResponse(url=request.url,status=500,request=request)

        # return a Response object 更低优先级的DownLoaderMiddleware的process_request
        # 和process_exception就不会执行了转而执行process_response 需构造Response对象

        # HtmlResponse继承了Response类__init__(self, url, status=200, headers=None, body=b'', flags=None, request=None)



    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        print('下载中间件开始处理响应信息')
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

