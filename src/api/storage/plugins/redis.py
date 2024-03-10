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
