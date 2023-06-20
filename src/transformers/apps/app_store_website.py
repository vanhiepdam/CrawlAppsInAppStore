from src.data.apps import AppsData
from src.transformers.abstract import AbstractTransformer


class AppStoreAppsWebsiteTransformer(AbstractTransformer):
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
                    app_id=app["trackId"],
                    app_url=app.get("trackViewUrl"),
                    app_targets=app.get("supportedDevices"),
                    artist_name=app.get("artistName"),
                    artist_id=app.get("artistId"),
                )
            )
        return transformed_data
