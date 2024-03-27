from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from utilities.helpers import unique_name, generate_uuid
from utilities.encryption import SecretCipher

from organization.model import Connection


# Enumerations
class FieldType(str, Enum):
    url = "url"
    inline = "inline"


class FieldSchema(BaseModel):
    name: str
    type: FieldType
    embedding_model: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"
    settings: Optional[dict] = {}


class SourceSchema(BaseModel):
    filters: dict
    on_operation: List[str]
    field: FieldSchema


class DestinationSchema(BaseModel):
    collection: str
    new_field_name: str
    new_embeddings: str


# Pipeline schema definition
class PipelineSchema(BaseModel):
    index_id: str
    created_at: datetime
    last_run: Optional[datetime]
    pipeline_id: str
    enabled: bool
    connection: Connection
    source: SourceSchema
    destination: DestinationSchema


# requests
"""Requests"""


# Pipeline schema definition
class PipelineCreateRequest(BaseModel):
    pipeline_id: str = Field(default_factory=lambda: generate_uuid(6, False))
    connection: Optional[Connection]
    source: SourceSchema
    destination: DestinationSchema
    metadata: Optional[dict] = {}
    enabled: bool = False
    last_run: Optional[datetime] = None


"""responses"""


class PipelineResponse(BaseModel):
    pipeline_id: str
    created_at: datetime
    last_run: Optional[datetime]
    enabled: bool
    connection: Connection
    source: SourceSchema
    destination: DestinationSchema
    metadata: Optional[dict] = {}
