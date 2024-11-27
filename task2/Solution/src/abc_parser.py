from abc import ABC, abstractmethod
from typing import Dict, Any


class AbcDataParser(ABC):

    @abstractmethod
    def __init__(self, url: str) -> None:
        pass

    @abstractmethod
    async def data_pars(self, url: str) -> Dict[str, Any]:
        pass
