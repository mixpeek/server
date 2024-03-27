from fastapi import APIRouter

from .model import GenerationResponse, GenerationRequest
from .service import generate_orchestrator

from _exceptions import route_exeception_handler


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
@route_exeception_handler
async def generate(request: GenerationRequest):
    generate_request = await generate_orchestrator(request)
    return generate_request
