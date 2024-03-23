from fastapi import APIRouter

from generate.models.model import GenerationResponse, GenerationRequest
from generate.service import generate_orchestrator

from _exceptions import route_exeception_handler


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
@route_exeception_handler
async def generate(request: GenerationRequest) -> GenerationResponse:
    generate_request = await generate_orchestrator(request)
    return generate_request
