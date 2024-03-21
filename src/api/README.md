[![Python application test with Github Actions](https://github.com/nux-ai/api/actions/workflows/python_app.yaml/badge.svg)](https://github.com/nux-ai/api/actions/workflows/python_app.yaml)

# Project Name

Add a brief description of your project here.

## Setup
We use poetry for dependency management. Make sure to install it first before proceeding.
Poetry Installation: https://python-poetry.org/docs/

Follow these steps to set up the project:

1. **Create a virtual environment**
   ```
   poetry env use python3.10
   ```

2. **Activate the virtual environment**
   ```
   poetry shell
   ```

3. **Install the requirements**
   ```
   poetry install
   ```

4. **Run the local server**
   ```
   poetry run uvicorn main:app --reload
   ```
    or
    ```
    poetry run python3 -m uvicorn main:app --reload
    ```

Docs are at `/docs`,


### To test webhooks leverage ngrok 

`ngrok http http://localhost:8000`


## Docker Commands:

docker build --platform linux/amd64 -t mixpeek/mixpeek-api:latest .

docker run -p 8000:8000 mixpeek/mixpeek-api:latest


## push to gh

docker tag mixpeek/mixpeek-api:latest ghcr.io/mixpeek/mixpeek-api:latest

docker push ghcr.io/mixpeek/mixpeek-api:latest
