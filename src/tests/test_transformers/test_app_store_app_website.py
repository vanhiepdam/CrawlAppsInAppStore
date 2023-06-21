import pytest

from transformers.apps.app_store_website import AppStoreAppsWebsiteTransformer


class TestAppStoreAppsWebsiteTransformer:
    @pytest.mark.parametrize(
        "raw_data",
        [
            [
                {
                    "trackName": "",
                    "trackId": "363590054",
                    "trackViewUrl": "https://apps.apple.com/us/app/netflix/id363590054?uo=4",
                    "supportedDevices": ["iPhone5s-iPhone5s", "iPadAir-iPadAir"],
                }
            ],
            [
                {
                    "trackName": "Netflix",
                    "trackId": "",
                    "trackViewUrl": "https://apps.apple.com/us/app/netflix/id363590054?uo=4",
                    "supportedDevices": ["iPhone5s-iPhone5s", "iPadAir-iPadAir"],
                }
            ],
        ],
    )
    def test_transform__raw_data_missing_data(self, raw_data):
        # Arrange
        transformer = AppStoreAppsWebsiteTransformer()

        # Act
        with pytest.raises(ValueError) as ex:
            transformer.transform(raw_data)

        # Assert
        assert str(ex.value) == "Missing trackName" or str(ex.value) == "Missing trackId"

    @pytest.mark.parametrize(
        "raw_data",
        [
            [
                {
                    "trackName": "Netflix",
                    "trackId": "363590054",
                    "trackViewUrl": "https://apps.apple.com/us/app/netflix/id363590054?uo=4",
                    "supportedDevices": ["iPhone5s-iPhone5s", "iPadAir-iPadAir"],
                }
            ],
            [
                {
                    "trackName": "Netflix",
                    "trackId": "363590054",
                    "trackViewUrl": "",
                    "supportedDevices": [],
                }
            ],
        ],
    )
    def test_transform__raw_data_correct(self, raw_data):
        # Arrange
        transformer = AppStoreAppsWebsiteTransformer()

        # Act
        data = transformer.transform(raw_data)

        # Assert
        assert len(data) == 1
        data = data[0]
        assert data.app_name == "Netflix"
        assert data.app_id == "363590054"
        assert (
            data.app_url == "https://apps.apple.com/us/app/netflix/id363590054?uo=4"
            or data.app_url == ""
        )
        assert (
            data.app_targets == ["iPhone5s-iPhone5s", "iPadAir-iPadAir"] or data.app_targets == []
        )
