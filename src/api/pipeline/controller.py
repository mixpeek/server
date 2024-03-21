from fastapi import APIRouter, Body, Depends, Request
from typing import Optional, List

from _utils import create_success_response
from _exceptions import NotFoundError

from .service import PipelineSyncService

router = APIRouter()


# @router.post("/{pipeline_id}")
# async def invoke_pipeline(
#     request: Request,
#     pipeline_id: str,
#     payload: dict = Body(...),
# ):
#     pipeline_service = PipelineSyncService(request.index_id)
#     pipeline = pipeline_service.get_one({"pipeline_id": pipeline_id})

#     if not pipeline:
#         raise NotFoundError(error="Pipeline not found")

#     return await pipeline_service.invoke(pipeline, payload)


{
    "pipeline": {
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


@router.post("/")
async def create_pipeline(
    request: Request,
    payload: dict = Body(...),
):
    pipeline_service = PipelineSyncService(request.index_id)
    pipeline = pipeline_service.create_one(payload)

    # pipeline should have:
    # connection information,
    # tables/collections you want to sync/pull from (sources)
    # the column, or field(s) of each (and deciding if its url vs content)
    # embedding model (select from a list of models)
    # tables/collections you want to push to (destinations)
    # defaults to "original_elements"

    return await pipeline_service.invoke(pipeline, payload)
