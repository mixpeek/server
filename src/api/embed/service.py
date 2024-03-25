import httpx
import json
import time

from config import services_url

from _exceptions import InternalServerError, NotFoundError, BadRequestError
from utilities.methods import create_success_response, _send_post_request


class EmbeddingHandler:
    def __init__(self, modality="text", model="sentence-transformers/all-MiniLM-L6-v2"):
        self.modality = modality
        self.model = model

    async def encode(self, data):
        url = f"{services_url}/embed/{self.modality}"
        try:
            start_time = time.time() * 1000
            resp = await _send_post_request(url, json.dumps(data))
            return create_success_response(resp)
        except Exception as e:
            raise InternalServerError(
                error="There was an error with the request, reach out to support"
            )

    async def get_configs(self):
        """
        accepts
            modality: Optional[Modality] = "text"
            model: Optional[str] = "sentence-transformers/all-MiniLM-L6-v2"
        """
        url = f"{services_url}/embed/{self.modality}/config"
        data = {"model": self.model, "modality": self.modality}
        try:
            start_time = time.time() * 1000
            resp = await _send_post_request(url, json.dumps(data))
            return create_success_response(resp)
        except Exception as e:
            raise InternalServerError(
                error="There was an error with the request, reach out to support"
            )
