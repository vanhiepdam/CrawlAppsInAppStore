from src.crawlers.apps.itune_lookup import ITunesAppsLookupCrawler
from src.extractors.apps.itunes_lookup import ITunesAppsExtractor
from src.loaders.dummy import DummyLoader
from src.transformers.apps.itune_lookup import ITunesAppsTransformer
import sys


def crawl_company_apps(company_name: str):
    crawler = ITunesAppsLookupCrawler(
        extractor=ITunesAppsExtractor(),
        transformer=ITunesAppsTransformer(),
        loader=DummyLoader(),
    )
    crawler.set_url_to_crawl_app_by_company_name(company_name)
    crawler.crawl()
    return crawler.transformed_data


if __name__ == "__main__":
    # args = sys.argv[1]
    crawl_company_apps("netflix")
