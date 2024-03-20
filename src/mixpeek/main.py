from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
import logging


from _exceptions import (
    InternalServerError,
    NotFoundError,
    BadRequestError,
)
from _utils import create_json_response

from api import api_router


log = logging.getLogger(__name__)


app = FastAPI(openapi_url="/docs/openapi.json", title="NUX API")


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(BadRequestError)
async def bad_request_exception_handler(request: Request, exc: BadRequestError):
    return create_json_response(exc.success, exc.status, exc.error, exc.response)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return create_json_response(False, 422, exc.errors(), None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
