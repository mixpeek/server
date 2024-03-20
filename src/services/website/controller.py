from fastapi import APIRouter

from .model import (
    WebsiteData,
)

from .service import WebScraper


router = APIRouter()


@router.post("")
async def process_website(data: WebsiteData):
    scraper = WebScraper(data.website, data.max_depth)
    return await scraper.scrapeData()
