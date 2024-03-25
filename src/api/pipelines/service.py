import json
from db.service import BaseAsyncDBService, BaseSyncDBService
from _exceptions import BadRequestError

from organization.service import OrganizationSyncService

from parsers.service import ParseHandler
from embed.service import EmbeddingHandler

from pymongo import MongoClient


async def process_orchestrator(index_id: str, pipeline: dict, payload: dict):
    pipeline_processor = PipelineProcessor(index_id, pipeline)
    return await pipeline_processor.process(payload)


class PipelineTaskSyncService(BaseSyncDBService):
    def __init__(self, index_id, task_id):
        self.task_id = task_id
        super().__init__("pipeline_tasks", index_id)

    def create(self, full_object: dict):
        obj = {"task_id": self.task_id, "status": "PENDING", **full_object}
        return self.create_one(obj)


class PipelineAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("pipelines", index_id)


class PipelineProcessor:
    def __init__(self, index_id, pipeline: dict):
        self.index_id = index_id
        self.pipeline = pipeline

        """
            1. check if the connection exists in the organization
            2. decrypt the connection information
            3. create a connection to the source
            4. create a connection to the destination
            5. create a change handler
            6. process the change
            7. return tƒhe response and insert it into the db
        """

    # async def check_connection(self, organization):
    #     # Check if the connection exists in the organization
    #     pass

    # async def decrypt_connection_info(self, connection_info):
    #     # Decrypt the connection information
    #     pass

    # async def create_source_connection(self, decrypted_info):
    #     # Create a connection to the source
    #     pass

    # async def create_destination_connection(self, decrypted_info):
    #     # Create a connection to the destination
    #     pass

    # async def create_change_handler(self):
    #     # Create a change handler
    #     pass

    # async def process_change(self, change):
    #     # Process the change
    #     pass

    async def log_error_in_tasks_db(self, response):
        print(response)

    def insert_into_destination(self, obj):
        print("Inserted into destination collection")

    async def parse_file(self, file_url):
        parse_handler = ParseHandler(file_url)
        parse_response = await parse_handler.parse(should_chunk=True)
        return json.loads(parse_response.body.decode())

    async def process_chunks(self, chunks, file_url):
        embed_handler = EmbeddingHandler(model="jinaai/jina-embeddings-v2-base-en")
        for chunk in chunks:
            embedding_response = await embed_handler.encode({"input": chunk["text"]})
            embedding_response_content = json.loads(embedding_response.body.decode())

            if not embedding_response_content.get("success"):
                await self.log_error_in_tasks_db(
                    {
                        "task_id": "1",
                        "status_code": embedding_response_content["status"],
                        "error": embedding_response_content["message"],
                    }
                )
                continue

            obj = {
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "embedding": embedding_response_content["response"]["embedding"],
                "file_url": file_url,
            }
            self.insert_into_destination(obj)

    async def process(self, payload):
        file_url = payload["file_url"]
        parse_response_content = await self.parse_file(file_url)

        if not parse_response_content.get("success"):
            await self.log_error_in_tasks_db(
                {
                    "task_id": "1",
                    "status_code": parse_response_content["status"],
                    "error": parse_response_content["message"],
                }
            )
            return None

        await self.process_chunks(parse_response_content["response"]["text"], file_url)


# Assuming ParseHandler and EmbeddingHandler are defined elsewhere and compatible with these changes.
