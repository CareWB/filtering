# -*- coding: utf-8 -*-
import scrapy
import json
import time
from filtering.items import FilteringItem

class AicampSpider(scrapy.Spider):
    name = 'aicamp'
    alias = 'AI科技大本营'
    group = '技术'

    def start_requests(self):
        headers = {'Host':'www.waijiedanao.com'}
        urls = ['https://www.waijiedanao.com/api/posts?page=1&limit=50&profile=5dae904ea9a67271c3720487&q=&isOriginal=false']
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        for i in data['data']:
            item = FilteringItem()
            t = time.mktime(time.strptime(i['publishAt'], "%Y-%m-%dT%H:%M:%S.000Z"))
            item['title'] = i['title']
            item['url'] = i['link']
            item['time'] = int(t)
            item['site'] = self.alias
            item['group'] = self.group
            yield item
