from constants.app_device import AppDevice
from data.apps import AppsData
from exceptions.base import CrawlException
from transformers.abstract import AbstractTransformer


class AppStoreAppsWebsiteTransformer(AbstractTransformer):
    @staticmethod
    def get_supported_devices(supported_device_raw_data: list[str]) -> list[str]:
        devices = set()
        for device in supported_device_raw_data:
            if device.startswith("iPhone"):
                devices.update([
                    AppDevice.IPHONE,
                    AppDevice.IPAD,
                ])
            elif device.startswith("iPad"):
                devices.update([
                    AppDevice.IPAD,
                ])
            elif device.startswith("iPod"):
                devices.update([
                    AppDevice.IPOD,
                ])
            elif device.startswith("Watch"):
                devices.update([
                    AppDevice.APPLE_WATCH,
                ])
            elif device == AppDevice.APPLE_TV:
                devices.update([
                    AppDevice.APPLE_TV,
                ])
        return list(devices)

    def transform(self, data: list[dict]) -> list[AppsData]:
        transformed_data = []
        for app in data:
            if not app.get("trackName"):
                raise CrawlException("Missing trackName")
            if not app.get("trackId"):
                raise CrawlException("Missing trackId")

            transformed_data.append(
                AppsData(
                    app_name=app["trackName"],
                    app_id=str(app["trackId"]),
                    app_url=app.get("trackViewUrl"),
                    app_targets=self.get_supported_devices(app.get("supportedDevices")),
                    artist_name=app.get("artistName"),
                    artist_id=app.get("artistId"),
                )
            )
        return transformed_data
