from abc import ABC, abstractmethod
from typing import Dict


class AbcWriteToFile(ABC):

    @abstractmethod
    async def buffer_file_to_write(self, data: Dict[str, int]) -> None:
        pass
