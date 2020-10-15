# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import XMLFeedSpider
import json
import time
from filtering.items import FilteringItem

class HackNewsSpider(XMLFeedSpider):
    name = 'martinfowler'
    alias = 'martinfowler'
    group = '海外'

    start_urls = ['https://martinfowler.com/feed.atom']
    itertag = 'entry'

    def parse_node(self, response, selector):
        print('111111111111')
        item = FilteringItem()
        item['title'] = selector.css("title::text").extract_first()
        item['url'] = selector.css("link::href").get()
        t = time.mktime(
            time.strptime(selector.css("updated::text").extract_first(), 
            "%Y-%m-%dT%H:%M:%S-04:00")
        )
        item['time'] = int(t)
        item['site'] = self.alias
        item['group'] = self.group
        print(item)

