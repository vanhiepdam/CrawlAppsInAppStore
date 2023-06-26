import pytest

from constants.app_device import AppDevice
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
        assert set(data.app_targets) == {"iPhone", "iPad"} or data.app_targets == []

    @pytest.mark.parametrize(
        "raw_data, expected_devices",
        [
            (["iPhone5s-iPhone5s"], [AppDevice.IPHONE, AppDevice.IPAD]),
            (["iPadAir-iPadAir"], [AppDevice.IPAD]),
            (["iPodTouchSixthGen-iPodTouchSixthGen"], [AppDevice.IPOD]),
            (["Watch1,1-Watch1,1"], [AppDevice.APPLE_WATCH]),
            (["iPhone5s-iPhone5s", "iPadAir-iPadAir"], [AppDevice.IPHONE, AppDevice.IPAD]),
            (
                ["iPhone5s-iPhone5s", "iPodTouchSixthGen-iPodTouchSixthGen"],
                [AppDevice.IPHONE, AppDevice.IPAD, AppDevice.IPOD],
            ),
            (
                ["iPhone5s-iPhone5s", "Watch1,1-Watch1,1"],
                [AppDevice.IPHONE, AppDevice.IPAD, AppDevice.APPLE_WATCH],
            ),
            (
                ["iPadAir-iPadAir", "iPodTouchSixthGen-iPodTouchSixthGen"],
                [AppDevice.IPAD, AppDevice.IPOD],
            ),
            (["iPadAir-iPadAir", "Watch1,1-Watch1,1"], [AppDevice.IPAD, AppDevice.APPLE_WATCH]),
            (
                ["iPodTouchSixthGen-iPodTouchSixthGen", "Watch1,1-Watch1,1"],
                [AppDevice.IPOD, AppDevice.APPLE_WATCH],
            ),
            (
                ["iPhone5s-iPhone5s", "iPadAir-iPadAir", "iPodTouchSixthGen-iPodTouchSixthGen"],
                [AppDevice.IPHONE, AppDevice.IPAD, AppDevice.IPOD],
            ),
            (
                ["iPhone5s-iPhone5s", "iPadAir-iPadAir", "Watch1,1-Watch1,1"],
                [AppDevice.IPHONE, AppDevice.IPAD, AppDevice.APPLE_WATCH],
            ),
            (
                ["iPhone5s-iPhone5s", "iPodTouchSixthGen-iPodTouchSixthGen", "Watch1,1-Watch1,1"],
                [AppDevice.IPHONE, AppDevice.IPAD, AppDevice.IPOD, AppDevice.APPLE_WATCH],
            ),
        ],
    )
    def test_get_supported_devices(self, raw_data, expected_devices):
        # Arrange
        transformer = AppStoreAppsWebsiteTransformer()

        # Act
        devices = transformer.get_supported_devices(raw_data)

        # Assert
        assert set(devices) == set(expected_devices)
