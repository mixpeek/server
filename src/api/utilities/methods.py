import traceback
from fastapi import HTTPException
import logging
import sentry_sdk


class BadRequestError(HTTPException):
    # deafults to 400 error if no error_code provided
    def __init__(self, detail=None, status_code=400, headers=None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


def log_and_send_to_sentry(e):
    logging.error("An error occurred: %s", e)
    traceback.print_exc()
    sentry_sdk.capture_exception(e)
