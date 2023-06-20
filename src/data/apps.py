from dataclasses import dataclass


@dataclass(frozen=True)
class AppsData:
    app_name: str
    app_id: str
    app_url: str | None
    app_targets: list[str]
    artist_name: str
    artist_id: str
