# -*- coding: utf-8 -*-
import scrapy
import json
from filtering.items import FilteringItem


class CnbetaSpider(scrapy.Spider):
    name = 'cnbeta'
    alias = 'cnbeta'
    group = '资讯'
    start_urls = ['https://www.anyknew.com/api/v1/sites/cnbeta']

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