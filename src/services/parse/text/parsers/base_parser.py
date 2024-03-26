from abc import ABC, abstractmethod
from io import BytesIO
from typing import Union, Dict, List, Optional


class ParserInterface(ABC):
    @abstractmethod
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
        pass
