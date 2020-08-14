# -*- coding: utf-8 -*-
import scrapy
import json
import time
from filtering.items import FilteringItem

class AliTechSpider(scrapy.Spider):
    name = 'ali_tech'
    alias = '阿里技术'
    group = '技术'

    def start_requests(self):
        headers = {
               'User-Agent':'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36'}
        urls = ['https://www.zhihu.com/org/a-li-ji-zhu']
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        for i in response.css('div.ContentItem.ArticleItem'):
            item = FilteringItem()
            item['title'] = i.css('[itemprop=headline]::attr(content)').get()
            item['url'] = 'https:' + i.css('a::attr(href)').get()
            t = i.css('[itemprop=datePublished]::attr(content)').get()
            t = time.mktime(time.strptime(t, "%Y-%m-%dT%H:%M:%S.000Z"))
            item['time'] = int(t)
            item['site'] = self.alias
            item['group'] = self.group
            yield item
