from fastapi import APIRouter, Body, Depends, Request
from typing import List, Optional
from _exceptions import BadRequestError, InternalServerError, NotFoundError


from utilities.helpers import generate_uuid, current_time
from utilities.code import CodeValidation

from .model import (
    WorkflowCreateRequest,
    WorkflowSchema,
    WorkflowResponse,
)
from .service import WorkflowSyncService
from .invoke import invoke_handler

from db.model import PaginationParams

router = APIRouter()


@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    request: Request,
    workflow_request: WorkflowCreateRequest = Body(...),
    pagination: PaginationParams = Depends(),
):
    try:
        workflow_service = WorkflowSyncService(request.index_id)
        return workflow_service.create(workflow_request)
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)


@router.post("/{workflow_id}/invoke", response_model=WorkflowResponse)
async def run_workflow(
    request: Request,
    workflow_id: str,
    parameters: dict = Body(...),
    websocket_id: Optional[str] = None,
):
    try:
        workflow_service = WorkflowSyncService(request.index_id)

        workflow = workflow_service.get(workflow_id)
        if not workflow:
            raise NotFoundError(error={"message": f"Workflow {workflow_id} not found."})
        if workflow.get("metadata", {}).get("serverless_function_name") is None:
            raise BadRequestError(
                error={"message": f"Workflow {workflow_id} has no serverless function."}
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
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)


@router.get("/code", response_model=WorkflowResponse)
def convert_code_to_string(code: str = Body(...)):
    try:
        return WorkflowResponse(
            success=True,
            status=200,
            response={"code_as_string": code},
            error=None,
            metadata=None,
        )
    except BadRequestError as e:
        raise BadRequestError(error=e.error)
    except NotFoundError as e:
        raise NotFoundError(error=e.error)
    except InternalServerError as e:
        raise InternalServerError(error=e.error)
