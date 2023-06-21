import logging
import sys
from dataclasses import asdict

from crawlers.apps.app_store import AppStoreAppsCrawler
from extractors.apps.app_store_website import AppStoreAppsWebsiteExtractor
from loaders.dummy import DummyLoader
from transformers.apps.app_store_website import AppStoreAppsWebsiteTransformer

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
    return [
        asdict(apps) for apps in crawler.transformed_data
    ]


if __name__ == "__main__":
    # company_name = sys.argv[1]
    data = crawl_company_apps("netflix")
    logging.info(f"Done. Found {len(data)} apps.")

    # Print details information
    group_data_by_artist_id = {}
    for app in data:
        key = (app["artist_id"], app["artist_name"])
        if key not in group_data_by_artist_id:
            group_data_by_artist_id[key] = []
        group_data_by_artist_id[key].append(app)
    for artist_id, artist_name in group_data_by_artist_id:
        logging.info(
            "Artist: {}: {} apps. Verify here: {}".format(
                artist_name,
                len(group_data_by_artist_id[(artist_id, artist_name)]),
                f"https://apps.apple.com/us/developer/{artist_id}",
            )
        )
