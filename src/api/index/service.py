from magika import Magika
from .model import CollectionModel

from storage.plugins.mongodb import MongoDBHandler
from storage.plugins.redis import RedisHandler


def detect_filetype(contents):
    try:
        m = Magika()
        res = m.identify_bytes(contents)
        print(res)
        data = {
            "label": res.output.ct_label,
            "description": res.output.description,
            "mime_type": res.output.mime_type,
            "group": res.output.group,
        }

        return data
    except Exception as e:
        raise ValueError("Error occurred while detecting filetype") from e


class CollectionService:
    @staticmethod
    def create_collection(collection: CollectionModel) -> dict:
        collection_dict = collection.dict()
        engine = collection_dict["db_connection"].get("engine")

        if engine == "mongodb":
            mongo = MongoDBHandler()
            collection_dict = mongo.create_collection(collection_dict)
