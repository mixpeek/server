from fastapi import APIRouter, Request
from _exceptions import route_exeception_handler
from typing import Optional, Dict, Any


from .model import ParseFileRequest
from .service import ParseHandler

router = APIRouter()


@router.post("/")
@route_exeception_handler
async def parse_file(
    request: Request,
    parser_request: ParseFileRequest,
    should_chunk: Optional[bool] = True,
):
    parse_handler = ParseHandler(parser_request.file_url)
    return await parse_handler.parse(should_chunk)
