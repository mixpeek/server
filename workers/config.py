import os
from dotenv import load_dotenv

load_dotenv()

aws = {
    "s3_bucket": os.getenv("S3_BUCKET"),
    "aws_access_key": os.getenv("AWS_ACCESS_KEY"),
    "aws_secret_key": os.getenv("AWS_SECRET_KEY"),
    "region": os.getenv("AWS_REGION"),
}


unstructured = {
    "api_key": os.getenv("UNSTRUCTURED_API_KEY"),
    "url": os.getenv("UNSTRUCTURED_URL"),
}
