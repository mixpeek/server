uvicorn main:app --reload --host 8001

## Docker Commands:

docker build --platform linux/amd64 -t mixpeek/parse:latest .

docker run -p 8001:8001 nux-ai/worker:latest