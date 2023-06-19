from abc import ABC

from src.extractors.abstract import AbstractExtractor
from src.loaders.abstract import AbstractLoader
from src.transformers.abstract import AbstractTransformer


class GenericCrawler(ABC):
    def __init__(
        self,
        extractor: AbstractExtractor,
        transformer: AbstractTransformer,
        loader: AbstractLoader,
    ):
        self.url = None
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
        self.extracted_data = None
        self.transformed_data = None

    def set_url(self, url: str):
        self.url = url

    def set_extractor(self, extractor: AbstractExtractor):
        self.extractor = extractor

    def set_transformer(self, transformer: AbstractTransformer):
        self.transformer = transformer

    def set_loader(self, loader: AbstractLoader):
        self.loader = loader

    def crawl(self):
        if self.url is None:
            raise ValueError("URL is not set")
        self.extracted_data = self.extractor.extract(self.url)
        self.transformed_data = self.transformer.transform(self.extracted_data)
        self.loader.load(self.transformed_data)
