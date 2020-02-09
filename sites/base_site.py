import asyncio
from news import news

class base_site:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.news = []

    async def get(self) -> list:
        pass

    async def run(self):
        self.news = await self.get()

    async def save(self):
        result = {'name':self.name,'news':[]}
        for n in self.news:
            result['news'].append(n.__dict__)
        return result