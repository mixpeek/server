from fastapi import APIRouter, Request

from _exceptions import route_exeception_handler


from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    ConfigsRequest,
    ConfigsResponse,
)

from .service import EmbeddingHandler

router = APIRouter()


@router.get("/config", response_model=ConfigsResponse)
@route_exeception_handler
async def get_dimensions(data: ConfigsRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return await embedding_handler.get_configs()


@router.get("/", response_model=EmbeddingResponse)
@route_exeception_handler
async def embed_input(data: EmbeddingRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return await embedding_handler.encode(data.model_dump())
