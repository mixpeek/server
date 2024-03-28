import uuid
from datetime import datetime
from fastapi.responses import JSONResponse
from typing import Optional
import httpx
from _exceptions import InternalServerError
import time
import pytz


def generate_uuid(length=36, dashes=True):
    x = uuid.uuid4()
    if dashes:
        return str(x)[:length]
    else:
        return str(x).replace("-", "")[:length]


def current_time():
    return datetime.now(pytz.UTC)


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


async def _send_post_request(url, data, timeout=None):
    try:
        start_time = time.time() * 1000
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, data=data)

        if response.status_code != 200:
            raise InternalServerError(
                f"Internal request failed with status {response.status_code}"
            )
        response_as_json = response.json()["response"]
        response_as_json["metadata"] = {}
        response_as_json["metadata"]["elapsed_time"] = time.time() * 1000 - start_time

        return response_as_json

    except Exception as e:
        print(e)
        raise InternalServerError(
            error="There was an error with the request, reach out to support"
        )
