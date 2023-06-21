from typing import Any

from loaders.abstract import AbstractLoader


class DummyLoader(AbstractLoader):
    def load(self, data: Any) -> None:
        pass
