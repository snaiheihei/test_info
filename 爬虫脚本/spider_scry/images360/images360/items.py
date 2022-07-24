# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Images360Item(scrapy.Item):
    # define the fields for your item here like:
    Id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    thumb = scrapy.Field()
    
