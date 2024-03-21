import cgi
import httpx
from io import BytesIO
from magika import Magika
import time

from .utils import generate_filename_from_url, get_filename_from_cd
from .text.service import TextService

from _exceptions import InternalServerError, NotFoundError, BadRequestError
from _utils import create_success_response


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

    async def parse(self, modality, should_chunk=True):
        # Download file into memory
        contents, filename = await self.download_into_memory()
        stream = BytesIO(contents)

        # Detect file type
        metadata = self.detect_filetype(stream.getvalue())
        metadata.update({"filename": filename})

        if modality == "text":
            text_service = TextService(stream, metadata)
            output = await text_service.handler(should_chunk)
        else:
            raise BadRequestError(error="Modality not supported")

        # # Process file based on chunking preference and file type
        # if metadata["label"] == "pdf":
        #     text_output = await text_service.run(should_chunk)
        # else:
        #     raise BadRequestError(error={"message": "File type not supported"})

        return create_success_response({modality: output, "metadata": metadata})
