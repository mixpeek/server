import cgi
import httpx
from io import BytesIO
from magika import Magika

from .utils import generate_filename_from_url, get_filename_from_cd
from .text.service import TextParsingService

from _exceptions import BadRequestError
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

    async def parse(
        self,
        modality,
        should_chunk=True,
        clean_text=True,
        max_characters_per_chunk=None,
        new_after_n_chars_per_chunk=None,
        overlap_per_chunk=None,
        overlap_all_per_chunk=None,
    ):
        contents, filename = await self.download_into_memory()
        stream = BytesIO(contents)

        metadata = self.detect_filetype(stream.getvalue())
        metadata.update({"filename": filename})

        if modality == "text":
            text_service = TextParsingService(
                file_stream=stream,
                should_chunk=should_chunk,
                clean_text=clean_text,
                metadata=metadata,
                max_characters_per_chunk=max_characters_per_chunk,
                new_after_n_chars_per_chunk=new_after_n_chars_per_chunk,
                overlap_per_chunk=overlap_per_chunk,
                overlap_all_per_chunk=overlap_all_per_chunk,
            )
            output = await text_service.parse()
        else:
            raise BadRequestError(error="Modality not supported")

        return create_success_response({modality: output, "metadata": metadata})
