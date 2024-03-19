import requests
import json


def parse(file_url):
    url = "http://localhost:8001/file"

    payload = json.dumps({"file_url": file_url})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def embed(contents):
    url = "http://0.0.0.0:8003/embed"

    payload = json.dumps({"input": contents})
    headers = {"Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def insert(obj):
    url = "http://0.0.0.0:8000/storage"

    payload = json.dumps(obj)
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


# do dag here (this triggers from /listener via a message queue or CDC or webhook)
results = parse(
    "https://athena-web-app-public-assets.s3.amazonaws.com/nux-tmp/R46947.pdf"
)

for result in results["response"]:
    embedding = embed(result["text"])
    result["embedding"] = embedding["response"]["embedding"]
    insert(result)
