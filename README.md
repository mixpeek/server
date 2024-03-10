[![Slack](https://img.shields.io/badge/slack-@mixpeek/dev-green.svg?logo=slack)](https://join.slack.com/t/mixpeek/shared_invite/enQtNjQxMzgyNTEzNzk1LTU0ZjZlZmY5ODdkOTEzZDQzZWU5OTk3ZTgyNjY1ZDE1M2U1ZTViMWQxMThiMjU1N2MwOTlhMmVjYjEzMjEwMGQ)
 **[Docs](https://docs.mixpeek.com/)** | **[Free account](https://dashboard.mixpeek.com)** | **[Email list](https://www.mixpeek.com/newsletter-signup/)**


<p align="center">
    <img src ="https://mixpeek.com/static/img/logo-dark.png"
     width="250"/>
         </p>

### Integrate a fully extensible RAG pipeline in minutes 

---

Mixpeek is an open source framework for chunking, indexing, embedding, querying, generating, and fine-tuning RAG (Retrieval Augmented Generation) pipelines. 

It supports video, audio, image and text files is extremely simple to use and is built to be extensible for any data source and model.

**Import and initialize the client**

```python
from mixpeek import Mixpeek
from pydantic import BaseModel

# initiatlize mixpeek client using a collection_id tenant
client = Mixpeek(
    collection_id="1",
    connection={
        "storage": "mongodb",
        "connection_string": "mongodb+srv://username:password@hostname",
        "database": "files",
        "collection": "resumes",
    },
    embedding_model={
        "name": "all-MiniLM-L6-v2",
        "version": "latest",
    },  # optional
    embed_suffix="embedding",  # optional
)
```

**Configure and initiate the indexing worker**

```python
# Define how you'd like to index the content
class StorageModel(BaseModel):
    file_metadata: dict
    raw_content: str


# Index file urls, raw string, or byte objects. Returns a unique id for the index.
index_id = client.index(
    input=[
        "https://nux-sandbox.s3.us-east-2.amazonaws.com/marketing/ethan-resume.pdf"
    ],  # one or the other (existing db)
    # input={
    #     "filter": {"collection_id": "1"},
    #     "upsert": True,
    # }
    data_model={
        "schema": StorageModel.to_dict(),  # optional
        "fields_to_embed": [
            "raw_content",
            "file_metadata.name",
        ],  # these are placed beside them?
        "metadata": {
            "name": "Ethan's Resume",
        },
    },
)
```

**Retrieve results using KNN**

```python
# Generate embedding
query = "What was Ethan's first job?"
embedding = client.embed(input=query)

# retrieve the results
results = client.retrieve(
    query={
        "file_metadata.embedding": query,  # detect if embedding is in it
        "file_metadata.name": "Ethan's Resume",
    },
    filters={"collection_id": "1"},
)
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

Mixpeek's architecture is divided into several components, each runs as seperate local web services for ease of use and deployment:

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

Future enhancements planned for OSS Mixpeek:

- [ ] Fine-tuning support for BERT encoders and LoRa adapters.
- [ ] Integration with hybrid databases (Weaviate, Qdrant, and Redis).
- [ ] Multimodal querying & generation
- [ ] Kubernetes deployment options
- [ ] Additional integrations (Google Drive, Box, Dropbox, etc.).
- [ ] Support for more models (both embedding and LLMs).
- [ ] Evaluation tools for index, query, and generate processes.
- [ ] Learn to Rank (LTR) and re-ranking features.


## Public Cloud

For those interested in a fully managed hosting solution:

- **Full Dashboard**: Provision collections, A/B test queries, revision history, rollbacks and more
- **Monitoring**: Full visibility into indexing, retrieval and generation performance
- **Compliance Checks**: Ensuring that your data handling meets regulatory standards (HIPAA, SOC-2, etc.)
- **Support**: 24 hour SLA 
- **User Management**: Managed OAuth 2.0, SSO, and more
- **Audit and Access History**: Full data lineage and usage history
- **Security**: Private endpoint, network access, and more

### Pricing

$1.00 per GB per month with discounts for upfront commitments.
