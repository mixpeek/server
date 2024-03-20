# Standard library imports
from typing import List, Optional

# Related third party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

# Local application/library specific imports
from embed.controller import router as embed_router
from parse.controller import router as parse_router
from package.controller import router as package_router
from website.controller import router as website_router

api_router = APIRouter()


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


api_router.include_router(embed_router, prefix="/embed", tags=["Embedders"])
api_router.include_router(parse_router, prefix="/parse", tags=["Parse"])
api_router.include_router(package_router, prefix="/package", tags=["Packages"])
api_router.include_router(website_router, prefix="/website", tags=["Websites"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
