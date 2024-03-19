from fastapi import HTTPException
from config import aws, python_version

from db_internal.service import BaseSyncDBService

from .model import WorkflowCreateRequest
from .utilities import CodeHandler

from _exceptions import InternalServerError


from utilities.helpers import generate_function_name, current_time


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
        # code_handler._validate_code()

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

        new_workflow.metadata["serverless_function_name"] = function_name
        new_workflow.metadata["serverless_last_edited"] = current_time()

        return self.create_one(new_workflow.model_dump())

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
