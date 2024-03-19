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
    <b>serverless infrastructure for multimodal indexing, retrieving and generation. integrate in one line of code. completely open source. 
    </b>
</h2>

<!-- ![nux Logo](https://nux.com/static/img/logo-dark.png) -->

## Why Bother?

Companies rarely have data that lives in a single location. Not only does it span various location (S3, Snowflake, MongoDB, etc.) but the data also varies in modality (image, video, audio, text).
NUX (New User Experience) is an open source developer framework for consolidating insights across the enterprise, and abstracts it down to 2 lines of code. 

## Quickstart

The guide below use nux's [python client](https://github.com/nux-ai/nux-python). For examples interfacing with the nux api directly, see [examples](/examples).

**Import and initialize the client**

```python
from nuxai import NUX
from pydantic import BaseModel

# init NUX client
nux = NUX("API-KEY")

# create your first collection
collection_id = nux.create_collection(namespace="files.resume")
```

**Configure and initiate the indexing worker**

```python
# Index file urls, raw string, or byte objects. 
index_id = client.index(["https://s3.us-east-2.amazonaws.com/resume.pdf"])

# check the status
index_id.status()

# which returns
{'UPLOADED': 1, 'PROCESSING': 0, 'READY': 0, 'ERROR': 0}
```

**Retrieve results using KNN**

```python
# retrieve the results
results = client.search(query="What was Ethan's first job?")
```

**Generate JSON output using context from KNN results**
```python
# specify json output
class UserModel(BaseModel):
    name: str
    age: int

# generate a response with context from results
generation = client.generate.openai.chat(
    engine="gpt-3.5-turbo",
    response_shape=UserModel,
    context=f"Content from resume: {results}",
    messages=[
        {"role": "user", "content": query},
    ],
)
```

## Folder Structure

nux's architecture is divided into several components, each runs as seperate local web services for ease of use and deployment:

### Parse

Handles the parsing of different file types to make them accessible for further processing.

| FileType | Extensions      |
|----------|-----------------|
| Image    | jpg, png, etc.  |
| Document | pdf, docx, etc. |
| Audio    | mp3, wav, etc.  |

Included parsers:

- **Website Scraper**: Web scraper with recursive `depth` specification.
- **Image**: Object detection, OCR or generating embeddings.
- **Text**: Extracting raw text or metadata from files.
- **Audio**: Transcribing audio or generating embeddings.
- **Video**: Scene detection, object recognition and transcribing.

### API

Provides a set of APIs for interacting with the framework, including:

- **Index**: Creating searchable indexes of the processed data.
- **Chunk**: Breaking down large texts or files into independent chunks.
- **Retrieve**: Query your storage engine of choice
- **Generate**: Generate output based on your LLM of choice.
- **Integrations**: 3rd party integrations for read and write support

### Storage

For securely storing processed data and embeddings. All storage engines support hybrid search (BM25 & KNN).

- **MongoDB (Cloud Only)**: For storing indexed data and metadata.

### Inference

Handles the generation and fine-tuning of content based on the indexed data.

- **Generate**: For generating outputs that adheres to a JSON schema
- **Embed**: Generating embedding based on input


## Roadmap

Future enhancements planned for OSS nux:

- [ ] CDC connection with databases, storage for real-time sync
- [ ] Fine-tuning support for BERT encoders and LoRa adapters.
- [ ] Integration with hybrid databases (Weaviate, Qdrant, and Redis).
- [ ] Multimodal querying & generation
- [ ] Kubernetes deployment options
- [ ] Additional integrations (Google Drive, Box, Dropbox, etc.).
- [ ] Support for more models (both embedding and LLMs).
- [ ] Evaluation tools for index, query, and generate processes.
- [ ] Learn to Rank (LTR) and re-ranking features.


## Managed Version

For those interested in a fully managed hosting solution:

- **Full Dashboard**: Provision collections, A/B test queries, revision history, rollbacks and more
- **Serverless**: For hosting the indexing and querying jobs
- **Monitoring**: Full visibility into indexing, retrieval and generation performance
- **Compliance Checks**: Ensuring that your data handling meets regulatory standards (HIPAA, SOC-2, etc.)
- **Support**: 24 hour SLA 
- **User Management**: Managed OAuth 2.0, SSO, and more
- **Audit and Access History**: Full data lineage and usage history
- **Security**: Private endpoint, network access, and more

### Pricing

- First 10 GB free
- $1.00 per GB per month with discounts for upfront commitments.
