# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem
from scrapy.spiders import XMLFeedSpider

class TedSpider(XMLFeedSpider):
    name = 'kk'
    alias = 'KK'
    group = '海外'

    start_urls = ['https://kk.org/thetechnium/']

    def parse(self, response):
        c = response.css('div.maincontent')
        for i in range(len(response.css('h2'))):
            item = FilteringItem()
            item['title'] = response.css('h2 a::text')[i].get()
            item['url'] = response.urljoin(response.css('h2 a::attr(href)')[i].get())
            commentnum = response.css('div#commentnum')[i]
            t = time.mktime(
                time.strptime(commentnum.css('a::text').get(), 
                "%B %d, %Y")
            )
            item['time'] = int(t)
            item['site'] = self.alias
            item['group'] = self.group
            yield item
