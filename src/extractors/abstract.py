from abc import ABC, abstractmethod
from typing import Any


class AbstractExtractor(ABC):
    @abstractmethod
    def extract(self, url: str) -> Any:
        pass
