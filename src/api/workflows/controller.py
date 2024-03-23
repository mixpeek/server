from fastapi import APIRouter, Body, Depends, Request
from typing import List, Optional

from _exceptions import route_exeception_handler


from utilities.helpers import generate_uuid, current_time
from utilities.methods import create_success_response
from utilities.code import CodeValidation

from .model import WorkflowCreateRequest, WorkflowSchema, WorkflowResponse
from .service import WorkflowSyncService
from .invoke import invoke_handler

from db.model import PaginationParams

router = APIRouter()


@router.post("/", response_model=WorkflowResponse)
@route_exeception_handler
async def create_workflow(
    request: Request,
    workflow_request: WorkflowCreateRequest = Body(...),
    pagination: PaginationParams = Depends(),
):
    workflow_service = WorkflowSyncService(request.index_id)
    return workflow_service.create(workflow_request)


@router.post("/{workflow_id}/invoke")
@route_exeception_handler
async def run_workflow(
    request: Request,
    workflow_id: str,
    parameters: dict = Body(...),
    websocket_id: Optional[str] = None,
):

    workflow_service = WorkflowSyncService(request.index_id)
    workflow = workflow_service.get_and_validate(workflow_id)

    # run invokation
    result = await invoke_handler(
        serverless_name=workflow["metadata"]["serverless_function_name"],
        run_id=generate_uuid(),
        websocket_id=websocket_id,
        request_parameters=parameters,
    )

    workflow_service.update(workflow_id, {"last_run": current_time()})

    return result


@router.get("/code", response_model=WorkflowResponse)
@route_exeception_handler
def convert_code_to_string(code: str = Body(...)):
    return create_success_response({"code_as_string": code})
