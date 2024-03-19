from pydantic import BaseModel, validator, ValidationError
from typing import List, Union, Optional
from enum import Enum


class ParseFileRequest(BaseModel):
    file_url: Optional[str] = None
    contents: Optional[str] = None

    @validator("contents", pre=True, always=True)
    def check_file_data(cls, v, values, **kwargs):
        file_url = values.get("file_url") if "file_url" in values else None
        contents = v
        if file_url is None and contents is None:
            raise ValueError("Either 'file_url' or 'contents' must be provided.")
        if file_url is not None and contents is not None:
            raise ValueError("Only one of 'file_url' or 'contents' can be provided.")
        return v
