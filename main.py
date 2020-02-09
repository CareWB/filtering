import asyncio
import traceback
import json

from aiofile import AIOFile, Writer

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

        async with AIOFile("./result.json", 'w') as afp:
            writer = Writer(afp)
            await writer(json.dumps(data, ensure_ascii=False))
            await afp.fsync()

def load_cfg():
    config = None
    with open('./config.json','r') as f:
        config = json.load(f)
    return config

async def main():
    try:
        config = load_cfg()
        site_list = []
        for site in config['sites']:
            c = site['class']
            m = __import__('{}.{}'.format('sites', c), fromlist = (c))
            if (not m) or (not getattr(m, c)):
                continue
            a = getattr(m, c)
            p = a(site['name'], site['url'])
            site_list.append(p)
        m = manager(site_list)
        await m.run()
        await m.save()
    except Exception as e:
        print(e)
        traceback.print_exc()
    
if __name__ == '__main__':
    asyncio.run(main())
