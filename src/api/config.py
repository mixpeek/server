import os
from dotenv import load_dotenv

load_dotenv()

python_version = os.getenv("PYTHON_VERSION")

# dbs
redis_url = os.getenv("REDIS_URL")
mongo_url = os.getenv("MONGO_URL")

# inference
openai_key = os.getenv("OPENAI_KEY")

parser_url = os.getenv("PARSER_CONTAINER_URL")
storage_url = os.getenv("STORAGE_CONTAINER_URL")
inference_url = os.getenv("INFERENCE_CONTAINER_URL")

log_level = os.getenv("LOG_LEVEL")
