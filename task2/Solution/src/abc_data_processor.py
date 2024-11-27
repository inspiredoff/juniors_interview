from abc import ABC, abstractmethod
from typing import Dict


class AbcDataProcessor(ABC):

    @abstractmethod
    async def parser_data_handler(self) -> Dict[str, int]:
        pass

    @abstractmethod
    async def parser_url_handler(self) -> str:
        pass
