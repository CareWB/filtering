# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FilteringItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    group = scrapy.Field()
    abstract = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()
    site = scrapy.Field()
