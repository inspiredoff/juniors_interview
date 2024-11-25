import asyncio
import aiofiles
from aiohttp import ClientSession
from lxml import html
import config as conf

DOMAIN = conf.domain
PREFIX = conf.prefix
NAME_FILE = conf.name_file
RUSSIAN_UPPER_CHARS = conf.russian_upper_chars


async def fetch_page(session: ClientSession(), url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


async def parse_animals(html_text: str) -> list[str]:
    makes_html = html.fromstring(html_text)
    animals = [elem.xpath('text()')[0] for elem in makes_html.xpath('//*[@id="mw-pages"]/div[2]/div/div/ul/li/a')]
    return animals


async def extract_next_url(html_text: str) -> str:
    makes_html = html.fromstring(html_text)
    next_url = makes_html.xpath('//html/body/div[3]/div[3]/div[5]/div[2]/div[2]/a[2]')[0].get('href')
    return next_url


async def count_animals(animals: list[str]) -> dict[str, int]:
    animals_counts = {}
    for animal in animals:
        if animal[0].upper() in RUSSIAN_UPPER_CHARS:
            animals_counts[animal[0].upper()] = animals_counts.get(animal[0].upper(), 0) + 1
    return animals_counts


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
                html_text = await fetch_page(session, url)
                animals = await parse_animals(html_text)
                next_url = await extract_next_url(html_text)

                new_counts = await count_animals(animals)
                for letter, count in new_counts.items():
                    animals_counts[letter] = animals_counts.get(letter, 0) + count

                url = DOMAIN + next_url if next_url else None
            except Exception as e:
                print(f"Произошла ошибка: {e}")
                break
            await write_to_file(NAME_FILE, animals_counts)


if __name__ == "__main__":
    asyncio.run(main())
