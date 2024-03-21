from fastapi import APIRouter, Request

from _exceptions import BadRequestError, InternalServerError, NotFoundError


from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    ConfigsRequest,
    ConfigsResponse,
)

from .service import EmbeddingHandler

router = APIRouter()


@router.get("/config", response_model=ConfigsResponse)
async def get_dimensions(data: ConfigsRequest):
    try:
        embedding_handler = EmbeddingHandler(data.modality, data.model)
        return await embedding_handler.get_configs()
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)


@router.get("/", response_model=EmbeddingResponse)
async def embed_input(data: EmbeddingRequest):
    try:
        embedding_handler = EmbeddingHandler(data.modality, data.model)
        return await embedding_handler.encode(data.model_dump())
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
