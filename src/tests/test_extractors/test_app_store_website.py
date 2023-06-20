import os
from unittest import mock

import pytest

from src.extractors.apps.app_store_website import AppStoreAppsWebsiteExtractor
from src.tests.test_extractors.data.app_store.apps_info import app_info_sample


def _get_website_content_from_url_side_effect(self, driver, url):
    current_folder_of_this_file = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder_of_this_file, "data/app_store/developer_homepage.html")
    driver.get(f"file://{file_path}")


class TestAppStoreWebsiteExtractor:
    @mock.patch(
        "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_developers_data_from_website",
    )
    def test_extract__no_developer(self, _get_developers_data_from_website):
        # Arrange
        url = "https://apps.apple.com/us/developer/netflix-inc/id363590051"
        extractor = AppStoreAppsWebsiteExtractor(context={"company_name": "netflix"})
        _get_developers_data_from_website.return_value = {
            "resultCount": 0,
            "results": [],
        }

        # Act
        result = extractor.extract(url)

        # Assert
        assert result == []

    @mock.patch(
        "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_developers_data_from_website",
    )
    def test_extract__too_many_developer(self, _get_developers_data_from_website):
        # Arrange
        url = "https://apps.apple.com/us/developer/netflix-inc/id363590051"
        extractor = AppStoreAppsWebsiteExtractor(
            context={"company_name": "netflix"}, limit_developer_match=1
        )
        _get_developers_data_from_website.return_value = {
            "resultCount": 2,
            "results": [],
        }

        # Act
        with pytest.raises(ValueError) as ex:
            extractor.extract(url)

        # Assert
        assert str(ex.value) == "Too many results. Please search for more specific name."

    @mock.patch(
        "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_developers_data_from_website",
    )
    def test__get_developers_by_search_name(self, _get_developers_data_from_website):
        # Arrange
        extractor = AppStoreAppsWebsiteExtractor(context={"company_name": "netflix"})
        _get_developers_data_from_website.return_value = {
            "resultCount": 2,
            "results": [
                {
                    "wrapperType": "artist",
                    "artistType": "Software Artist",
                    "artistName": "Netflix, Inc.",
                    "artistLinkUrl": "",
                    "artistId": 363590054,
                },
                {
                    "wrapperType": "artist",
                    "artistType": "Software Artist",
                    "artistName": "Netflix +",
                    "artistLinkUrl": "",
                    "artistId": 1691287718,
                },
                {
                    "wrapperType": "artist",
                    "artistType": "Software Artist",
                    "artistName": "Netflix +++",
                    "artistLinkUrl": "",
                    "artistId": 1691287718,
                },
            ],
        }

        # Act
        result = extractor._get_developers_by_search_name()

        # Assert
        assert result == {
            363590054: "Netflix, Inc.",
            1691287718: "Netflix +++",
        }

    def test_extract__from_developer_has_both_deep_link_and_apps_in_home_page__match_2_developers(
        self,
        mocker,
    ):
        # Arrange
        url = "https://itunes.apple.com/search/netflix-inc/id363590051"
        extractor = AppStoreAppsWebsiteExtractor(context={"company_name": "netflix"})

        # Mock data
        mocker.patch(
            "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_developers_data_from_website",
            return_value={
                "resultCount": 2,
                "results": [
                    {
                        "wrapperType": "artist",
                        "artistType": "Software Artist",
                        "artistName": "Netflix, Inc.",
                        "artistLinkUrl": "",
                        "artistId": 363590054,
                    },
                    {
                        "wrapperType": "artist",
                        "artistType": "Software Artist",
                        "artistName": "Netflix +",
                        "artistLinkUrl": "",
                        "artistId": 1691287718,
                    },
                ],
            },
        )
        mocker.patch(
            "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._look_up_app_info_from_app_ids",
            return_value=app_info_sample["results"],
        )
        mocker.patch(
            "src.extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_website_content_from_url",
            _get_website_content_from_url_side_effect,
        )

        # Act
        result = extractor.extract(url)

        # Assert
        assert result == app_info_sample["results"] * 2
