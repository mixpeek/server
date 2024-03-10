# Standard library imports
from typing import List, Optional

# Related third party imports
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

# Local application/library specific imports
from feedback.controller import router as feedback_router
from index.controller import router as index_router


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

# # WARNING: Don't use this unless you want unauthenticated routes
# authenticated_api_router = APIRouter()


# def get_organization_path():
#     pass


# authenticated_organization_api_router = APIRouter(
#     prefix="/{organization}", dependencies=[Depends(get_organization_path)]
# )

# NOTE: All api routes should be authenticated by default
api_router.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])
api_router.include_router(index_router, prefix="/index", tags=["Index"])


@api_router.get("/", include_in_schema=False)
def hello_world():
    return "welcome to the Mixpeek api, check out the docs for more: docs.mixpeek.com"


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
