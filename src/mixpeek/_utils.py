import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Optional


def generate_uuid(length=36, dashes=True):
    x = uuid.uuid4()
    if dashes:
        return str(x)[:length]
    else:
        return str(x).replace("-", "")[:length]


def current_time():
    return datetime.utcnow()


def create_json_response(
    success: bool, status: int, error: str, response: Optional[str]
):
    return JSONResponse(
        content={
            "success": success,
            "status": status,
            "error": error,
            "response": response,
        },
        status_code=status,
    )


def create_success_response(response: Optional[str]):
    return create_json_response(True, 200, None, response)
