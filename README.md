<p align="center">
  <img height="60" src="https://mixpeek.com/static/img/logo-dark.png" alt="Mixpeek Logo">
</p>
<p align="center">
<strong><a href="https://mixpeek.com/start">Sign Up</a> | <a href="https://docs.mixpeek.com/">Documentation</a> | <a href="https://mixpeek.com/start">Email List</a> | <a href="https://join.slack.com/t/mixpeek/shared_invite/zt-2edc3l6t2-H8VxHFAIl0cnpqDmyFGt0A">Slack</a>
</strong>
</p>

<p align="center">
    <a href="https://github.com/mixpeek/mixpeek-python/stargazers">
        <img src="https://img.shields.io/github/stars/mixpeek/mixpeek-python.svg?style=flat&color=yellow" alt="Github stars"/>
    </a>
    <a href="https://github.com/mixpeek/mixpeek-python/issues">
        <img src="https://img.shields.io/github/issues/mixpeek/mixpeek-python.svg?style=flat&color=success" alt="GitHub issues"/>
    </a>
    <a href="https://join.slack.com/t/mixpeek/shared_invite/zt-2edc3l6t2-H8VxHFAIl0cnpqDmyFGt0A">
        <img src="https://img.shields.io/badge/slack-join-green.svg?logo=slack" alt="Join Slack"/>
    </a>
</p>

<h2 align="center">
    <b>real-time multi-modal vector embedding pipeline. set and forget. 
    </b>
</h2>

## Overview

Mixpeek automatically listens in on database changes, processes your files, and generates embeddings to send right back into your database.

It removes the need of setting up architecture to track database changes, extracting content, processing and embedding it. This stuff doesn't move the needle in your business, so why focus on it?

We support every modality: **documents, images, video, audio and of course text.**

### Integrations

- [MongoDB Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search)
- [Supabase](https://supabase.com/vector)

## Architecture

Mixpeek is structured into two main services, each designed to handle a specific part of the process:

- **API (Orchestrator)**: Coordinates the flow between services, ensuring smooth operation and handling failures gracefully.
- **Listener**: Monitors the database for specified changes, triggering the process when changes are detected.
- **Services**: Loads and parses the changed files, preparing them for processing (supports image, video audio and text)
- **Inference**: Processes the parsed data, generating embeddings that can then be integrated back into the database.

These services are containerized and can be deployed on separate servers for optimal performance and scalability.

## Getting Started

### Installation

Clone the Mixpeek repository and navigate to the SDK directory:

```bash
git clone git@github.com:mixpeek/server.git
cd server
```

First, build the Docker image:

```bash
docker build -t my-app .
```

Then, run the application using Docker Compose:

```bash
docker-compose up
```

### Configuration and Usage

Configure each service with your environment's specifics. Here's an illustrative setup:

```bash
pip install mixpeek
```

init our client
```python
from mixpeek import Mixpeek

mixpeek = Mixpeek("API-KEY") # if using localhost, you'll need to create one locally.
```

### Parse
```python
# grab a url

corpus = mixpeek.parse.text.extract("ethan-resume.pdf")

json.dumps(resp, indent=2)
```

### Generate
First we define our schema, then send it to the client alongside our corpus from above.
```python
class CompanyDetails(BaseModel):
    company_name: str

class OutputSchema(BaseModel):
    company_details: List[CompanyDetails]

output = mixpeek.generate.openai.chat(
    model="gpt-4",
    response_format=OutputSchema,
    context=f"format this document and make sure to respond and adhere to the provided JSON format: {corpus}",
    settings={"temperature": 1},
)
```

## Index
You can also setup automated indexing workflows (WIP)
```python
mixpeek.listen("mongodb://hostname", output_schema=OutputSchema)
```


#### Are we missing anything?

- Email: ethan@mixpeek.com
- Meeting: https://mixpeek.com/contact

