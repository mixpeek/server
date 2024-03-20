import cgi
import httpx
from io import BytesIO
from magika import Magika
import time

from .utils import generate_filename_from_url, get_filename_from_cd
from .text.service import TextService

from _exceptions import InternalServerError, NotFoundError, BadRequestError
from _utils import create_success_response

files = {
    "text": ["pdf", "docx", "txt", "md", "html", "xml"],
    "image": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"],
    "audio": ["mp3", "wav", "ogg", "flac", "m4a", "wma", "aac"],
    "video": ["mp4", "mkv", "webm", "avi", "mov", "wmv", "flv"],
}


class ParseHandler:
    def __init__(self, file_url):
        self.file_url = file_url

    async def download_into_memory(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.file_url)
                if response.status_code == 200:
                    filename = get_filename_from_cd(
                        response.headers.get("content-disposition")
                    )
                    if not filename:
                        filename = generate_filename_from_url(self.file_url)
                    else:
                        raise BadRequestError(error={"message": "Filename not found"})
                    return response.content, filename
                else:
                    raise BadRequestError(error={"message": "Error downloading file"})

        except Exception as e:
            raise BadRequestError(error={"message": "Error downloading file"})

    def detect_filetype(self, contents):
        try:
            m = Magika()
            res = m.identify_bytes(contents)
            # {
            #     "label": "pdf",
            #     "description": "PDF document",
            #     "mime_type": "application/pdf",
            #     "group": "document",
            # }
            data = {
                "label": res.output.ct_label,
                "mime_type": res.output.mime_type,
                "group": res.output.group,
            }
            return data
        except Exception as e:
            raise BadRequestError(
                error={"message": "Error occurred while detecting filetype"}
            )

    async def parse(self, should_chunk=True):
        # Download file into memory
        contents, filename = await self.download_into_memory()
        stream = BytesIO(contents)

        # Detect file type
        metadata = self.detect_filetype(stream.getvalue())
        metadata.update({"filename": filename})

        text_service = TextService(self.file_url, metadata)

        start_time = time.time() * 1000
        # Process file based on chunking preference and file type
        if metadata["label"] == "pdf":
            text_output = await text_service.run(should_chunk)
        else:
            raise BadRequestError(error={"message": "File type not supported"})

        # Calculate elapsed time
        metadata["elapsed_taken"] = (time.time() * 1000) - start_time

        return create_success_response({"text": text_output, "metadata": metadata})
