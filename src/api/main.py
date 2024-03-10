from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sentry_asgi import SentryMiddleware
import logging

# from .extensions import configure_extensions
# from .logger import configure_logging

from api import api_router

# from rate_limiter import limiter

log = logging.getLogger(__name__)

# we configure the logging level and format
# configure_logging()

app = FastAPI(openapi_url="/docs/openapi.json", title="Mixpeek API")

app.add_middleware(SentryMiddleware)


# # Add the limiter as a middleware
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router)
