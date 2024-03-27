from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict


class Model(BaseModel):
    provider: str = Field(...)
    model: str = Field(...)


class Message(BaseModel):
    role: str = Field(...)
    content: str = Field(...)


class Settings(BaseModel):
    system_prompt: Optional[str] = Field(None)
    temperature: Optional[float] = Field(None)
    max_tokens: Optional[int] = Field(None)
    stop: Optional[List[str]] = Field(None)
    top_p: Optional[float] = Field(None)
    frequency_penalty: Optional[float] = Field(None)
    presence_penalty: Optional[float] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "system_prompt": "You are a helpful assistant.",
                "temperature": 0.7,
                "max_tokens": 150,
                "stop": ["\n"],
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            }
        }


class GenerationRequest(BaseModel):
    model: Model = Field(...)
    response_format: Optional[Dict] = Field(None)
    context: Optional[str] = Field(None)
    messages: List[Message] = Field(...)
    settings: Optional[Settings] = Field(None)


class Metadata(BaseModel):
    elapsed_time: Optional[float] = Field(...)
    total_tokens: Optional[int] = Field(...)
    generation_id: Optional[str] = Field(...)
    model: Optional[Model] = Field(...)
    created_at: Optional[datetime] = Field(...)


class GenerationResponse(BaseModel):
    success: bool = Field(...)
    status: int = Field(...)
    error: Optional[dict] = Field(None)
    response: dict = Field(...)
    metadata: Optional[Metadata] = Field(...)
