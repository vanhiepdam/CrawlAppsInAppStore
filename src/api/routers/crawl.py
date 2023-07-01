from fastapi import APIRouter, HTTPException

from api.serializers.crawl import CrawlRequestSerializer, CrawlResponseSerializer
from api.services.crawl import CrawlAppsService
from exceptions.base import CrawlException

router = APIRouter()


@router.post("/api/v1/crawl")
async def crawl(request: CrawlRequestSerializer) -> list[CrawlResponseSerializer]:
    try:
        data = CrawlAppsService.crawl_app_store_apps_by_company_name(request.company_name)
    except CrawlException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return [
        CrawlResponseSerializer(
            app_name=item.app_name,
            app_id=item.app_id,
            app_url=item.app_url,
            app_targets=item.app_targets,
        )
        for item in data
    ]
