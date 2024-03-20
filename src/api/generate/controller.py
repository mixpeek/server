from fastapi import APIRouter
from _exceptions import BadRequestError, InternalServerError, NotFoundError

from generate.models.model import GenerationResponse, GenerationRequest
from generate.service import generate_orchestrator


router = APIRouter()


@router.post("/", response_model=GenerationResponse)
async def generate(request: GenerationRequest) -> GenerationResponse:
    try:
        generate_request = await generate_orchestrator(request)
        return generate_request
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
