# -*- coding: utf-8 -*-
import scrapy
import json
import time
from filtering.items import FilteringItem

class XueqiuSpider(scrapy.Spider):
    name = 'eastmoney'
    alias = '东方财富'
    group = '财经'
    start_urls = ['https://www.anyknew.com/api/v1/sites/eastmoney']

    def parse(self, response):
        data = json.loads(response.text)
        sub = data['data']['site']['subs'][0]
        for i in sub['items']:
            item = FilteringItem()
            item['title'] = i['title']
            item['url'] = 'https://www.anyknew.com/go/'+str(i['iid'])
            item['time'] = int(i['add_date'])
            item['site'] = self.alias
            item['group'] = self.group
            yield item

