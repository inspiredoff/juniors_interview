import asyncio
from collections import Counter
from typing import Any

import aiofiles
from aiohttp import ClientSession
from lxml import html
import task2.config as conf

DOMAIN = conf.domain
PREFIX = conf.prefix
NAME_FILE = conf.name_file
RUSSIAN_UPPER_CHARS = conf.russian_upper_chars


async def fetch_page(session: ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        return html.fromstring(await response.text())


async def parse_animals(makes_html: Any) -> list[str]:
    animals = [elem.xpath('text()')[0] for elem in makes_html.xpath('//*[@id="mw-pages"]/div[2]/div/div/ul/li/a')]
    return list(filter(lambda animal: animal[0].upper() in RUSSIAN_UPPER_CHARS, animals))


async def extract_next_url(makes_html: str) -> str:
    next_prefix = makes_html.xpath('//html/body/div[3]/div[3]/div[5]/div[2]/div[2]/a[2]')[0].get('href')
    return next_prefix


async def count_animals(animals: list[str]) -> dict[str, int]:
    return Counter([animal[0].upper() for animal in animals if animal[0].upper() in RUSSIAN_UPPER_CHARS])


async def write_to_file(file_name: str, animal_counts: dict[str, int]) -> None:
    async with aiofiles.open(file_name, 'w') as f:
        fieldnames = ['Буква', 'Количество']
        await f.write(f'{fieldnames}\n')
        for key in animal_counts:
            await f.write(f'{key},{animal_counts[key]}\n')


async def main() -> None:
    animals_counts = {}
    url = DOMAIN + PREFIX
    async with ClientSession() as session:
        while url:
            try:
                make_html = await fetch_page(session, url)
                animals = await parse_animals(make_html)
                next_prefix = await extract_next_url(make_html)
                for key in await count_animals(animals):
                    animals_counts[key] = animals_counts.get(key, 0) + 1
                url = DOMAIN + next_prefix
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
            await write_to_file(NAME_FILE, animals_counts)


if __name__ == "__main__":
    asyncio.run(main())
