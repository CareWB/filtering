# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
import json
import time
from filtering.items import FilteringItem

class InfoQSpider(XMLFeedSpider):
    name = 'infoq'
    alias = 'InfoQ'
    group = '技术'

    start_urls = ['https://www.infoq.cn/feed.xml']
    itertag = 'item'

    def parse_node(self, response, selector):
        item = FilteringItem()
        item['title'] = selector.css("title::text").extract_first()
        item['url'] = selector.css("link::text").extract_first()
        t = time.mktime(
            time.strptime(selector.css("pubDate::text").extract_first(), 
            "%a, %d %b %Y %H:%M:%S GMT")
        )
        item['time'] = int(t)
        item['site'] = self.alias
        item['group'] = self.group
        yield item

