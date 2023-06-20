from abc import ABC, abstractmethod
from typing import Any


class AbstractTransformer(ABC):
    def __init__(self, context: dict = None):
        self.context = context or {}

    @abstractmethod
    def transform(self, data: Any) -> Any:
        pass

    def update_context(self, **kwargs) -> None:
        self.context.update(kwargs)
