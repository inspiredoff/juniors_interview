from abc import ABC, abstractmethod
from typing import Dict, Any

class AbcDataParser(ABC):
    @abstractmethod
    async def data_pars(self) -> Dict[str, Any]:
        pass
