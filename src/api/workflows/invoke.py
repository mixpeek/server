from cloud_services.aws.serverless import AsyncLambdaClass
import time
from _exceptions import BadRequestError, InternalServerError


async def invoke_handler(serverless_name, run_id, websocket_id, request_parameters):
    async_lambda_client = AsyncLambdaClass()

    try:
        response = await async_lambda_client.invoke(
            serverless_name,
            request_parameters,
        )
        if not response.get("success"):
            raise BadRequestError(error=response.get("error"))
        else:
            return response

    except Exception as e:
        raise BadRequestError(error=response.get("error"))
