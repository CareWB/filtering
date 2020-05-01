# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
import json
import time
from filtering.items import FilteringItem

class MeituanSpider(XMLFeedSpider):
    name = 'meituan'
    alias = '美团技术团队'
    group = '技术'

    start_urls = ['https://tech.meituan.com/feed/']
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

