from fastapi import APIRouter  # Import APIRouter instead of FastAPI
from _utils import create_success_response

from .model import PackageData
from .service import PackageManager

router = APIRouter()


@router.post("")
async def process_request(data: PackageData):
    processor = PackageManager()
    return await processor.process(data.model_dump())
