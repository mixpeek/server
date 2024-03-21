import aiohttp

from unstructured.partition.pdf import partition_pdf

# from unstructured.partition.docx import partition_docx
# from unstructured.partition.txt import partition_txt
# from unstructured.partition.md import partition_md
# from unstructured.partition.html import partition_html
# from unstructured.partition.xml import partition_xml

from unstructured.cleaners.core import clean
from unstructured.chunking.basic import chunk_elements


from _exceptions import InternalServerError, NotFoundError, BadRequestError


class TextService:
    def __init__(self, file_stream, metadata):
        self.metadata = metadata
        self.file_ext = metadata["label"]
        self.file_stream = file_stream
        self.chunks = []
        self.partition_handlers = {
            "pdf": self.pdf_handler,
            # "docx": partition_docx,
            # "txt": partition_txt,
            # "md": partition_md,
            # "html": partition_html,
            # "xml": partition_xml,
        }

    async def handler(self, should_chunk=True):
        handler = self.partition_handlers.get(self.file_ext)
        if handler:
            return await handler(should_chunk)
        else:
            raise BadRequestError(error=f"Unsupported file: {self.file_ext}")

    # TODO: we'll want to migrate to a seperate module eventually
    # Asynchronously handle PDF files
    async def pdf_handler(self, should_chunk=True):
        try:
            # Partition the PDF into elements
            elements = partition_pdf(
                file=self.file_stream,
                infer_table_structure=False,
                metadata_filename=self.metadata["filename"],
                # strategy="hi_res",
                # hi_res_model_name="detectron2_onnx",
            )
            # Chunk the elements
            chunks = self.chunk_elements(elements)
            # Process the chunks based on the should_chunk flag
            return self.process_chunks(chunks, should_chunk)
        except Exception as e:
            # Raise an internal server error if an exception occurs
            raise InternalServerError(error=str(e))

    # Chunk the elements
    def chunk_elements(self, elements, chunk_size=500, overlap_percent=15):
        # Calculate the overlap subset
        overlap_subset = int(chunk_size * (overlap_percent / 100))
        # Return the chunked elements
        return chunk_elements(
            elements,
            max_characters=chunk_size,
            overlap=overlap_subset,
        )

    # Process the chunks
    def process_chunks(self, chunks, should_chunk):
        # If should_chunk is True, process each chunk individually
        if should_chunk:
            return [self.process_chunk(chunk) for chunk in chunks]
        # If should_chunk is False, join all chunks into a single string
        else:
            return "".join(self.clean_and_join(chunk) for chunk in chunks)

    # Process a single chunk
    def process_chunk(self, chunk):
        chunk_dict = chunk.to_dict()
        chunk_dict["text"] = self.clean_text(chunk_dict["text"])
        return chunk_dict

    # Clean and join a chunk
    def clean_and_join(self, chunk):
        return self.clean_text(chunk.to_dict()["text"])

    # Clean the text
    def clean_text(self, text):
        return clean(text, bullets=True, extra_whitespace=True, dashes=True)
