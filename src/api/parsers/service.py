import httpx
import json
import time

from config import services_url

from _exceptions import InternalServerError, NotFoundError, BadRequestError
from utilities.methods import create_success_response, _send_post_request

modality_to_content_types = {
    "text": [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "text/markdown",
        "text/html",
        "application/xml",
    ],
    "image": [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/bmp",
        "image/tiff",
        "image/webp",
    ],
    "audio": [
        "audio/mpeg",
        "audio/wav",
        "audio/ogg",
        "audio/flac",
        "audio/mp4",
        "audio/x-ms-wma",
        "audio/aac",
    ],
    "video": [
        "video/mp4",
        "video/x-matroska",
        "video/webm",
        "video/x-msvideo",
        "video/quicktime",
        "video/x-ms-wmv",
        "video/x-flv",
    ],
}


class ParseHandler:
    def __init__(self, file_url):
        self.file_url = file_url

    async def _get_file_type(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(self.file_url)
                print(response)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type")
                    if not content_type:
                        raise BadRequestError(
                            error={"message": "Content type not found"}
                        )
                    return content_type
                else:
                    raise BadRequestError(
                        error={"message": "Error retrieving file info"}
                    )

        except Exception as e:
            raise BadRequestError(error={"message": "Error retrieving file info"})

    def _get_modality(self, content_type):
        for modality, content_types in modality_to_content_types.items():
            if content_type in content_types:
                return modality
        raise BadRequestError(f"Content type {content_type} not recognized")

    async def parse(self, should_chunk=True):
        content_type = await self._get_file_type()
        modality = self._get_modality(content_type)

        url = f"{services_url}/parse/{modality}?should_chunk={str(should_chunk)}"
        data = json.dumps({"file_url": self.file_url})

        try:
            start_time = time.time() * 1000
            resp = await _send_post_request(url, data)
            return create_success_response(resp)
        except Exception as e:
            raise InternalServerError(
                error="There was an error with the request, reach out to support"
            )
        #     return create_success_response(resp)
        # except Exception as e:
        #     raise InternalServerError(
        #         error="There was an error with the request, reach out to support"
        #     )
