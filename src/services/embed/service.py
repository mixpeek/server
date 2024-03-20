from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time

from _utils import create_success_response
from _exceptions import BadRequestError

from .modalities.text import TextEmbeddingService

# from .modalities.image import ImageEmbeddingService
# from .modalities.audio import AudioEmbeddingService
# from .modalities.video import VideoEmbeddingService


class EmbeddingHandler:
    def __init__(self, modality, model):
        if modality == "text":
            # sentence-transformers/all-MiniLM-L6-v2
            self.service = TextEmbeddingService(model)
        # elif modality == "image":
        #     # openai/clip-vit-base-patch32
        #     self.service = ImageEmbeddingService(model)
        # elif modality == "audio":
        #     # facebook/wav2vec2-base-960h
        #     self.service = AudioEmbeddingService(model)
        # elif modality == "video":
        #     # openai/clip-vit-base-patch32
        #     self.service = VideoEmbeddingService(model)
        else:
            raise BadRequestError({"error": "Modality not supported"})

    def encode(self, data):
        start_time = time.time() * 1000
        embedding = self.service.encode(data).tolist()[0]
        return create_success_response(
            {
                "embedding": embedding,
                "elapsed_time": (time.time() * 1000) - start_time,
            }
        )

    def get_configs(self):
        start_time = time.time() * 1000
        dimensions = self.service.get_dimensions()
        token_size = self.service.get_token_size()
        return create_success_response(
            {
                "dimensions": dimensions,
                "token_size": token_size,
                "elapsed_time": (time.time() * 1000) - start_time,
            }
        )
