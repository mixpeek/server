from fastapi import HTTPException
from db.service import BaseAsyncDBService

from .plugins.mongodb import MongoDBChangeHandler

"""
Accepts a payload and processes it using the listener service.

Pseudocode:
1. Grabs all the pipelines from the local db run the following for each:
    2. match the db & coll provided from the payload with the corresponding pipeleines in the db
    3. check that the payload matches the doc_filters and operationType
    4. if the field.type is url:
        5. download the file
        6. extract the text
        7. embed the text
        8. insert the text, embeddings, and url into the destination collection
    5. if the field.type is inline:
        6. extract the text
        7. embed the text
        8. insert the text, embeddings, and url into the destination collection


Args:
    request (Request): The incoming request object.

Returns:
    dict: A dictionary containing the response message.
"""


class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)
