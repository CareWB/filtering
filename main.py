import asyncio
import traceback

class manager:
    def __init__(self, sites = []):
        self.sites = sites

    async def run(self):
        for site in self.sites:
            await site.run()
            await site.save()

async def main():
    try:
        sites = {'weibo': ('weibo_site', 'https://www.anyknew.com/api/v1/sites/weibo'),\
                 'zhihu': ('zhihu_site', 'https://www.anyknew.com/api/v1/sites/zhihu')}
        site_list = []
        for k,v in sites.items():
            m = __import__('{}.{}'.format('sites', v[0]), fromlist = (v[0]))
            if (not m) or (not getattr(m, v[0])):
                continue
            a = getattr(m, v[0])
            p = a(k,v[1])
            site_list.append(p)
        m = manager(site_list)
        await m.run()
    except Exception as e:
        print(e)
        traceback.print_exc()
    
if __name__ == '__main__':
    asyncio.run(main())
