import logging

from crawlers.apps.app_store import AppStoreAppsCrawler
from data.apps import AppsData
from extractors.apps.app_store_website import AppStoreAppsWebsiteExtractor
from loaders.dummy import DummyLoader
from transformers.apps.app_store_website import AppStoreAppsWebsiteTransformer


class CrawlAppsService:
    @staticmethod
    def crawl_app_store_apps_by_company_name(company_name: str) -> list[AppsData]:
        logging.info(f"Crawling apps from company: {company_name}")
        crawler = AppStoreAppsCrawler(
            extractor=AppStoreAppsWebsiteExtractor(),
            transformer=AppStoreAppsWebsiteTransformer(),
            loader=DummyLoader(),
        )
        company_name = company_name.strip()
        crawler.set_url_to_crawl_app_by_company_name(company_name)
        crawler.crawl()
        return crawler.transformed_data
