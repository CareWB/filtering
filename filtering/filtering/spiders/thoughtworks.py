# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem
from scrapy.spiders import XMLFeedSpider

class TedSpider(XMLFeedSpider):
    name = 'thoughtworks'
    alias = 'TW洞见'
    group = '技术'

    start_urls = ['https://insights.thoughtworks.cn/feed/']
    itertag = 'item'

    def parse_node(self, response, selector):
        item = FilteringItem()
        item['title'] = selector.css("title::text").extract_first()
        item['url'] = selector.css("link::text").extract_first()
        t = time.mktime(
            time.strptime(selector.css("pubDate::text").extract_first(), 
            "%a, %d %b %Y %H:%M:%S +%f")
        )
        item['time'] = int(t)
        item['site'] = self.alias
        item['group'] = self.group
        yield item
