# -*- coding: utf-8 -*-
import scrapy
import json
from filtering.items import FilteringItem


class CaiXinSpider(scrapy.Spider):
    name = 'caixin'
    alias = '财新'
    group = '财经'
    start_urls = ['https://www.anyknew.com/api/v1/sites/caixin']

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