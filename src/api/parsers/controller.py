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
    print(parser_request)
    return await parse_handler.parse(
        should_chunk=parser_request.should_chunk,
        clean_text=parser_request.clean_text,
        max_characters_per_chunk=parser_request.max_characters_per_chunk,
        new_after_n_chars_per_chunk=parser_request.new_after_n_chars_per_chunk,
        overlap_per_chunk=parser_request.overlap_per_chunk,
        overlap_all_per_chunk=parser_request.overlap_all_per_chunk,
    )
