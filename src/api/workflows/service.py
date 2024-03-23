from config import aws, python_version
from bson import ObjectId


from db.service import BaseSyncDBService

from .model import WorkflowCreateRequest, WorkflowResponse
from .utilities import CodeHandler

from utilities.helpers import (
    convert_objectid_to_str,
    generate_function_name,
    current_time,
)
from utilities.methods import create_success_response

from _exceptions import InternalServerError, NotFoundError, BadRequestError


class WorkflowSyncService(BaseSyncDBService):
    def __init__(self, index_id):
        super().__init__("workflows", index_id)

    def create(self, workflow_request):
        # init workflow class
        new_workflow = WorkflowCreateRequest(
            code_as_string=workflow_request.code_as_string,
            metadata=workflow_request.metadata,
            settings=workflow_request.settings,
            workflow_name=workflow_request.workflow_name,
        )

        # create unique name for lambda function
        function_name = generate_function_name(
            self.index_id, new_workflow.workflow_id, new_workflow.workflow_name
        )

        # check for code security and function
        code_handler = CodeHandler(
            self.index_id,
            new_workflow.workflow_id,
            new_workflow.code_as_string,
            function_name,
        )

        # upload to s3
        response = code_handler._create_zip_package(
            new_workflow.settings.requirements,
            new_workflow.settings.python_version,
        )

        if response["status"] == "error":
            raise InternalServerError(response["error"])

        s3_dict = response["response"]

        # create lambda function
        code_handler.create_lambda_function(s3_dict["bucket"], s3_dict["key"])

        # update metadata
        new_workflow.metadata["serverless_function_name"] = function_name
        new_workflow.metadata["serverless_last_edited"] = current_time()

        # add to DB
        db_response = self.create_one(new_workflow.model_dump())

        # prepare response
        workflow_response = {
            "workflow_id": new_workflow.workflow_id,
            "workflow_name": new_workflow.workflow_name,
            "created_at": new_workflow.created_at.isoformat(),
            "metadata": {
                "serverless_function_name": new_workflow.metadata[
                    "serverless_function_name"
                ],
                "serverless_last_edited": new_workflow.metadata[
                    "serverless_last_edited"
                ].isoformat(),
            },
        }

        return create_success_response(workflow_response)

    def get_and_validate(self, workflow_id):
        workflow = self.get(workflow_id)
        if not workflow:
            raise NotFoundError(error={"message": f"Workflow {workflow_id} not found."})
        if workflow.get("metadata", {}).get("serverless_function_name") is None:
            raise BadRequestError(
                error={"message": f"Workflow {workflow_id} has no serverless function."}
            )
        return workflow

    def list(self, lookup_conditions=None, limit=None, offset=None):
        if lookup_conditions is None:
            lookup_conditions = {}
        """List workbooks with pagination."""
        results = self.list_by_index(lookup_conditions, limit, offset)
        return results

    def get(self, workflow_id):
        """Get a single workflow by ID."""
        return self.get_one({"workflow_id": workflow_id})

    def update(self, workflow_id, updated_data):
        """Update a single workflow by ID."""
        lookup_conditions = {"workflow_id": workflow_id}
        return self.update_one(lookup_conditions, updated_data)
