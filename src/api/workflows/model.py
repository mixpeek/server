from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from utilities.helpers import unique_name, generate_uuid, current_time


class QueryParamsSchema(BaseModel):
    parameters: dict


class WorkflowSettings(BaseModel):
    requirements: Optional[List[str]] = Field(default_factory=list)
    python_version: Optional[str] = "python3.10"


class WorkflowSchema(BaseModel):
    index_id: str
    created_at: datetime
    last_run: Optional[datetime]
    workflow_id: str
    workflow_name: Optional[str]
    metadata: Optional[dict] = {}
    settings: WorkflowSettings


class WorkflowCreateRequest(BaseModel):
    workflow_id: Optional[str] = Field(
        default_factory=lambda: generate_uuid(length=15, dashes=False)
    )
    code_as_string: str
    metadata: Optional[dict] = {}
    settings: WorkflowSettings
    workflow_name: Optional[str] = Field(default_factory=unique_name)
    last_run: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: current_time())


class WorkflowResponse(BaseModel):
    workflow_id: str
    workflow_name: Optional[str]
    created_at: datetime
    metadata: Optional[dict] = {}


# class WorkflowInvokeResponse(BaseModel):
#     response: dict
