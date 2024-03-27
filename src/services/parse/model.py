from pydantic import BaseModel, validator
from typing import Optional
from _exceptions import BadRequestError


class ParseFileRequest(BaseModel):
    # Common Parameters across Parsers
    file_url: Optional[str] = (
        None  # This should be a Union (either file_url or contents)
    )
    contents: Optional[str] = None
    should_chunk: Optional[bool] = True
    clean_text: Optional[bool] = True
    max_characters_per_chunk: Optional[int] = None

    # Parser specific Parameters
    # Defined in <modality>/parsers/model.py e.g. text/parsers/model.py
    class Config:
        extra = "allow"
