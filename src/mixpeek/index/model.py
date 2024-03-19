from pydantic import BaseModel, Field
from utilities.helpers import generate_uuid


class FileType(BaseModel):
    label: str
    description: str
    mime_type: str
    group: str


class EmbeddingModel(BaseModel):
    name: str
    version: str
    type: str


class CollectionModel(BaseModel):
    collection_id: str = Field(default_factory=generate_uuid)
    db_connection: dict
    embedding_model: EmbeddingModel
    embed_suffix: str = Field(default="embedding")


# responses
class CollectionResponse(CollectionModel):
    pass
