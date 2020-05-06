from flask import Flask
from flask import jsonify
from flask import Response
import json
import pymysql
import time
from filtering.settings import *
import jieba
from collections import Counter
from dbhelper import POOL

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
jieba.load_userdict('./worddict.txt') 

def get_cursor():
    conn = POOL.connection()
    cursor = conn.cursor()
    return cursor

@app.route('/api/groups',methods=['GET'])
def groups():
    sql = "select distinct GP, SITE FROM NEWS"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    group_site = {}
    for r in result:
        group_site.setdefault(r[0],[]).append(r[1])
    return json.dumps(group_site, ensure_ascii=False)

def get_titles(group):
    t = time.localtime(int(time.time()-60*60*24*7))
    dt = time.strftime("%m-%d %H:%M", t)
    sql = "SELECT TITLE FROM NEWS WHERE GP=%s AND TIME>=%s"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, (group,dt,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_words(titles):
    stops_words = load_stop_words()
    words = []
    seg_list = jieba.cut(str(titles), cut_all=False)
    for w in seg_list:
        if len(w.strip())>0 and (w not in stops_words):
            words.append(w)
    return dict(Counter(words))

def load_stop_words():
    stopwords = []
    with open('./stopwords.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            if len(line)>0:
                stopwords.append(line.strip())
    return stopwords

@app.route('/api/hotwords/<group>',methods=['GET'])
def hotwords(group):
    titles = get_titles(group)
    w = get_words(titles)
    w = (sorted(w.items(),key=lambda x:x[1], reverse=True)[:9])
    print(w)

    return json.dumps(w, ensure_ascii=False)

@app.route('/api/group_news/<group>',methods=['GET'])
def group_news(group):
    t = time.localtime(int(time.time()-60*60*24*7))
    dt = time.strftime("%m-%d %H:%M", t)

    sql = "SELECT ID, SITE, TITLE, URL, TIME FROM NEWS WHERE GP=%s ORDER BY TIME DESC,SN LIMIT 100;"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, (group,))
    result = cursor.fetchall()
    conn.close()

    itmes = []
    for r in result:
        itmes.append({
                    'id':r[0],
                    'site':r[1],
                    'title':r[2],
                    'url':r[3],
                    'time':r[4]})

    return json.dumps({'news':itmes}, ensure_ascii=False)

@app.route('/api/sites/<site>',methods=['GET'])
def news(site):
    t = time.localtime(int(time.time()-60*60*24*7))
    dt = time.strftime("%m-%d %H:%M", t)

    sql = "SELECT ID, SITE, TITLE, URL, TIME FROM NEWS WHERE SITE=%s ORDER BY TIME DESC,SN LIMIT 100"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, (site,))
    result = cursor.fetchall()
    conn.close()

    itmes = []
    for r in result:
        itmes.append({
                    'id':r[0],
                    'site':r[1],
                    'title':r[2],
                    'url':r[3],
                    'time':r[4]})

    return json.dumps({'site':site,'news':itmes}, ensure_ascii=False)

@app.route('/api/hotword/<group>/<word>',methods=['GET'])
def hotword(group, word):
    t = time.localtime(int(time.time()-60*60*24*7))
    dt = time.strftime("%m-%d %H:%M", t)

    sql = "SELECT ID, SITE, TITLE, URL, TIME FROM NEWS WHERE GP=%s AND TIME>=%s AND TITLE LIKE %s ORDER BY TIME DESC,SN"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, (group,dt,'%'+word+'%',))
    result = cursor.fetchall()
    conn.close()

    itmes = []
    for r in result:
        itmes.append({
                    'id':r[0],
                    'site':r[1],
                    'title':r[2],
                    'url':r[3],
                    'time':r[4]})

    return json.dumps({'site':'','news':itmes}, ensure_ascii=False)

@app.route('/api/search/<word>',methods=['GET'])
def search(word):
    sql = "SELECT ID, SITE, TITLE, URL, TIME FROM NEWS WHERE TITLE LIKE %s ORDER BY TIME DESC,SN"
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, ('%'+word+'%',))
    result = cursor.fetchall()
    conn.close()

    itmes = []
    for r in result:
        itmes.append({
                    'id':r[0],
                    'site':r[1],
                    'title':r[2],
                    'url':r[3],
                    'time':r[4]})

    return json.dumps({'site':'','news':itmes}, ensure_ascii=False)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8100)
