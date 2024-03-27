from abc import ABC, abstractmethod
from io import BytesIO
from pydantic import BaseModel
from typing import Union, Dict, List


class ParserInterface(ABC):
    @abstractmethod
    def parse(
        self,
        file_stream: BytesIO,
        params: BaseModel
    ) -> Union[List[Dict], str]:
        pass
