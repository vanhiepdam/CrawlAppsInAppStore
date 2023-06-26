from constants.app_device import AppDevice
from data.apps import AppsData
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
        return list(devices)

    def transform(self, data: list[dict]) -> list[AppsData]:
        transformed_data = []
        for app in data:
            if not app.get("trackName"):
                raise ValueError("Missing trackName")
            if not app.get("trackId"):
                raise ValueError("Missing trackId")

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
