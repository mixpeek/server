<img width="326" alt="Group 311 (2)" src="https://mixpeek.com/static/img/logo-light.png">

# Multimodal RAG Framework
---

Mixpeek is an open source framework for chunking, indexing, embedding, querying, generating, and fine-tuning RAG (Retrieval Augmented Generation) pipelines. 

It supports video, audio, image and text files and is built to be extensible for any data source and model.

**Import and initialize the client**

```python
from mixpeek import Mixpeek
from pydantic import BaseModel

# initiatlize mixpeek client using a collection_id tenant
collection_id = "1"
client = Mixpeek(
    collection_id="1",
    engine="mongodb",
    connection={
        "connection_string": "mongodb+srv://username:password@hostname",
        "database": "files",
        "collection": "resumes",
    },
    embedding_model={
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "version": "latest",
    },
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
    input=["https://nux-sandbox.s3.us-east-2.amazonaws.com/marketing/ethan-resume.pdf"],
    chunker={
        "method": "character",
        "length": 1000,
        "seperator": "\n\n",
        "chunk_overlap": 100,
    },
    data_model={
        "model": StorageModel,
        "fields_to_embed": ["raw_content"],
        "embed_suffix": "embedding_field",
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
    query=[
        {
            "$vectorSearch": {
                "index": "default",
                "path": f"{StorageModel.raw_content}.embedding_field",
                "queryVector": embedding,
                "numCandidates": 150,
                "limit": 10,
                "filter": {
                    "$gt": {"collection_id": collection_id, "index_id": index_id}
                },
            }
        }
    ],
)
```

**Generate JSON output using context from KNN results**
```python
# specify json output
class UserModel(BaseModel):
    name: str
    age: int


# generate a response with context from results
generation = client.openai.chat.generate(
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

### Storage

For securely storing processed data and embeddings. All storage engines support hybrid search (BM25 & KNN).

- **MongoDB (Cloud Only)**: For storing indexed data and metadata.

### Inference

Handles the generation and fine-tuning of content based on the indexed data.

- **Generate**: For generating outputs that adheres to a JSON schema
- **Embed**: Generating embedding based on input

### Integrations

Connectors for various platforms that supports read and write

- Monday.com
- AWS S3

## Roadmap

Future enhancements planned for Mixpeek:

- [ ] Fine-tuning support for BERT encoders and LoRa adapters.
- [ ] Integration with OSS hybrid databases (Weaviate, Qdrant, and Redis).
- [ ] Multimodal querying
- [ ] Multimodal generation
- [ ] Kubernetes deployment options
- [ ] Additional integrations (Google Drive, Box, Dropbox, etc.).
- [ ] Support for more models (both for embedding and LLMs).
- [ ] Indexing version control.
- [ ] Evaluation tools for index, query, and generate processes.
- [ ] Learning to Rank (LTR) and re-ranking features.


## Public Cloud

For those interested in a fully managed hosting solution:

- **Pricing**: $.10 per GB per month with discounts for upfront commitments.
- **Monitoring**: Full visibility into indexing, retrieval and generation performance
- **UI Control Panel**: For easy management of your deployment and usage.
- **Compliance Checks**: Ensuring that your data handling meets regulatory standards (HIPAA, SOC-2, etc.)
- **Support**: 24 hour SLA 
- **User Management**: Managed OAuth 2.0 
- **Audit and Access History**: Full data lineage and usage history
- **Security**: Private endpoint, network access, and more
