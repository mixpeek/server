from cloud_services.aws.serverless import AsyncLambdaClass
import time
from _exceptions import InternalServerError


async def invoke_handler(serverless_name, run_id, websocket_id, request_parameters):
    async_lambda_client = AsyncLambdaClass()

    try:
        response = await async_lambda_client.invoke(
            serverless_name,
            request_parameters,
        )
        return response
    except Exception as e:
        raise InternalServerError(error={"message": "Failed to invoke function"})
