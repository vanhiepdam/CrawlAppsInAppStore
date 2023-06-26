from dataclasses import dataclass

from pydantic import BaseModel


@dataclass(frozen=True)
class AppsData(BaseModel):
    app_name: str
    app_id: str
    app_url: str | None
    app_targets: list[str]
    artist_name: str
    artist_id: str
