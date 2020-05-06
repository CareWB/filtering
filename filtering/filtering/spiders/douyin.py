# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem

class DouYinSpider(scrapy.Spider):
    name = 'douyin'
    alias = '抖音'
    group = '新闻娱乐'

    start_urls = ['https://creator.douyin.com/aweme/v1/creator/data/billboard/?billboard_type=4']

    def parse(self, response):
        data = json.loads(response.text)
        sub = data['billboard_data']
        for i in sub:
            item = FilteringItem()
            item['title'] = i['title']
            item['url'] = i['link']
            item['site'] = self.alias
            item['time'] = int(data['extra']['now']/1000)
            item['group'] = self.group
            yield item


