from urllib.parse import quote
import boto3
import aioboto3
import json
from config import aws as creds
import io
import os
import requests

from fastapi import HTTPException


class AsyncLambdaClass:
    def __init__(self, timeout=900, memory_size=1024):
        self.session = aioboto3.Session(
            aws_access_key_id=creds["access_key"],
            aws_secret_access_key=creds["secret_key"],
            region_name=creds["region"],
        )

    async def invoke(self, function_name, payload):
        async with self.session.client("lambda") as client:
            response = await client.invoke(
                FunctionName=function_name,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )
            response_payload = await response["Payload"].read()
            return json.loads(response_payload)


class LambdaClass:
    def __init__(
        self,
        timeout=60,
        memory_size=1024,
        role=creds["arn_lambda"],
    ):
        self.session = boto3.Session(
            aws_access_key_id=creds["access_key"],
            aws_secret_access_key=creds["secret_key"],
            region_name=creds["region"],
        )
        self.role = role
        self.timout = timeout
        self.memory_size = memory_size
        self.client = self.session.client("lambda")
        self.layer_arns = [
            # "arn:aws:lambda:us-east-2:770693421928:layer:Klayers-p310-Pillow:5",
            # "arn:aws:lambda:us-east-2:770693421928:layer:Klayers-p310-openpyxl:1",
            # "arn:aws:lambda:us-east-2:770693421928:layer:Klayers-p310-requests:7"
        ]

    def create_with_s3(self, runtime, function_name, s3_bucket, s3_key, tags={}):
        try:
            response = self.client.create_function(
                FunctionName=function_name,
                Runtime=runtime,
                Role=self.role,
                Handler=f"{function_name}.function",
                Code={"S3Bucket": s3_bucket, "S3Key": s3_key},
                Timeout=self.timout,
                MemorySize=self.memory_size,
                Tags=tags,
                Layers=self.layer_arns,
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_with_s3(self, function_name, s3_bucket, s3_key):
        try:
            response = self.client.update_function_code(
                FunctionName=function_name, S3Bucket=s3_bucket, S3Key=s3_key
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update(self, function_name, in_memory_zip):
        try:
            response = self.client.update_function_code(
                FunctionName=function_name, ZipFile=in_memory_zip.getvalue()
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def run(self, payload, function_name):
        try:
            response = self.client.invoke(
                FunctionName=function_name,
                InvocationType="RequestResponse",
                Payload=json.dumps(payload),
            )

            response_payload = json.loads(response["Payload"].read())

            return response_payload

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def delete(self, function_name):
        try:
            response = self.client.delete_function(FunctionName=function_name)
            return response

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_function_details(self, function_name):
        try:
            response = self.client.get_function(FunctionName=function_name)
            return response
        except self.client.exceptions.ResourceNotFoundException:
            return False

    def get_function_code(self, lambda_metadata):
        try:
            code_url = lambda_metadata["Code"]["Location"]

            resp = requests.get(code_url)
            function_code = resp.content

            return function_code, code_url

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list(self):
        response = self.client.list_functions()
        return response["Functions"]

    def create_layer(self, layer_name, s3_bucket, s3_key):
        try:
            response = self.client.publish_layer_version(
                LayerName=layer_name,
                Content={"S3Bucket": s3_bucket, "S3Key": s3_key},
                CompatibleRuntimes=["python3.10"],
            )
            return response

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_layers(self):
        try:
            response = self.client.list_layers()
            return response["Layers"]

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
