from ..model import ParseFileRequest
from .parsers.base_parser import ParserInterface
from .parsers.pdf import PDFParser
from .parsers.html import HTMLParser
from .parsers.csv import CSVParser
from .parsers.xlsx import XLSXParser
from .parsers.ppt import PPTParser
from .parsers.pptx import PPTXParser
from .parsers.txt import TextParser

from io import BytesIO
from typing import Union, List, Dict
from _exceptions import BadRequestError


class ParserFactory:
    @staticmethod
    def get_parser(file_ext: str) -> ParserInterface:
        parsers = {
            "pdf": PDFParser(),
            "html": HTMLParser(),
            "csv": CSVParser(),
            "xlsx": XLSXParser(),
            "ppt": PPTParser(),
            "pptx": PPTXParser(),
            "txt": TextParser(),
        }
        parser = parsers.get(file_ext.lower())
        if not parser:
            raise BadRequestError(error=f"Unsupported file type: {file_ext.lower()}")
        return parser


class TextParsingService:
    def __init__(
        self, file_stream: BytesIO, metadata: dict, parser_request: ParseFileRequest
    ):
        self.file_stream = file_stream
        self.file_ext = metadata["label"]
        self.metadata = metadata
        self.parser_request = parser_request

    async def parse(self) -> Union[List[Dict], str]:
        parser = ParserFactory.get_parser(self.file_ext)
        param_model = ParserFactory.get_param_model(self.file_ext)
        return parser.parse(
            file_stream=self.file_stream,
            params=self.parser_request,
        )
