from src.crawlers.base import GenericCrawler


class ITunesAppsLookupCrawler(GenericCrawler):
    def __init__(self, extractor, transformer, loader):
        super().__init__(extractor, transformer, loader)
        self.url = "https://itunes.apple.com/search?media=software&entity=software"

    def set_url_to_crawl_app_by_company_name(self, company_name: str):
        self.url += f"&attribute=softwareDeveloper&term={company_name}"
