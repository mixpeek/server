[![Python application test with Github Actions](https://github.com/nux-ai/api/actions/workflows/python_app.yaml/badge.svg)](https://github.com/nux-ai/api/actions/workflows/python_app.yaml)

# Project Name

Add a brief description of your project here.

## Setup

Follow these steps to set up the project:

1. **Create a virtual environment**
   ```
   virtualenv venv
   ```

2. **Activate the virtual environment**
   ```
   source venv/bin/activate
   ```

3. **Install the requirements**
   ```
   pip install -r requirements
   ```

4. **Run the local server**
   ```
   uvicorn main:app --reload
   ```
    or
    ```
    python3 -m uvicorn main:app --reload
    ```

Docs are at `/docs`,


### To test webhooks leverage ngrok

`ngrok http http://localhost:8000`


### Alternatively, you can build with Docker

`docker build --platform linux/amd64 -t nux-ai/api:v1 .`

`docker run -p 8000:8000 nux-ai/api:v1`