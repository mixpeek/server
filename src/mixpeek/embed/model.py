from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class Modality(Enum):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    TEXT = "text"


class ConfigsRequest(BaseModel):
    modality: Optional[Modality] = "text"
    model: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"


class ConfigsResponse(BaseModel):
    dimensions: int
    elapsed_time: float
    token_size: int


class EmbeddingRequest(BaseModel):
    input: str
    modality: Optional[Modality] = "text"
    model: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingResponse(BaseModel):
    embedding: List[float]
    elapsed_time: float
