import asyncio
import aiofiles
from aiohttp import ClientSession
from lxml import html
import confid as conf

DOMAIN = conf.domain
PREFIX = conf.prefix
NAME_FILE = conf.name_file
RUSSIAN_UPPER_CHARS = conf.russian_upper_chars


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_animals(html_text):
    makes_html = html.fromstring(html_text)
    animals = [elem.xpath('text()')[0] for elem in makes_html.xpath('//*[@id="mw-pages"]/div[2]/div/div/ul/li/a')]
    return animals


async def extract_next_url(html_text):
    makes_html = html.fromstring(html_text)
    next_url = makes_html.xpath('//html/body/div[3]/div[3]/div[5]/div[2]/div[2]/a[2]')[0].get('href')
    return next_url


async def count_animals(animals):
    animals_counts = {}
    for animal in animals:
        if animal[0].upper() in RUSSIAN_UPPER_CHARS:
            animals_counts[animal[0].upper()] = animals_counts.get(animal[0].upper(), 0) + 1
    return animals_counts


async def write_to_file(file_name, animal_counts):
    async with aiofiles.open(file_name, 'w') as f:
        fieldnames = ['Буква', 'Количество']
        await f.write(f'{fieldnames}\n')
        for key in animal_counts:
            await f.write(f'{key},{animal_counts[key]}\n')


async def main():
    animals_counts = {}
    url = DOMAIN + PREFIX
    while url:
        async with ClientSession() as session:
            html_text = await fetch_page(session, url)
            animals = await parse_animals(html_text)
            next_url = await extract_next_url(html_text)
            new_counts = await count_animals(animals)
            animals_counts.update(new_counts)
        url = DOMAIN + next_url if next_url else None
        await write_to_file(NAME_FILE, animals_counts)


if __name__ == "__main__":
    asyncio.run(main())
