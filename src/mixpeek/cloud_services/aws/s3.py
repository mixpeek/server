from urllib.parse import quote
import boto3
import json
from config import aws as creds
import io
import os
import requests

from _exceptions import BadRequestError


class S3Class:
    def __init__(self, bucket_name='nux-runs'):
        self.session = boto3.Session(
            aws_access_key_id=creds['aws_access_key'],
            aws_secret_access_key=creds['aws_secret_key'],
            region_name=creds['region']
        )
        self.bucket_name = bucket_name
        self.region = creds['region']
        self.client = self.session.client('s3')

    def upload(self, in_memory_file, file_name):
        try:
            response = self.client.put_object(
                Body=in_memory_file.getvalue(),
                Bucket=self.bucket_name,
                Key=file_name
            )
            return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_name}"

        except Exception as e:
            raise BadRequestError(str(e))

    def list(self):
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket_name)
            return response.get('Contents', [])

        except Exception as e:
            raise BadRequestError(str(e))

    def delete(self, key):
        try:
            response = self.client.delete_object(
                Bucket=self.bucket_name, Key=key)
            return response

        except Exception as e:
            raise BadRequestError(str(e))

    def download(self, key):
        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()

        except Exception as e:
            raise BadRequestError(str(e))
