from abc import ABC, abstractmethod
from typing import Any


class AbstractLoader(ABC):
    def __init__(self, context: dict = None):
        self.context = context or {}

    @abstractmethod
    def load(self, data: Any) -> Any:
        pass

    def update_context(self, **kwargs) -> None:
        self.context.update(kwargs)
