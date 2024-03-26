from .plugins.mongodb import MongoDBHandler
from pydantic import ValidationError


# from .plugins.qdrant import QdrantHandler
# from .plugins.postgres import PostgresHandler
# from .plugins.redis import RedisHandler
# from .plugins.weaviate import WeaviateHandler
# from .plugins.pinecone import PineconeHandler

from _exceptions import StorageConnectionError


class StorageService:
    def __init__(self, connection_info, db_handler):
        self.connection_info = connection_info
        self.storage_handlers = {
            "mongodb": MongoDBHandler(),
        }
        # Validate connection_info against the appropriate Pydantic model
        try:
            self.storage_handler = self.storage_handlers[db_handler]
            self.storage_handler.connection_info = (
                self.storage_handler.ConnectionModel.model_validate(connection_info)
            )
        except ValidationError as e:
            raise StorageConnectionError(f"Invalid connection info: {e}")
        except KeyError:
            raise StorageConnectionError(f"Unsupported storage handler: {db_handler}")

    def connect_to_db(self):
        try:
            self.storage_handler.connect()
            return True
        except Exception as e:
            print(f"Failed to connect to DB: {e}")
            return False

    def write_to_db(self, data):
        try:
            self.storage_handler.write(data)
            return True
        except Exception as e:
            print(f"Failed to write to DB: {e}")
            return False
