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
parser_url = os.getenv("PARSER_CONTAINER_URL")
listener_url = os.getenv("LISTENER_CONTAINER_URL")
inference_url = os.getenv("INFERENCE_CONTAINER_URL")

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

# local configs
auth_off = os.getenv("AUTH_OFF", "False").lower() in ["true", "1"]
