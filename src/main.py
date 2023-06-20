import logging
import sys

from src.crawlers.apps.app_store import AppStoreAppsCrawler
from src.extractors.apps.app_store_website import AppStoreAppsWebsiteExtractor
from src.loaders.dummy import DummyLoader
from src.transformers.apps.app_store_website import AppStoreAppsWebsiteTransformer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def crawl_company_apps(company_name: str):
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


if __name__ == "__main__":
    # args = sys.argv[1]
    crawl_company_apps("netflix")
