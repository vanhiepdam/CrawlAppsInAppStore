from typing import Any

from src.loaders.abstract import AbstractLoader


class DummyLoader(AbstractLoader):
    def load(self, data: Any) -> None:
        pass
