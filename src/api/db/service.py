from json import JSONEncoder
from bson import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient, ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, redis_url
import json
from utilities.helpers import current_time
import pickle

from celery import Celery

celery_app = Celery(
    "worker",
    broker=f"{redis_url}/0",
    backend=f"{redis_url}/1",
    include=["pipeline.tasks"],
)


class JSONEncoderCustom(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


def json_dumps(data):
    return dumps(data, cls=JSONEncoderCustom)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

# Initialize MongoDB
mongo_client = MongoClient(mongo_url)
sync_db = mongo_client["api"]
async_db = AsyncIOMotorClient(mongo_url)["api"]


class BaseSyncDBService:
    def __init__(self, collection, index_id):
        self.collection = sync_db[collection]
        self.index_id = index_id

    def get_one(self, lookup_conditions: dict = {}):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        return self.collection.find_one(lookup_conditions)

    def list_by_index(self, lookup_conditions=None, limit=None, offset=None):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})

        query = self.collection.find(lookup_conditions)

        if offset is not None:
            query = query.skip(offset)
        if limit is not None:
            query = query.limit(limit)

        return list(query)

    def aggregate(self, pipeline: list = [], limit=None, offset=None):
        base_match = {"$match": {"index_id": self.index_id}}

        # Construct the final aggregation pipeline
        final_pipeline = [base_match] + pipeline

        # Apply pagination using limit and offset
        if offset is not None:
            skip_stage = {"$skip": offset}
            final_pipeline.append(skip_stage)
        if limit is not None:
            limit_stage = {"$limit": limit}
            final_pipeline.append(limit_stage)

        results = self.collection.aggregate(final_pipeline)
        return list(results)

    def create_one(self, full_object: dict, session=None):
        new_object = {
            "index_id": self.index_id,
            "created_at": current_time(),
            **full_object,
        }
        self.collection.insert_one(new_object, session=session)
        return new_object

    def update_one(self, lookup_conditions: dict = {}, updated_data: dict = {}):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})

        updated_data.update({"updated_at": current_time()})

        return self.collection.find_one_and_update(
            lookup_conditions,
            {"$set": updated_data},
            return_document=ReturnDocument.AFTER,
        )

    def delete_one(self, lookup_conditions: dict = {}):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        return self.collection.delete_one(lookup_conditions)

    @property
    def db_client(self):
        return sync_db

    @property
    def client(self):
        return self.collection


class BaseAsyncDBService:
    def __init__(self, collection, index_id):
        self.collection = async_db[collection]
        self.index_id = index_id

    async def create_one(self, full_object: dict, session=None):
        full_object.update({"index_id": self.index_id, "created_at": current_time()})
        return await self.collection.insert_one(full_object, session=session)

    async def get_one(self, lookup_conditions: dict):
        if lookup_conditions is None:
            lookup_conditions = {}
        lookup_conditions.update({"index_id": self.index_id})
        return await self.collection.find_one(lookup_conditions)

    async def update_one(self, lookup_conditions: dict, updated_data: dict):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        updated_data.update({"updated_at": current_time()})

        return await self.collection.update_one(
            lookup_conditions, {"$set": updated_data}
        )

    async def delete_one(self, lookup_conditions: dict):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})

        return await self.collection.delete_one(lookup_conditions)

    async def list_many(self, lookup_conditions, limit=10, offset=0):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        cursor = self.collection.find(lookup_conditions).skip(offset).limit(limit)
        return [doc async for doc in cursor]
