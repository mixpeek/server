## Docker Commands:

docker build --platform linux/amd64 -t mixpeek/mixpeek-services:latest .

<!-- docker run -p 8001:8001 nux/nux-server-parse:latest -->

## Run without docker:

pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8001

nux-server-parse-latest:8001

## push to gh

docker tag mixpeek/mixpeek-services:latest ghcr.io/mixpeek/mixpeek-services:latest

docker push ghcr.io/mixpeek/mixpeek-services:latest
