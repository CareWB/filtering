import asyncio
import traceback
import json
from collections import Counter

from aiofile import AIOFile, Writer, Reader
import jieba
from pyecharts.charts import WordCloud

config = None

class manager:
    def __init__(self, sites = []):
        self.sites = sites

    async def run(self):
        for site in self.sites:
            await site.run()

    async def save(self):
        data = {'sites':[]}
        for site in self.sites:
            data['sites'].append(await site.save())

        async with AIOFile(config['output'], 'w') as afp:
            writer = Writer(afp)
            await writer(json.dumps(data, ensure_ascii=False))
            await afp.fsync()

async def analyse():
    title = ''
    stops_words = load_stop_words()
    async with AIOFile(config['output'], 'r') as afp:
        contents = json.loads(await afp.read())
        for s in contents['sites']:
            title += ' '.join([n['title'] for n in s['news']])
    
    seg_list = jieba.cut(title, cut_all=False)
    words = []
    for w in seg_list:
        if w not in stops_words:
            words.append(w)

    mywordcloud=WordCloud()
    mywordcloud.add('',filter(lambda v: v[1]>3, Counter(words).items()), \
        shape='pentagon', word_size_range=(10, 500))
    mywordcloud.render(config['wordcloud_output'])
    return 


def load_cfg():
    global config
    with open('./config.json','r') as f:
        config = json.load(f)
    return

def load_stop_words():
    stopwords = []
    with open(config['stop_words'], 'r') as f:
        for line in f:
            if len(line)>0:
                stopwords.append(line.strip())
    return stopwords


async def main():
    try:
        load_cfg()
        site_list = []
        for site in config['sites']:
            c = site['class']
            m = __import__('{}.{}'.format('sites', c), fromlist = (c))
            if (not m) or (not getattr(m, c)):
                continue
            p = getattr(m, c)(site['name'], site['url'])
            site_list.append(p)
        m = manager(site_list)
        await m.run()
        await m.save()
        await analyse()
    except Exception as e:
        print(e)
        traceback.print_exc()
    
if __name__ == '__main__':
    load_cfg()
    asyncio.run(main())
