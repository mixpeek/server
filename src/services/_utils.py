from fastapi.responses import JSONResponse
from typing import Optional


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
