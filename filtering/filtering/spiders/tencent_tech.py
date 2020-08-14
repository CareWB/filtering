# -*- coding: utf-8 -*-
import scrapy
import json
import time
from filtering.items import FilteringItem

class TencentTechSpider(scrapy.Spider):
    name = 'tencent_tech'
    alias = '腾讯技术工程'
    group = '技术'

    def start_requests(self):
        headers = {
                'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
        urls = ['https://www.zhihu.com/api/v4/columns/tencent-TEG/items']
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        for i in data['data']:
            item = FilteringItem()
            item['title'] = i['title']
            item['url'] = i['url']
            item['time'] = int(i['created'])
            item['site'] = self.alias
            item['group'] = self.group
            yield item
