import os

import pytest

from main import crawl_company_apps
from tests.data.app_store.apps_info import app_info_sample


class TestCrawlAppsInAppStore:
    def test_success__crawl_by_company_name__without_network(self, mocker):
        # Mock data
        mocker.patch(
            "extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_developers_data_from_website",
            return_value={
                "resultCount": 1,
                "results": [
                    {
                        "wrapperType": "artist",
                        "artistType": "Software Artist",
                        "artistName": "Netflix, Inc.",
                        "artistLinkUrl": "",
                        "artistId": 363590054,
                    },
                ],
            },
        )
        mocker.patch(
            "extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._look_up_app_info_from_app_ids",
            return_value=app_info_sample["results"],
        )

        def _get_website_content_from_url_side_effect(self, driver, url):
            current_folder_of_this_file = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                os.path.dirname(current_folder_of_this_file),
                "data/app_store/developer_homepage.html",
            )
            driver.get(f"file://{file_path}")

        mocker.patch(
            "extractors.apps.app_store_website.AppStoreAppsWebsiteExtractor._get_website_content_from_url",
            _get_website_content_from_url_side_effect,
        )

        # Act
        apps_info = crawl_company_apps("netflix, inc.")

        # Assert
        assert len(apps_info) == len(app_info_sample["results"])

        # Assert 1st app
        sample_netflix_app = app_info_sample["results"][0]
        netflix_app_result = [
            item for item in apps_info if item["app_id"] == sample_netflix_app["trackId"]
        ]
        assert len(netflix_app_result) == 1
        assert netflix_app_result[0]["app_name"] == sample_netflix_app["trackName"]
        assert netflix_app_result[0]["app_url"] == sample_netflix_app["trackViewUrl"]
        assert netflix_app_result[0]["app_targets"] == sample_netflix_app["supportedDevices"]
        assert netflix_app_result[0]["artist_name"] == sample_netflix_app["artistName"]
        assert netflix_app_result[0]["artist_id"] == sample_netflix_app["artistId"]

        # Assert 2nd app
        sample_too_hot_to_handle_app = app_info_sample["results"][1]
        too_hot_to_handle_app_result = [
            item for item in apps_info if item["app_id"] == sample_too_hot_to_handle_app["trackId"]
        ]
        assert len(too_hot_to_handle_app_result) == 1
        assert (
            too_hot_to_handle_app_result[0]["app_name"] == sample_too_hot_to_handle_app["trackName"]
        )
        assert (
            too_hot_to_handle_app_result[0]["app_url"]
            == sample_too_hot_to_handle_app["trackViewUrl"]
        )
        assert (
            too_hot_to_handle_app_result[0]["app_targets"]
            == sample_too_hot_to_handle_app["supportedDevices"]
        )
        assert (
            too_hot_to_handle_app_result[0]["artist_name"]
            == sample_too_hot_to_handle_app["artistName"]
        )
        assert (
            too_hot_to_handle_app_result[0]["artist_id"] == sample_too_hot_to_handle_app["artistId"]
        )

    @pytest.mark.integration
    def test_success__crawl_by_company_name__with_network(self):
        # Act
        apps_info = crawl_company_apps("netflix, inc.")

        # Assert
        assert len(apps_info) > 60

        # Assert netflix app in the result
        netflix_app_result = [item for item in apps_info if item["app_id"] == 363590051]
        assert len(netflix_app_result) == 1
        assert netflix_app_result[0]["app_name"] is not None
        assert netflix_app_result[0]["app_name"] != ""
        assert netflix_app_result[0]["app_url"] is not None
        assert netflix_app_result[0]["app_url"] != ""
        assert len(netflix_app_result[0]["app_targets"]) > 0
        assert netflix_app_result[0]["artist_name"] is not None
        assert netflix_app_result[0]["artist_name"] != ""
        assert netflix_app_result[0]["artist_id"] == 363590054
