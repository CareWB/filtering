import asyncio
from sites.base_site import base_site
import aiohttp
import json
from news import news
import time

class aicamp_site(base_site):
    async def get(self) -> list:
        news_list = []
        headers = {'Host':'www.waijiedanao.com'}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=headers) as response:
                html = await response.text()
                data = json.loads(html)
                for item in data['data']:
                    t = time.mktime(time.strptime(item['publishAt'], "%Y-%m-%dT%H:%M:%S.000Z"))
                    news_list.append(news(item['title'], item['link'], str(int(t))))
        return news_list