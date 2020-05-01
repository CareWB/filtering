# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem
from scrapy.spiders import XMLFeedSpider

class TedSpider(XMLFeedSpider):
    name = 'ted'
    alias = 'TED'
    group = '海外'

    headers = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    def start_requests(self):
        yield scrapy.Request(url='https://www.ted.com/talks', 
                             headers=self.headers, 
                             callback=self.parse)

    def parse(self, response):
        for i in response.css('div.media__message'):
            item = FilteringItem()
            t = time.mktime(time.strptime(
                i.css('span.meta__val::text').get().strip('\n').strip(), "%b %Y"))
            item['title'] = i.css('a.ga-link::text').get().strip('\n').strip()
            item['url'] = 'https://www.ted.com' + i.css('a::attr(href)').get()
            item['site'] = self.alias
            item['time'] = int(t)
            item['group'] = self.group
            yield item
