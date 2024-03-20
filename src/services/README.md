## Docker Commands:

docker build --platform linux/amd64 -t nux/nux-server-parse:latest .

docker run -p 8001:8001 nux/nux-server-parse:latest

## Run without docker:

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8001

nux-server-parse-latest:8001

## push to gh

docker tag nux/nux-server-parse:latest ghcr.io/nux-ai/nux-server-parse:latest

docker push ghcr.io/nux-ai/nux-server-parse:latest
