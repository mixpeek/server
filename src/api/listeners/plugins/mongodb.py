from _exceptions import NotFoundError

# changes
# create
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


class MongoDBChangeHandler:
    def __init__(self, config):
        self.config = config

    def _on_delete(self):
        pass

    def _on_insert(self):
        pass

    def on_change(self, change_object):
        if change_object["operationType"] == "insert":
            return self._on_insert(change_object)
        elif change_object["operationType"] == "delete":
            return self._on_delete(change_object)
        else:
            raise NotFoundError("Operation type not found for MongoDB payload.")
