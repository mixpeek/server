from fastapi import APIRouter, HTTPException, Body, Depends, Request
import json

# from .model import ConnectionInformation
from .service import ListenerAsyncService

from _exceptions import route_exeception_handler

router = APIRouter()


{
    "listener": {
        # connection information
        "connection_information": {
            "engine": "mongodb",
            "host": "",
            "port": "",
            "username": "",
            "password": "",
            "database": "",
            "collection": "documents",
        },
        "pipeline": [
            {
                "source": {
                    "filters": {"status": "processing"},  # must match all of these
                    "actions": ["insert"],
                    "field": {
                        "name": "file_url",
                        "type": "url",  # vs inline
                        "embedding_model": "jinaai/jina-embeddings-v2-base-en",
                    },
                },
                "destination": {
                    "collection": "documents_elements",
                    "new_field_name": "file_elements",  # contents of the chunks
                    "new_embeddings": "file_embeddings",
                },
            }
        ],
    }
}


@router.post("/{provider}")
@route_exeception_handler
async def receive_payload(request: Request):
    listener_service = ListenerAsyncService(request.index_id)
    obj = await request.json()

    print(obj)
    # await listener_service.process(obj)

    return {"message": "received"}
