from crawlers.base import GenericCrawler


class AppStoreAppsCrawler(GenericCrawler):
    def __init__(self, extractor, transformer, loader):
        super().__init__(extractor, transformer, loader)
        self.url = "https://itunes.apple.com/search?media=software&entity=software"

    def set_url_to_crawl_app_by_company_name(self, company_name: str):
        self.extractor.update_context(company_name=company_name)
        self.transformer.update_context(company_name=company_name)
        self.loader.update_context(company_name=company_name)
