import asyncio
from sites.base_site import base_site
import aiohttp
import json
from news import news

class xueqiu_site(base_site):
    async def get(self) -> list:
        news_list = []
        headers = {'Host':'xueqiu.com', \
                  'Cookie':'''aliyungf_tc=AQAAAADHAEQIbAkAGB/leEYqmJMFj6sK; \acw_tc=2760820115812286396373548e0cc9490debcfce9235a39325d675bf12c4af; xq_a_token=b2f87b997a1558e1023f18af36cab23af8d202ea; xqat=b2f87b997a1558e1023f18af36cab23af8d202ea; xq_r_token=823123c3118be244b35589176a5974c844687d5e; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU4MzE0MzIwMCwiY3RtIjoxNTgxMjI4NjE2MTkwLCJjaWQiOiJkOWQwbjRBWnVwIn0.edS-Tn9iT2huNVKhiiu-tz0ocnfHb5X1hvfLQW-i2IV5REkYPBESMY6k8zAm-ZCX-UFn68XF7cbfXUGm8hpu5_ibafFBvZiB1jgICo6XR36TF3TmISryxcGnCeDVIakU3gfbQ_hgN-blF7tymooSv5yKXp6Veu66cfE05z7rIrp326THxnqTK6dnph4NVDH6fyzFz8wBQtPr4IFGGT7iWKEmhMLndzDTUkGTeKdmt7IJD58QWuxR8T_Q_qlNR2C-elDxpp_Wu8AaWWwZqPg9uEKUTFc3a3bkMll4m9wpVGjyZcUUNSrG3gpamELJvIXhLOnSFEjL9yQpBy4F3HHrlA; u=111581228639641; device_id=573ca601344af6a914f4ab83171b34cf; Hm_lvt_1db88642e346389874251b5a1eded6e3=1581228642,1581228676,1581228681,1581228686; OUTFOX_SEARCH_USER_ID_NCOO=2109077540.7053394; s=bw125pf1dv; ___rl__test__cookies=1581228968413; __utma=1.1497135620.1581229261.1581229261.1581229261.1; __utmc=1; __utmz=1.1581229261.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); cookiesu=111581230815523; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1581230816''',\
                  'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=headers) as response:
                html = await response.text()
                data = json.loads(html)
                for item in data['list']:
                    item = json.loads(item['data'])
                    if not item['title']:
                        continue
                    news_list.append(news(item['title'], \
                                          'https://xueqiu.com'+str(item['target']), \
                                          item['created_at']/1000))
        return news_list