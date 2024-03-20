from fastapi import APIRouter  # Import APIRouter instead of FastAPI

from .model import (
    EmbeddingRequest,
    EmbeddingResponse,
    ConfigsRequest,
    ConfigsResponse,
)

from embed.service import EmbeddingHandler

router = APIRouter()


@router.get("/configs", response_model=ConfigsResponse)
async def get_dimensions(data: ConfigsRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return embedding_handler.get_configs()


@router.get("/", response_model=EmbeddingResponse)
async def embed_input(data: EmbeddingRequest):
    embedding_handler = EmbeddingHandler(data.modality, data.model)
    return embedding_handler.encode(data.input)
