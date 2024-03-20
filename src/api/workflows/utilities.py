from cloud_services.aws.serverless import LambdaClass

from utilities.code import CodeValidation
from utilities.zipper import PackageZipper

from _exceptions import BadRequestError


class CodeHandler:
    def __init__(self, index_id, workflow_id, code_as_string=None, function_name=None):
        self.index_id = index_id
        self.workflow_id = workflow_id
        self.code_as_string = code_as_string
        self.function_name = function_name
        self.lambda_client = LambdaClass()

    def _validate_code(self):
        # check security
        if not CodeValidation.check_code_security(self.code_as_string):
            raise BadRequestError(
                error={
                    "message": "Code contains security issues, contact info@nux.ai for help"
                }
            )
        # check for function
        CodeValidation.check_for_function(self.code_as_string)

    def _create_zip_package(
        self,
        requirements=[],
        python_version="python3.10",
    ):
        self.python_version = python_version
        self.requirements = requirements

        obj = {
            "function_name": self.function_name,
            "code_as_string": self.code_as_string,
            "requirements": self.requirements,
            "python_version": self.python_version,
        }
        try:
            zipper = PackageZipper(obj)
            # {"bucket": "nux-code-packages", "key": "packages/2021-07-20/1626791533.zip}
            resp = zipper.get_s3_url()
            if resp["status"] == "error":
                raise BadRequestError(error={"message": resp["message"]})
            return resp

        except Exception as e:
            raise BadRequestError(error={"message": "Couldn't create package"})

    def _check_if_lambda_exists(self):
        if self.lambda_client.get_function_details(self.function_name):
            raise BadRequestError(error={"message": "Function already exists"})

    def create_lambda_function(self, bucket, key):
        # check if the name already exists
        self._check_if_lambda_exists()

        # create new lambda function
        return self.lambda_client.create_with_s3(
            runtime=self.python_version,
            function_name=self.function_name,
            s3_bucket=bucket,
            s3_key=key,
            tags={
                "Context": "Workflow",
                "IndexId": self.index_id,
                "WorkflowId": self.workflow_id,
            },
        )
