from .parsers.base_parser import ParserInterface
from .parsers.pdf import PDFParser
from .parsers.html import HTMLParser
from .parsers.csv import CSVParser
from .parsers.excel import ExcelParser
from .parsers.ppt import PPTParser

from io import BytesIO
from typing import Optional, Union, List, Dict
from _exceptions import BadRequestError


class ParserFactory:
    @staticmethod
    def get_parser(file_ext: str) -> ParserInterface:
        parsers = {
            "pdf": PDFParser(),
            "html": HTMLParser(),
            "csv": CSVParser(),
            "excel": ExcelParser(),
            "ppt": PPTParser(),
        }
        parser = parsers.get(file_ext.lower())
        if not parser:
            raise BadRequestError(error=f"Unsupported file type: {file_ext.lower()}")
        return parser


class TextParsingService:
    def __init__(
        self,
        file_stream: BytesIO,
        should_chunk: bool,
        clean_text: bool,
        metadata: dict,
        max_characters_per_chunk: Optional[int] = None,
        new_after_n_chars_per_chunk: Optional[int] = None,
        overlap_per_chunk: Optional[int] = None,
        overlap_all_per_chunk: Optional[int] = None,
    ):
        self.file_stream = file_stream
        self.clean_text = clean_text
        self.file_ext = metadata["label"]
        self.metadata = metadata

        # Chunking Specifc Optional Parameters
        self.should_chunk = should_chunk
        self.max_characters_per_chunk = max_characters_per_chunk
        self.new_after_n_chars_per_chunk = new_after_n_chars_per_chunk
        self.overlap_per_chunk = overlap_per_chunk
        self.overlap_all_per_chunk = overlap_all_per_chunk

    async def parse(self) -> Union[List[Dict], str]:
        parser = ParserFactory.get_parser(self.file_ext)
        return parser.parse(
            file_stream=self.file_stream,
            should_chunk=self.should_chunk,
            clean_text=self.clean_text,
            max_characters_per_chunk=self.max_characters_per_chunk,
            new_after_n_chars_per_chunk=self.new_after_n_chars_per_chunk,
            overlap_per_chunk=self.overlap_per_chunk,
            overlap_all_per_chunk=self.overlap_all_per_chunk,
        )
