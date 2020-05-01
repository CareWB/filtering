# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem

class TuikuSpider(scrapy.Spider):
    name = 'tuiku'
    alias = '推酷'
    group = '资讯'
    max_page_count = 3
    headers = {'Host':'www.tuicool.com',
               'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
    def start_requests(self):
        yield scrapy.Request(url='https://www.tuicool.com/ah/20/0?lang=1', 
                             headers=self.headers, 
                             meta={'dont_merge_cookies': True}, 
                             callback=self.parse)

    def parse(self, response):
        self.max_page_count -= 1
        for i in response.css('div.article'):
            item = FilteringItem()
            t = time.mktime(time.strptime(str(datetime.now().year) + '-' + \
                i.css('span.time::text').get(), "%Y-%m-%d %H:%M"))
            item['title'] = i.css('a.title::text').get().strip('\n').strip()
            item['url'] = 'https://www.tuicool.com' + i.css('a::attr(href)').get()
            item['site'] = self.alias
            item['time'] = int(t)
            item['group'] = self.group
            yield item

