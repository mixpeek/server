from fastapi import APIRouter, HTTPException, Body, Depends, Request, Path
from typing import Optional, Dict, Any


from .model import ParseFileRequest
from .service import ParseHandler

router = APIRouter()


@router.post("/")
async def parse_file(
    request: Request,
    parser_request: ParseFileRequest,
    should_chunk: Optional[bool] = True,
):
    parse_handler = ParseHandler(parser_request.file_url)
    try:
        return await parse_handler.parse(should_chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
