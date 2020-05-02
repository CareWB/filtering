# -*- coding: utf-8 -*-
from scrapy.exporters import CsvItemExporter
import zlib
from filtering.settings import *
import time
import pymysql

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class FilteringPipeline(object):
    def open_spider(self, spider):
        self.db_conn =pymysql.connect(host=MYSQL_IP, 
                                      port=MYSQL_PORT, 
                                      db=MYSQL_DB, 
                                      user=MYSQL_USER, 
                                      passwd=MYSQL_PW, 
                                      charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_cur.close()
        self.db_conn.close()

    def process_item(self, item, spider):
        id_str = item['url'] if item['url'] else item['title']
        item['id'] = zlib.crc32(id_str.encode('utf8'))
        
        t = time.localtime(int(item['time']))
        dt = time.strftime("%m-%d %H:%M",t)

        values = (
            int(item['id']),
            item['group'],
            item['site'],
            item['title'],
            item['url'],
            dt,
        )

        sql = 'REPLACE INTO NEWS (ID, GP, SITE, TITLE, URL, TIME) VALUES(%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)

        return item