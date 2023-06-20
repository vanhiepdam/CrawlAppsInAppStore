from typing import Any

from src.transformers.abstract import AbstractTransformer


class AppStoreAppsWebsiteTransformer(AbstractTransformer):
    def __init__(self, context: dict = None):
        self.context = context or {}

    def transform(self, data: Any) -> dict:
        pass
