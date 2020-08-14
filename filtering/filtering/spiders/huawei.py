# -*- coding: utf-8 -*-
import scrapy
import json
import time
from datetime import datetime
from filtering.items import FilteringItem

class TuikuSpider(scrapy.Spider):
    name = 'huawei'
    alias = '人工智能园地'
    group = 'HW'
    max_page_count = 3
    headers = {}
    def start_requests(self):
        yield scrapy.Request(url='https://bbs.huaweicloud.com/forum/forum.php?mod=forumdisplay&fid=719&orderby=lastpost&thelimit=all&filter=typeid&typeid=545&page=1',
                             callback=self.parse)

    def parse(self, response):
        self.max_page_count -= 1
        for r in response.css('.showul .section-post-mess'):
            item = FilteringItem()
            thread = r.css("a[href^='thread']")
            item['title'] = thread.css("::text").extract()[0]
            item['url'] = 'https://bbs.huaweicloud.com/forum/' + thread.css('::attr(href)').extract()[0]
            t = r.css('.section-time-info span')
            if t.css('::attr(title)'):
                t = t.css('::attr(title)').extract()[0]
            else:
                t = t.css('::text').extract()[1]
            t = time.mktime(time.strptime(t, "%Y-%m-%d"))
            item['time'] = int(t)
            item['site'] = self.alias
            item['group'] = self.group
            yield item

