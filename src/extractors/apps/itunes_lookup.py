import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.extractors.abstract import AbstractExtractor


class ITunesAppsExtractor(AbstractExtractor):
    def _get_developer_id_from_original_url(self, url: str) -> str | None:
        url += "&limit=5" if not url.endswith("&") else "limit=5"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["resultCount"] == 0:
            developer_id = None
        else:
            item = [
                item
                for item in data["results"]
                if item["kind"] == "software"
                and self.context["company_name"].lower() in item["artistName"].lower()
            ]
            if len(item) == 0:
                developer_id = None
            else:
                developer_id = item[0]["artistId"]

        return developer_id

    def get_all_apps_from_developer(self, developer_id: str) -> list[dict]:
        url = f"https://apps.apple.com/us/developer/{developer_id}"
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=option
        )
        driver.get(url)
        apps_ids = self._find_apps_by_sections(driver)
        return apps_ids

    def _get_apps_from_see_all_url(self, driver: WebDriver, see_all_url: str) -> list[str]:
        pass

    def _find_apps_by_sections(self, driver: WebDriver) -> set[str]:
        app_ids = set()
        sections = driver.find_elements(
            by=By.XPATH, value="//main//section[@class='l-content-width section section--bordered']"
        )
        for section in sections:
            # find in section has a tag a with class section__nav__see-all-link
            see_all_link = section.find_elements(
                by=By.XPATH, value=".//a[@class='section__nav__see-all-link']"
            )
            if len(see_all_link) > 0:
                self._get_apps_from_see_all_url(driver, see_all_link[0].get_attribute("href"))
            else:
                # find all a tags inside a div with class "l-row l-row--peek" and
                # get href from those a tags
                peek_row = section.find_elements(
                    by=By.XPATH, value=".//div[@class='l-row l-row--peek']"
                )
                if len(peek_row) > 0:
                    a_tags = peek_row[0].find_elements(by=By.XPATH, value=".//a")
                    app_ids.update([a_tag.get_attribute("href").split("/")[-1] for a_tag in a_tags])
        return app_ids

    def extract(self, url: str) -> list[dict]:
        developer_id = self._get_developer_id_from_original_url(url)
        if developer_id is None:
            return []

        return self.get_all_apps_from_developer(developer_id)
