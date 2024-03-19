import httpx
from typing import Optional, Any
from _exceptions import InternalServerError, NotFoundError, BadRequestError


class AsyncHttpClient:
    def __init__(self, url: str, headers: dict):
        self.url = url
        self.headers = headers

    async def get(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    raise NotFoundError(f"Resource not found at {self.url}")
                elif exc.response.status_code == 400:
                    raise BadRequestError(f"Bad request to {self.url}")
                else:
                    raise InternalServerError(
                        f"An error occurred while making a GET request to {self.url}"
                    )
            except Exception as exc:
                raise InternalServerError(f"An unexpected error occurred: {exc}")

    async def post(self, data: dict):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    raise NotFoundError(f"Resource not found at {self.url}")
                elif exc.response.status_code == 400:
                    raise BadRequestError(f"Bad request to {self.url}")
                else:
                    raise InternalServerError(
                        f"An error occurred while making a POST request to {self.url}"
                    )
            except Exception as exc:
                raise InternalServerError(f"An unexpected error occurred: {exc}")
