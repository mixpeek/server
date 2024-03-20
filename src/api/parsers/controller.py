from fastapi import APIRouter, Request
from _exceptions import BadRequestError, InternalServerError, NotFoundError
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
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
