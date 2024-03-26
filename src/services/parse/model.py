from pydantic import BaseModel, validator, ValidationError
from typing import List, Union, Optional
from enum import Enum
from _exceptions import BadRequestError


class ParseFileRequest(BaseModel):
    file_url: Optional[str] = None
    contents: Optional[str] = None
    should_chunk: Optional[bool] = True
    clean_text: Optional[bool] = True

    # unstructured library chunk specific parameters
    # https://github.com/Unstructured-IO/unstructured/blob/main/unstructured/chunking/basic.py#L46
    max_characters_per_chunk: Optional[int] = None
    new_after_n_chars_per_chunk: Optional[int] = None
    overlap_per_chunk: Optional[int] = None
    overlap_all_per_chunk: Optional[bool] = None

    @validator("contents", pre=True, always=True)
    def check_file_data(cls, v, values, **kwargs):
        file_url = values.get("file_url") if "file_url" in values else None
        contents = v
        if file_url is None and contents is None:
            raise BadRequestError(
                error={"message": "Either 'file_url' or 'contents' must be provided."}
            )
        if file_url is not None and contents is not None:
            raise BadRequestError(
                error={
                    "message": "Only one of 'file_url' or 'contents' can be provided."
                }
            )
        return v
