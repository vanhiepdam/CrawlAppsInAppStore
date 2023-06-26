from pydantic import BaseModel


class CrawlRequestSerializer(BaseModel):
    company_name: str


class CrawlResponseSerializer(BaseModel):
    app_name: str
    app_id: str
    app_url: str | None
    app_targets: list[str]
