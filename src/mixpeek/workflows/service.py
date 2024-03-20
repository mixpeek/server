from config import aws, python_version
from bson import ObjectId


from db_internal.service import BaseSyncDBService

from .model import WorkflowCreateRequest, WorkflowResponse
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

        workflow_response = WorkflowResponse(
            success=False, status=500, response=None, error=None, metadata={}
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

        new_workflow.metadata["serverless_function_name"] = function_name
        new_workflow.metadata["serverless_last_edited"] = current_time()

        create_one_response = self.create_one(new_workflow.model_dump())
        create_one_response = self.convert_objectid_to_str(create_one_response)

        workflow_response.status = 200
        workflow_response.success = True
        workflow_response.response = create_one_response

        return workflow_response

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

    def convert_objectid_to_str(self, item):
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    item[key] = str(value)
                elif isinstance(value, dict):
                    item[key] = self.convert_objectid_to_str(value)
        return item
