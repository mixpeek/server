from fastapi import APIRouter, HTTPException, Body, Depends, Request
from typing import List, Optional

from utilities.helpers import generate_uuid, current_time

from .model import (
    WorkflowCreateRequest,
    WorkflowMinimalResponse,
    WorkflowSchema,
    QueryParamsSchema,
    WorkflowInvokeResponse,
)
from .service import WorkflowSyncService
from .invoke import invoke_handler

from db_internal.model import PaginationParams

router = APIRouter()


@router.post("/", response_model=WorkflowSchema)
async def create_workflow(
    request: Request,
    workflow_request: WorkflowCreateRequest = Body(...),
    pagination: PaginationParams = Depends(),
):
    workflow_service = WorkflowSyncService(request.index_id)
    return workflow_service.create(workflow_request)


@router.post("/{workflow_id}/invoke", response_model=WorkflowInvokeResponse)
async def run_workflow(
    request: Request,
    workflow_id: str,
    parameters: dict = Body(...),
    websocket_id: Optional[str] = None,
):
    workflow_service = WorkflowSyncService(request.index_id)

    workflow = workflow_service.get(workflow_id)
    if not workflow:
        raise HTTPException(
            status_code=404, detail=f"Workflow {workflow_id} not found."
        )
    if workflow.get("metadata", {}).get("serverless_function_name") is None:
        raise HTTPException(
            status_code=400,
            detail=f"Workflow {workflow_id} has no serverless function.",
        )

    # run invokation
    result = await invoke_handler(
        serverless_name=workflow["metadata"]["serverless_function_name"],
        run_id=generate_uuid(),
        websocket_id=websocket_id,
        request_parameters=parameters,
    )

    workflow_service.update(workflow_id, {"last_run": current_time()})

    return result


# @router.get('/', response_model=List[WorkflowMinimalResponse])
# def list_workflows(
#     request: Request,
#     pagination: PaginationParams = Depends()
# ):

#     wb_service = WorkflowSyncService(
#         index_id,
#         version_id="latest",
#         scope=scope
#     )
#     try:
#         return wb_service.list(limit=pagination.limit, offset=pagination.offset)
#     except:
#         raise HTTPException(status_code=400, detail="Couldn't list workbooks.")


# @router.get("/{workflow_id}")
# async def get_workflow(
#     request: Request,
# ):

#     return {"message": "Listener created"}


# @router.put("/{workflow_id}")
# async def update_workflow(
#     request: Request,
# ):

#     return {"message": "Listener created"}


# @router.delete("/{workflow_id}")
# async def delete_workflow(
#     request: Request,
# ):
#     return {"message": "Listener created"}
