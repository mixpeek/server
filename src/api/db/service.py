from json import JSONEncoder
from bson import ObjectId
from bson.json_util import dumps
from kombu.serialization import register
from pymongo import MongoClient, ReturnDocument
from motor.motor_asyncio import AsyncIOMotorClient
from config import mongo_url, redis_url
import json
from utilities.helpers import current_time
import redis
import hashlib
import pickle
import time

from celery import Celery, current_task

celery_app = Celery(
    "worker",
    broker=f"{redis_url}/0",
    backend=f"{redis_url}/1",
    include=["batch.tasks", "loaders.tasks"],
)


class JSONEncoderCustom(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


def json_dumps(data):
    return dumps(data, cls=JSONEncoderCustom)


register(
    "json",
    json_dumps,
    json.loads,
    content_type="application/json",
    content_encoding="utf-8",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
)

# Initialize MongoDB
mongo_client = MongoClient(mongo_url)
sync_db = mongo_client["api"]
async_db = AsyncIOMotorClient(mongo_url)["api"]


class RedisHandler:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(redis_url)
        self.keys_to_remove = ["last_run", "updated_at"]

    def hash_and_retrieve(self, workbook, query):
        start_time = time.time() * 1000

        # Create a copy of the workbook object and remove unwanted keys
        workbook_copy = workbook.copy()
        for key in self.keys_to_remove:
            workbook_copy.pop(key, None)

        # Create a hash of the workbook object and query
        hash_object = hashlib.sha256()
        hash_object.update(pickle.dumps(workbook_copy))
        hash_object.update(json.dumps(query).encode())
        self.hash_key = hash_object.hexdigest()

        # Check if the hash exists in Redis
        if self.redis_client.exists(self.hash_key):
            # If the hash exists, retrieve it and store it in a class variable
            self.result = pickle.loads(self.redis_client.get(self.hash_key))

            # Modify the metadata.runtime in each object in the data array of the result
            for obj in self.result["data"]:
                obj["metadata"]["runtime"] = (time.time() * 1000) - start_time

            return True
        else:
            return False

    def store_run_response(self, run_response):
        # If the hash doesn't exist, store the run response in Redis
        if not self.redis_client.exists(self.hash_key):
            self.redis_client.set(self.hash_key, pickle.dumps(run_response))


class BaseSyncDBService:
    def __init__(self, collection, index_id, version_id=None, scope=None):
        self.collection = sync_db[collection]
        self.index_id = index_id
        self.version_id = version_id
        self.scope = scope
        self.global_scope_name = "global"

    """Read methods"""

    def get_one(self, lookup_conditions: dict = {}):
        if lookup_conditions is None:
            lookup_conditions = {}

        # override index_id if scope is provided
        if self.scope is not None:
            lookup_conditions["scope.id"] = self.scope
            if self.scope != self.global_scope_name:
                lookup_conditions["index_id"] = self.index_id
        else:
            lookup_conditions.update({"index_id": self.index_id})

        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id

        return self.collection.find_one(lookup_conditions)

    def list_by_index(self, lookup_conditions=None, limit=None, offset=None):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        # if the scope is provided, add it to the query
        if self.scope is not None:
            # we can use dot notation since its a query
            lookup_conditions["scope.id"] = self.scope
            # if the scope is global, do not use index_id
            if self.scope == self.global_scope_name:
                lookup_conditions.pop("index_id", None)

        # if the version_id is provided, add it to the query
        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id

        query = self.collection.find(lookup_conditions)
        if offset is not None:
            query = query.skip(offset)
        if limit is not None:
            query = query.limit(limit)

        return list(query)

    def aggregate(self, pipeline: list = [], limit=None, offset=None):
        base_match = {"$match": {"index_id": self.index_id}}

        # if the scope is provided, add it to the query
        if self.scope is not None:
            # we can use dot notation since its a query
            base_match["$match"]["scope.id"] = self.scope
            # if the scope is global, do not use index_id
            if self.scope == self.global_scope_name:
                base_match["$match"].pop("index_id", None)

        if self.version_id is not None:
            base_match["$match"]["version_id"] = self.version_id

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

    """Write methods"""

    def create_one(self, full_object: dict, session=None):
        new_object = {
            "index_id": self.index_id,
            "created_at": current_time(),
            **full_object,
        }
        if self.version_id is not None:
            new_object["version_id"] = self.version_id
        self.collection.insert_one(new_object, session=session)
        return new_object

    def update_one(self, lookup_conditions: dict = {}, updated_data: dict = {}):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
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
        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
        return self.collection.delete_one(lookup_conditions)

    @property
    def db_client(self):
        return sync_db

    @property
    def client(self):
        return self.collection


class BaseAsyncDBService:
    def __init__(self, collection, index_id, version_id=None, scope=None):
        self.collection = async_db[collection]
        self.index_id = index_id
        self.version_id = version_id
        self.scope = scope

    async def create_one(self, full_object: dict, session=None):
        full_object.update({"index_id": self.index_id, "created_at": current_time()})
        if self.version_id is not None:
            full_object["version_id"] = self.version_id
        return await self.collection.insert_one(full_object, session=session)

    async def get_one(self, lookup_conditions: dict):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        # if the scope is provided, add it to the query
        if self.scope is not None:
            # we can use dot notation since its a query
            lookup_conditions["scope.id"] = self.scope
            # if the scope is global, do not use index_id
            if self.scope == self.global_scope_name:
                lookup_conditions.pop("index_id", None)

        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
        return await self.collection.find_one(lookup_conditions)

    async def update_one(self, lookup_conditions: dict, updated_data: dict):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
        updated_data.update({"updated_at": current_time()})
        return await self.collection.update_one(
            lookup_conditions, {"$set": updated_data}
        )

    async def delete_one(self, lookup_conditions: dict):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
        return await self.collection.delete_one(lookup_conditions)

    async def list_many(self, lookup_conditions, limit=10, offset=0):
        if lookup_conditions is None:
            lookup_conditions = {}

        lookup_conditions.update({"index_id": self.index_id})
        # if the scope is provided, add it to the query
        if self.scope is not None:
            # we can use dot notation since its a query
            lookup_conditions["scope.id"] = self.scope
            # if the scope is global, do not use index_id
            if self.scope == self.global_scope_name:
                lookup_conditions.pop("index_id", None)

        if self.version_id is not None:
            lookup_conditions["version_id"] = self.version_id
        cursor = self.collection.find(lookup_conditions).skip(offset).limit(limit)
        return [doc async for doc in cursor]

    # async def client(self):
    #     return await self.collection
