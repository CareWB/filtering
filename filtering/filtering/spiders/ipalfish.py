# -*- coding: utf-8 -*-
import scrapy
import json
import time
from filtering.items import FilteringItem

class AicampSpider(scrapy.Spider):
    name = 'ipalfish'
    alias = '伴鱼技术团队'
    group = '技术'

    start_urls = ['https://tech.ipalfish.com/blog/archives/']

    def parse(self, response):
        for article in response.css('article'):
            item = FilteringItem()
            item['title'] = article.css('span::text').get()
            item['url'] = response.urljoin(article.css('a::attr(href)').get())
            t = time.mktime(
                time.strptime(article.css('time::attr(content)').get(), 
                "%Y-%m-%d")
            )
            item['time'] = int(t)
            item['site'] = self.alias
            item['group'] = self.group
            yield item
            
        # next_page = response.css('nav.pagination a[rel="next"]::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        

