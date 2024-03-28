from io import BytesIO
from typing import Union, Dict, List
from unstructured.partition.ppt import partition_ppt
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean

from .base_parser import ParserInterface
from parse.model import ParseFileRequest
from _exceptions import InternalServerError


class PPTParser(ParserInterface):

    def parse(
        self, file_stream: BytesIO, params: ParseFileRequest
    ) -> Union[List[Dict], str]:
        try:
            elements = partition_ppt(
                file=file_stream,
                **params.ppt_settings
            )
            chunks = chunk_elements(
                elements=elements,
                max_characters=params.max_characters_per_chunk,
            )
            chunks_dict = [chunk.to_dict() for chunk in chunks]

            if params.clean_text:
                chunks_dict = [
                    {**c, "text": self._clean_chunk_text(c["text"])}
                    for c in chunks_dict
                ]

            if params.should_chunk:
                return chunks_dict
            else:
                combined_text = " ".join([c["text"] for c in chunks_dict])
                return combined_text

        except Exception as e:
            raise InternalServerError(
                error="Failed to parse PPT. Please try again. If the issue persists, contact support."
            )

    def _clean_chunk_text(self, text: str) -> str:
        return clean(
            text=text,
            extra_whitespace=True,
            dashes=True,
            bullets=True,
            trailing_punctuation=True,
        )
