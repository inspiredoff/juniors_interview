
from aiohttp import ClientSession
from lxml import html
from typing import Dict, Any


from task2.Solution.abc_parser import AbcDataParser


class ParserWiki(AbcDataParser):

    async def __init__(self, url:str):
        self.url = url


    async def fetch_page(self, session: ClientSession) -> str:
        async with session.get(self.url) as response:
            return await response.text()


    async def parse_animals(self,html_text: str) -> list[str]:
        makes_html = html.fromstring(html_text)
        animals = [elem.xpath('text()')[0] for elem in makes_html.xpath('//*[@id="mw-pages"]/div[2]/div/div/ul/li/a')]
        return animals


    async def extract_next_url(self,html_text: str) -> str:
        makes_html = html.fromstring(html_text)
        next_prefix = makes_html.xpath('//html/body/div[3]/div[3]/div[5]/div[2]/div[2]/a[2]')[0].get('href')
        return next_prefix 

    async def data_pars(self) -> Dict[str, Any]:
        async with ClientSession() as session:
            html_text = await self.fetch_page(session)
            name_animals = await self.parse_animals(html_text)
            next_prefix = await self.extract_next_url(html_text)
        return {'name_animals': name_animals, 'next_prefix':next_prefix}







