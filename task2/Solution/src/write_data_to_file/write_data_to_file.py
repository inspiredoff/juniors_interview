import aiofiles
from typing import Dict

from task2.Solution.src.abc_write_to_file import AbcWriteToFile


class WriteDataToFile(AbcWriteToFile):

    def __init__(self, file_name: str, columns: list[str]) -> None:
        self.file_name = file_name
        self.columns = columns
        self.buffer_animal_counts = {}

    async def __write_to_file(self, animal_counts: Dict[str, int]) -> None:
        async with aiofiles.open(self.file_name, 'w') as f:
            fieldnames = self.columns
            await f.write(f'{fieldnames}\n')
            for key in animal_counts:
                await f.write(f'{key},{animal_counts[key]}\n')

    async def buffer_file_to_write(self, animal_counts: Dict[str, int]) -> None:
        if len(animal_counts.keys()) != 0:
            self.buffer_animal_counts = {key: value + animal_counts.get(key, 0)
                                         for key, value in self.buffer_animal_counts.items()}
        else:
            await self.__write_to_file(self.buffer_animal_counts)
