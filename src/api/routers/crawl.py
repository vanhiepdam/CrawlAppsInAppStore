from fastapi import APIRouter

from api.serializers.crawl import CrawlRequestSerializer, CrawlResponseSerializer
from api.services.crawl import CrawlAppsService

router = APIRouter()


@router.post("/api/v1/crawl")
async def crawl(request: CrawlRequestSerializer) -> list[CrawlResponseSerializer]:
    data = CrawlAppsService.crawl_app_store_apps_by_company_name(request.company_name)
    return [
        CrawlResponseSerializer(
            app_name=item.app_name,
            app_id=item.app_id,
            app_url=item.app_url,
            app_targets=item.app_targets,
        )
        for item in data
    ]
