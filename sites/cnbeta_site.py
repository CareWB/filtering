import asyncio
from sites.base_site import base_site
import aiohttp
import json
from news import news

class cnbeta_site(base_site):
    async def get(self) -> list:
        news_list = []
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                html = await response.text()
                data = json.loads(html)
                for sub in data['data']['site']['subs']:
                    for item in sub['items']:
                        news_list.append(news(item['title'], 'https://www.anyknew.com/go/'+str(item['iid']), item['add_date']))
        return news_list