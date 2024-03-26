from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.basic import chunk_elements
from unstructured.cleaners.core import clean

from .base_parser import ParserInterface


class ExcelParser(ParserInterface):

    async def parse(self, file_stream):
        try:
            elements = partition_pdf(
                file=file_stream,
            )
            chunks = chunk_elements(elements)
            return chunks

        except Exception as e:
            print("ExcelParser Exception")
