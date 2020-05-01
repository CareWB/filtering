# -*- coding: utf-8 -*-
import scrapy
import json
from filtering.items import FilteringItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    alias = '微博'
    group = '新闻娱乐'
    start_urls = ['https://www.anyknew.com/api/v1/sites/weibo']

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