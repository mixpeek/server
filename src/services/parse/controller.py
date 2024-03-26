from fastapi import APIRouter

from .model import ParseFileRequest
from .service import ParseHandler
from _exceptions import route_exeception_handler


router = APIRouter()


@router.post("/{modality}")
@route_exeception_handler
async def parse_file(
    modality: str,
    parser_request: ParseFileRequest,
):
    parse_handler = ParseHandler(parser_request.file_url)
    return await parse_handler.parse(
        modality=modality,
        should_chunk=parser_request.should_chunk,
        clean_text=parser_request.clean_text,
        max_characters_per_chunk=parser_request.max_characters_per_chunk,
        new_after_n_chars_per_chunk=parser_request.new_after_n_chars_per_chunk,
        overlap_per_chunk=parser_request.overlap_per_chunk,
        overlap_all_per_chunk=parser_request.overlap_all_per_chunk,
    )
