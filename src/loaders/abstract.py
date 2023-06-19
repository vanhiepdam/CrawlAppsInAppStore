from abc import ABC, abstractmethod
from typing import Any


class AbstractLoader(ABC):
    @abstractmethod
    def load(self, data: Any) -> Any:
        pass
