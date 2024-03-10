import asyncio
from sentence_transformers import SentenceTransformer, util


class VectorHandler:
    def __init__(self, vector_class):
        vector_classes = {
            "sentence-transformers/all-MiniLM-L6-v2": {
                "index_name": "sentence_transformer_384",
                "dimensions": 384,
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "index_name": "sentence_transformer_768",
                "dimensions": 768,
            },
            "emilyalsentzer/Bio_ClinicalBERT": {
                "index_name": "bio_clinicalbert_768",
                "dimensions": 768,
            },
        }

        # self.vector_object = vector_classes[vector_class]
        # self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        # self.index_name = vector_classes[model_name]["index_name"]
        self.model = SentenceTransformer(vector_class)

    async def encode(self, text):
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(None, self.model.encode, [text])
        return embedding[0].tolist()

    # def get_index_name(self):
    #     return self.index_name
