from abc import ABC, abstractmethod
from io import BytesIO
from typing import Union, Dict, List

from model import ParseFileRequest


class ParserInterface(ABC):
    @abstractmethod
    def parse(
        self, file_stream: BytesIO, params: ParseFileRequest
    ) -> Union[List[Dict], str]:
        pass
