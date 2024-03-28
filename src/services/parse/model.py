from pydantic import BaseModel
from typing import Optional


class ParseFileRequest(BaseModel):
    # Common Settings across Parsers
    file_url: Optional[str] = (
        None
    )
    contents: Optional[str] = None
    should_chunk: Optional[bool] = True
    clean_text: Optional[bool] = True
    max_characters_per_chunk: Optional[int] = None

    # Parser Specific Settings
    # Models defined in api/parsers/model.py
    pdf_settings: Optional[dict] = {}
    html_settings: Optional[dict] = {}
    csv_settings: Optional[dict] = {}
    ppt_settings: Optional[dict] = {}
    pptx_settings: Optional[dict] = {}
    xlsx_settings: Optional[dict] = {}
    txt_settings: Optional[dict] = {}
