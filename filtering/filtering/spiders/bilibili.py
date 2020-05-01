# -*- coding: utf-8 -*-
import scrapy
import json
from filtering.items import FilteringItem
import time


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    alias = 'bilibili'
    group = '新闻娱乐'
    start_urls = ['https://api.bilibili.com/x/web-interface/ranking?rid=0&day=1&type=1&arc_type=0&jsonp=jsonp']

    def parse(self, response):
        data = json.loads(response.text)
        sub = data['data']
        for i in sub['list']:
            item = FilteringItem()
            item['title'] = i['title']
            item['url'] = 'https://www.bilibili.com/video/'+str(i['bvid'])
            item['time'] = int(time.time())
            item['site'] = self.alias
            item['group'] = self.group
            yield item