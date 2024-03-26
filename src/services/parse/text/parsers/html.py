from io import BytesIO, StringIO
from typing import Union, Dict, List, Optional
from unstructured.partition.html import partition_html
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean

from .base_parser import ParserInterface
from _exceptions import InternalServerError


class HTMLParser(ParserInterface):

    def parse(
        self,
        file_stream: BytesIO,
        should_chunk: bool,
        clean_text: bool,
        max_characters_per_chunk: Optional[int] = None,
        new_after_n_chars_per_chunk: Optional[int] = None,
        overlap_per_chunk: Optional[int] = None,
        overlap_all_per_chunk: Optional[int] = None,
    ) -> Union[List[Dict], str]:
        try:
            elements = partition_html(
                file=file_stream,
            )
            chunks = chunk_elements(
                elements=elements,
                max_characters=max_characters_per_chunk,
                new_after_n_chars=new_after_n_chars_per_chunk,
                overlap=overlap_per_chunk,
                overlap_all=overlap_all_per_chunk,
            )
            chunks_dict = [chunk.to_dict() for chunk in chunks]

            if clean_text:
                chunks_dict = [
                    {**c, "text": self._clean_chunk_text(c["text"])}
                    for c in chunks_dict
                ]

            if should_chunk:
                return chunks_dict
            else:
                combined_text = " ".join([c["text"] for c in chunks_dict])
                return combined_text

        except Exception as e:
            raise InternalServerError(
                error="Failed to parse HTML. Please try again. If the issue persists, contact support."
            )

    def _clean_chunk_text(self, text: str) -> str:
        return clean(
            text=text,
            extra_whitespace=True,
            dashes=True,
            bullets=True,
            trailing_punctuation=True,
        )
