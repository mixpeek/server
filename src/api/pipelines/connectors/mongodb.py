from _exceptions import NotFoundError

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel


# changes
# insert
{
    "_id": {
        "_data": "8265FF3B3C000000012B022C0100296E5A1004392BF74A2CBC4D01B169EC58D853A32746645F6964006465FF3B3AC3DFD5EF4FB1D2F70004"
    },
    "operationType": "insert",
    "clusterTime": {"$timestamp": {"t": 1711225660, "i": 1}},
    "wallTime": "2024-03-23T20:27:40.270Z",
    "fullDocument": {"_id": "65ff3b3ac3dfd5ef4fb1d2f7"},
    "ns": {"db": "use_cases", "coll": "legal_cases"},
    "documentKey": {"_id": "65ff3b3ac3dfd5ef4fb1d2f7"},
}

# delete
{
    "_id": {
        "_data": "8265FF3B38000000012B022C0100296E5A1004392BF74A2CBC4D01B169EC58D853A32746645F6964006465FDCE1FAD7B6467D8108E340004"
    },
    "operationType": "delete",
    "clusterTime": {"$timestamp": {"t": 1711225656, "i": 1}},
    "wallTime": "2024-03-23T20:27:36.678Z",
    "ns": {"db": "use_cases", "coll": "legal_cases"},
    "documentKey": {"_id": "65fdce1fad7b6467d8108e34"},
}

# update
{
    "_id": {
        "_data": "8265FF49C6000000022B022C0100296E5A1004392BF74A2CBC4D01B169EC58D853A32746645F6964006465FF3945C3DFD5EF4FB1D2F00004"
    },
    "operationType": "update",
    "clusterTime": {"$timestamp": {"t": 1711229382, "i": 2}},
    "wallTime": "2024-03-23T21:29:42.331Z",
    "fullDocument": {
        "_id": "65ff3945c3dfd5ef4fb1d2f0",
        "citation": "McCutcheon v. Maryland, 4 Wheat. 316, 436 (1819)",
        "description": "A founddational case on the power of state taxation over federal institutions.",
        "decisionDate": "1819-03-06",
    },
    "ns": {"db": "use_cases", "coll": "legal_cases"},
    "documentKey": {"_id": "65ff3945c3dfd5ef4fb1d2f0"},
    "updateDescription": {
        "updatedFields": {
            "description": "A founddational case on the power of state taxation over federal institutions."
        },
        "removedFields": [],
        "truncatedArrays": [],
    },
}


class MongoDBConnection(BaseModel):
    host: str
    port: str
    username: str
    password: str
    database: str
    collection: str


class MongoDBChangeHandler:
    def __init__(self, connection: MongoDBConnection):
        connection_string = f"mongodb://{connection.username}:{connection.password}@{connection.host}:{connection.port}"
        self.user_client = AsyncIOMotorClient(connection_string)[connection.collection]

    def _on_insert(self):
        pass

    def on_change(self, change_object):
        if change_object["operationType"] == "insert":
            return self._on_insert(change_object)
        else:
            raise NotFoundError("Operation type not found for MongoDB payload.")

    def perform_write(self):
        pass
