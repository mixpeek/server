import os
from dotenv import load_dotenv

load_dotenv()

python_version = os.getenv("PYTHON_VERSION")
log_level = os.getenv("LOG_LEVEL")

# dbs
redis_url = os.getenv("REDIS_URL")
mongo_url = os.getenv("MONGO_URL")

# inference
openai_key = os.getenv("OPENAI_KEY")

# containers
services_url = os.getenv("SERVICES_CONTAINER_URL")

# cloud
mongodb_atlas = {
    "public_key": os.getenv("MONGODB_PUBLIC_KEY"),
    "private_key": os.getenv("MONGODB_PRIVATE_KEY"),
    "group_id": os.getenv("MONGODB_GROUP_ID"),
}

aws = {
    "access_key": os.getenv("AWS_ACCESS_KEY"),
    "secret_key": os.getenv("AWS_SECRET_KEY"),
    "region": os.getenv("AWS_REGION"),
    "arn_lambda": os.getenv("AWS_ARN_LAMBDA"),
}

unstructured_api_key = os.getenv("UNSTRUCTURED_API_KEY")
unstructured_api_url = os.getenv("UNSTRUCTURED_API_URL")

# local configs
server_env = os.getenv("SERVER_ENV")

sentry_dsn = os.getenv("SENTRY_DSN")
