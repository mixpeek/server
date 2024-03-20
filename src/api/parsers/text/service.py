import httpx
import json

# from unstructured.partition.pdf import partition_pdf
# from unstructured.cleaners.core import clean
# from unstructured.partition.api import partition_via_api
# from unstructured.chunking.basic import chunk_elements

# from config import unstructured_api_key, unstructured_api_url

from _exceptions import InternalServerError

from config import services_url


class TextService:
    def __init__(self, file_url, metadata):
        self.metadata = metadata
        self.file_url = file_url
        self.chunks = []

    # def _clean(self, text):
    #     return clean(text, bullets=True, extra_whitespace=True, dashes=True)

    # def _chunk(self, elements, chunk_size=500, overlap_percent=15):
    #     overlap_subset = int(chunk_size * (overlap_percent / 100))
    #     return chunk_elements(
    #         elements,
    #         max_characters=chunk_size,
    #         overlap=overlap_subset,
    #     )

    async def run(self, should_chunk=True):
        try:
            url = f"{services_url}/parse?should_chunk={str(should_chunk)}"
            data = json.dumps({"file_url": self.file_url})
            print(url, data)

            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data)

            if response.status_code != 200:
                raise Exception(f"Request failed with status {response.status_code}")

            return response.json()["response"]["text"]

            # elements = partition_via_api(
            #     file=self.file_stream,
            #     api_key=unstructured_api_key,
            #     api_url=unstructured_api_url,
            #     metadata_filename=self.metadata["filename"],
            # )

            # elements = partition_pdf(
            #     file=self.file_stream,
            #     infer_table_structure=False,
            #     metadata_filename=self.metadata["filename"],
            #     # strategy="hi_res",
            #     # hi_res_model_name="detectron2_onnx",
            # )

            # chunks = self._chunk(elements)

            # # Process chunks based on should_chunk flag
            # processed_chunks = self.process_chunks(chunks, should_chunk)
            return processed_chunks
        except Exception as e:
            raise InternalServerError(
                error="There was an error with the request, reach out to support"
            )

    # def process_chunks(self, chunks, should_chunk):
    #     if should_chunk:
    #         return [self.process_chunk(c) for c in chunks]
    #     else:
    #         return "".join(self._clean(c.to_dict()["text"]) for c in chunks)

    # def process_chunk(self, chunk):
    #     response_obj = chunk.to_dict()
    #     response_obj["text"] = self._clean(response_obj["text"])
    #     return response_obj
