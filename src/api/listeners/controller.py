from fastapi import APIRouter, HTTPException, Body, Depends, Request
import json

from .model import ConnectionInformation
from .service import ListenerAsyncService

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
        "processes": [
            {
                "source": {
                    "filters": {"status": "processing"},  # must match all of these
                    "actions": ["insert"],
                    "field": {
                        "name": "file_url",
                        "type": "url",  # vs inline
                        "embedding_model": "bert",
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
async def receive_payload(request: Request):
    listener_service = ListenerAsyncService(request.index_id)
    obj = await request.json()
    listener_service.insert(obj["record"])

    return {"message": "received"}
