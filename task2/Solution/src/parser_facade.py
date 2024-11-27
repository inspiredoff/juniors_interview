from typing import Dict, Any

from task2.Solution.src.abc_data_processor import AbcDataProcessor
from task2.Solution.src.abc_parser import AbcDataParser
from task2.Solution.src.abc_write_to_file import AbcWriteToFile
from task2.Solution.src.data_processor.data_processor import AnimalDataProcessor
from task2.Solution.src.parser.parser_wiki import ParserWiki
from task2.Solution.src.write_data_to_file.write_data_to_file import WriteDataToFile
from task2.Solution.src.config import russian_upper_chars, domain, prefix


class ParserFacade:

    def __init__(self, parser: AbcDataParser,
                 data_processor: AbcDataProcessor,
                 write_to_file: AbcWriteToFile) -> None:
        self.url = domain+prefix
        self.write_to_file = WriteDataToFile('beasts.csv', ['Буква', 'Количество'])
        self.parser = parser
        self.data_processor = data_processor
        self.write_to_file = write_to_file

    async def data_pars(self) -> None:
        flag = True
        while flag:
            pars_data = await self.parser.data_pars(self.url)
            self.url = await self.data_processor.parser_url_handler()
            animal_count = await self.data_processor.parser_data_handler()

