from fastapi import APIRouter
from _exceptions import route_exeception_handler

from .model import ParseFileRequest
from .service import ParseHandler


router = APIRouter()


@router.post("/")
@route_exeception_handler
async def parse_file(
    parser_request: ParseFileRequest,
):
    parse_handler = ParseHandler(parser_request.file_url)
    return await parse_handler.parse(parser_request)
