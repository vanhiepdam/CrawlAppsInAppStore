import logging

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from constants.app_device import AppDevice
from exceptions.base import CrawlException
from extractors.abstract import AbstractExtractor
from utils.list import ListUtil
from utils.matcher import MatcherUtil
from utils.selenium import SeleniumUtil


class AppStoreAppsWebsiteExtractor(AbstractExtractor):
    def __init__(
        self, context: dict = None, limit_per_request: int = 200, limit_developer_match: int = 5
    ):
        super().__init__(context)
        self.limit_per_request = limit_per_request
        self.limit_developer_match = limit_developer_match
        self.apple_tv_apps = set()

    def _get_developers_data_from_website(self) -> dict:
        url = "https://itunes.apple.com/search?media=software&entity=allArtist&attribute=softwareDeveloper&term={}&limit={}".format(
            self.context["company_name"],
            self.limit_per_request,
        )
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data

    def _get_developers_by_search_name(self) -> dict[str, str]:
        data = self._get_developers_data_from_website()
        if data["resultCount"] > self.limit_developer_match:
            raise CrawlException(
                "Too many companies in the search results. Please search for more specific name."
            )

        developers = {
            item["artistId"]: item["artistName"]
            for item in data["results"]
            if MatcherUtil.is_company_name_match_developer_name(
                self.context["company_name"], item["artistName"]
            )
        }

        return developers

    def _get_apps_from_see_all_url(self, see_all_url: str) -> list[str]:
        logging.info(f"Getting apps from see all url: {see_all_url}")
        # get page
        driver = self._get_new_driver_with_url(see_all_url)
        SeleniumUtil.scroll_to_bottom_infinite(driver)

        # find apps
        apps = driver.find_elements(by=By.XPATH, value="//div[@role='feed']/a[@role='article']")
        apps_ids = [app.get_attribute("href").split("/")[-1] for app in apps]
        return apps_ids

    def _clean_app_ids(self, app_ids: set[str]) -> list[str]:
        return list(set(map(lambda app_id: app_id.replace("id", ""), app_ids)))

    def _find_apps_by_sections(self, url) -> list[str]:
        # get page
        app_ids = set()
        driver = self._get_new_driver_with_url(url)
        SeleniumUtil.scroll_to_bottom_infinite(driver)

        # find apps in sections
        sections = driver.find_elements(
            by=By.XPATH, value="//main//section[@class='l-content-width section section--bordered']"
        )
        for section in sections:
            # find in section has a tag a with class section__nav__see-all-link
            see_all_link = section.find_elements(
                by=By.XPATH, value=".//a[@class='ember-view link section__nav__see-all-link']"
            )
            if len(see_all_link) > 0:
                sub_app_ids = self._get_apps_from_see_all_url(see_all_link[0].get_attribute("href"))
            else:
                # find all a tags inside a div with class "l-row l-row--peek" and
                # get href from those a tags
                logging.info(f"Finding apps from section in home page")
                peek_row = section.find_elements(
                    by=By.XPATH, value=".//div[@class='l-row l-row--peek']"
                )
                if len(peek_row) > 0:
                    a_tags = peek_row[0].find_elements(by=By.XPATH, value=".//a")
                    sub_app_ids = {a_tag.get_attribute("href").split("/")[-1] for a_tag in a_tags}
                else:
                    sub_app_ids = set()
            app_ids.update(sub_app_ids)

            # Update apple tv apps.
            # Because there is no apple tv supported devices in itunes api
            section_title = section.find_element(
                by=By.XPATH, value=".//h2[@class='section__headline']"
            ).accessible_name
            if section_title == "Apple TV":
                self.apple_tv_apps.update(sub_app_ids)
        return self._clean_app_ids(app_ids)

    def _look_up_app_info_from_app_ids(self, app_ids: list[str]) -> list[dict]:
        url = f"https://itunes.apple.com/lookup?id={','.join(app_ids)}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        raw_data = data["results"]

        # add apple tv to supported devices if it is in apple tv apps
        for app in raw_data:
            if (str(app["trackId"]) in self._clean_app_ids(self.apple_tv_apps)) or (
                app["trackId"] in self._clean_app_ids(self.apple_tv_apps)
            ):
                app["supportedDevices"].append(AppDevice.APPLE_TV)
        return raw_data

    def _get_apps_info_from_app_ids(self, app_ids: list[str]) -> list[dict]:
        id_chunks = ListUtil.split_array_into_chunks(app_ids, self.limit_per_request)
        apps_info = []
        for id_chunk in id_chunks:
            data = self._look_up_app_info_from_app_ids(id_chunk)
            apps_info.extend(data)
        return apps_info

    @staticmethod
    def _get_website_content_from_url(driver, url) -> None:
        driver.get(url)

    def _get_new_driver_with_url(self, url: str, **kwargs) -> WebDriver:
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=option, **kwargs
        )
        self._get_website_content_from_url(driver, url)
        return driver

    def get_all_apps_from_developer(self, developer_id: str) -> list[dict]:
        url = f"https://apps.apple.com/us/developer/{developer_id}"
        apps_ids = self._find_apps_by_sections(url)
        apps_info = self._get_apps_info_from_app_ids(apps_ids)
        return apps_info

    def extract(self, url: str) -> list[dict]:
        logging.info("Extracting apps from iTunes")
        developers = self._get_developers_by_search_name()
        data = []
        for developer_id, developer_name in developers.items():
            logging.info(f"Extracting apps from developer {developer_name}, ID: {developer_id}")
            developer_data = self.get_all_apps_from_developer(developer_id)
            logging.info(f"Extracted {len(data)} apps from developer {developer_name}")
            data.extend(developer_data)
        return data
