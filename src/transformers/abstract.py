from abc import ABC, abstractmethod
from typing import Any


class AbstractTransformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> Any:
        pass
