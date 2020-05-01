import time
import os
from filtering.settings import *

import pymysql

def get_spiders():
    spiders = []
    r = os.popen("scrapy list")
    spiders = r.readlines()
    r.close()
    return spiders

def del_outdate_news():
    db_conn =pymysql.connect(host=MYSQL_IP, 
                             port=MYSQL_PORT, 
                             db=MYSQL_DB, 
                             user=MYSQL_USER, 
                             passwd=MYSQL_PW, 
                             charset='utf8')
    db_cur = db_conn.cursor()

    sql = 'DELETE FROM NEWS WHERE TIME<%s'

    t = time.localtime(int(time.time()-60*60*24*30))
    dt = time.strftime("%m-%d %H:%M",t)

    db_cur.execute(sql, (dt,))

    db_conn.commit()
    db_cur.close()
    db_conn.close()

if __name__ == '__main__':
    while True:
        spiders = get_spiders()
        del_outdate_news()
        for s in spiders:
            os.system("scrapy crawl {}".format(s.strip('\n')))
            time.sleep(30)
        time.sleep(3600)

