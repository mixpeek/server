from fastapi import APIRouter, Body, Depends, Request
from typing import Optional, List

from utilities.methods import create_success_response
from _exceptions import route_exeception_handler

from .service import PipelineAsyncService

router = APIRouter()


# organizations.connections
{
    "connection_information": {
        "engine": "mongodb",
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "database": "",
        "collection": "documents",
    }
}


# pipelines collection
{
    "enabled": True,
    "storage": "mongodb",
    "source": {
        "filters": {"status": "processing"},  # must match all of these
        "on_operation": ["insert"],
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


# invoke pipeline
@router.post("/{provider}")
@route_exeception_handler
async def invoke_pipeline(request: Request):
    pipeline_service = PipelineAsyncService(request.index_id)
    payload = await request.json()
    pipeline_service.process_payload(payload)
    return create_success_response({"message": "Pipeline processed."})


# create pipeline
@router.post("/")
@route_exeception_handler
async def create_pipeline(request: Request):
    return create_success_response({"message": "Pipeline created."})


# list pipelines
@router.get("/")
@route_exeception_handler
async def list_pipelines(request: Request):
    return create_success_response({"message": "Pipelines listed."})


# modify pipeline
@router.put("/{pipeline_id}")
@route_exeception_handler
async def modify_pipeline(request: Request):
    return create_success_response({"message": "Pipeline modified."})
