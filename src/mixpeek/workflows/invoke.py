from cloud_services.aws.serverless import AsyncLambdaClass
import time


async def invoke_handler(serverless_name, run_id, websocket_id, request_parameters):
    async_lambda_client = AsyncLambdaClass()
    response_object = {
        "response": None,
        "error": None,
        "status": 500,
        "success": False,
        "metadata": {},
    }
    try:
        print("Running function!")
        start_time = time.time() * 1000
        response = await async_lambda_client.invoke(
            serverless_name,
            request_parameters,
        )
        response_object["response"] = response
        response_object["status"] = 200
        response_object["success"] = True
        response_object["metadata"]["elapsed_time"] = (time.time() * 1000) - start_time

    except Exception as e:
        response_object["error"] = f"Error running lambda: {e}"

    return response_object
