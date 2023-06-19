from abc import ABC, abstractmethod
from typing import Any


class AbstractExtractor(ABC):
    def __init__(self, context: dict = None):
        self.context = context or {}

    @abstractmethod
    def extract(self, url: str) -> Any:
        pass

    def update_context(self, **kwargs) -> None:
        self.context.update(kwargs)
