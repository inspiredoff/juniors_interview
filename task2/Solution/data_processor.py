from typing import Any, Dict

from task2.solution import count_animals


class AnimalDataProcessor:

    async def __init__(self, russian_upper_chars:str, pars_data:Dict[str, Any], domain) -> None:
        self.russian_upper_chars = russian_upper_chars
        self.name_animals = pars_data['name_animals']
        self.next_url =domain + pars_data['next_prefix']
        self.name_animal_count = {}


    async def count_animals(self, animals: list[str]) -> Dict[str, int]:
        for animal in animals:
            if animal[0].upper() in self.russian_upper_chars:
                self.name_animal_count[animal[0].upper()] = self.name_animal_count.get(animal[0].upper(), 0) + 1
        return self.name_animal_count

    async def parser_data_handler(self) -> Dict[str, int]|None:
        await self.count_animals(self.name_animals)
        if self.name_animal_count != 0:
            return self.name_animal_count
        else:
            return None


    async def parser_url_handler(self) -> str|None:
        if self.name_animal_count.keys() !=0:
            return self.next_url
        else:
            return None
