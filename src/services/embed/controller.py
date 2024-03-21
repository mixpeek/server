from fastapi import APIRouter  # Import APIRouter instead of FastAPI

from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    ConfigsRequest,
    ConfigsResponse,
)

from embed.service import EmbeddingHandler

from _exceptions import BadRequestError, InternalServerError, NotFoundError

router = APIRouter()


@router.post("/{modality}", response_model=EmbeddingResponse)
async def embed_input(modality: str, data: EmbeddingRequest):
    embedding_handler = EmbeddingHandler(modality, data.model)
    try:
        return embedding_handler.encode(data.input)
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)


@router.post("/{modality}/config", response_model=ConfigsResponse)
async def get_dimensions(modality: str, data: ConfigsRequest):
    embedding_handler = EmbeddingHandler(modality, data.model)
    return embedding_handler.get_configs()
