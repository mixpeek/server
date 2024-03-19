<p align="center">
  <img height="60" src="https://nux.ai/static/img/brand/nux_logo_dark.png" alt="NUX Logo">
</p>
<p align="center">
<strong><a href="https://docs.nux.ai/">Documentation</a> | <a href="https://www.nux.ai/newsletter-signup/">Email List</a>
</strong>
</p>

<p align="center">
    <a href="https://github.com/nux-ai/server/stargazers">
        <img src="https://img.shields.io/github/stars/nux-ai/server.svg?style=flat&color=yellow" alt="Github stars"/>
    </a>
    <a href="https://github.com/nux-ai/server/issues">
        <img src="https://img.shields.io/github/issues/nux-ai/server.svg?style=flat&color=success" alt="GitHub issues"/>
    </a>
    <a href="https://join.slack.com/t/nuxai/shared_invite/zt-2efp37o7q-FDyH3LFPkeOsc9Vi_Q6ZEA">
        <img src="https://img.shields.io/badge/slack-join-green.svg?logo=slack" alt="Join Slack"/>
    </a>
</p>

<h2 align="center">
    <b>real-time multi-modal vector embedding pipeline. set and forget. 
    </b>
</h2>

## Overview

NUX automatically listens in on database changes, processes your files, and generates embeddings to send right back into your database.

It removes the need of setting up architecture to track database changes, extracting content, processing and embedding it. This stuff doesn't move the needle in your business, so why focus on it?

### Integrations

- [MongoDB Vector Search](https://www.mongodb.com/products/platform/atlas-vector-search)
- [Supabase](https://supabase.com/vector)

## Services Architecture

NUX is structured into four main services, each designed to handle a specific part of the process:

- **API (Orchestrator)**: Coordinates the flow between services, ensuring smooth operation and handling failures gracefully.
- **Listener**: Monitors the database for specified changes, triggering the process when changes are detected.
- **Parser**: Loads and parses the changed files, preparing them for processing (supports image, video audio and text)
- **Embedder**: Processes the parsed data, generating embeddings that can then be integrated back into the database.

These services are containerized and can be deployed on separate servers for optimal performance and scalability.

## Getting Started

### Installation

Clone the NUX repository and navigate to the SDK directory:

```bash
git clone git@github.com:nux-ai/server.git
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

```python
# Listener Service Configuration

listen_settings = {
    "connection": {
        "engine": "mongodb",
        "dbname": "your_db_name",
        "user": "your_db_user",
        "password": "your_db_password",
        "host": "your_db_host",
        "port": 5432
    },
    "table_name": "my_table_name"
    "filters": {
        "status": "processing"
    },
    "embedding": {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "field": "file_id"
    }
}
```

Now let's setup our listener
```python
# the schema you'd like the insert to adhere to
class InsertSchema:
    file_id: str
    embedding: list
    contents: str

from nuxai import NUX

# add your internal key (or cloud if you're using our managed service)
nux = NUX("INTERNAL-API-KEY")

# add the db to your organization, it's encrypted don't worry
collection_id = nux.add_db(LISTENER_DB_CONFIG)

# now listen in on changes, that's it! 
listener_id = nux.listen(collection_id, listen_settings)f
```

We can even poll for status of our listener:

```python
nux.listener.status(listener_id)

{'ACTIVE': True, 'PROCESSING': 0, 'READY': 0, 'ERROR': 0}
```


#### Are we missing anything?

- Email: ethan@nux.ai
- Meeting: https://nux.ai/contact

