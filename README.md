[![Slack](https://img.shields.io/badge/slack-@mixpeek/dev-green.svg?logo=slack)](https://join.slack.com/t/mixpeek/shared_invite/zt-2edc3l6t2-H8VxHFAIl0cnpqDmyFGt0A)
 **[Docs](https://docs.mixpeek.com/)** | **[Free account](https://dashboard.mixpeek.com)** | **[Email list](https://www.mixpeek.com/newsletter-signup/)**


<p align="center">
    <img src ="https://mixpeek.com/static/img/logo-dark.png"
     width="250"/>
         </p>

### Integrate a fully extensible RAG pipeline in minutes 

---

Mixpeek is an open source framework for chunking, indexing, embedding, querying, generating, and fine-tuning RAG (Retrieval Augmented Generation) pipelines. 

It supports video, audio, image and text files is extremely simple to use and is built to be extensible for any data source and model.

## Quickstart

The description below use Mixpeek's [python client](https://github.com/mixpeek/mixpeek-python). For examples interfacing with the Mixpeek api directly, see [examples](/examples).

**Import and initialize the client**

```python
from mixpeek import Mixpeek

# initialize the connection (everything is encrypted)
client = Mixpeek(
    connection={
        "engine": "mongodb",
        "connection_string": "mongodb+srv://username:password@hostname",
        "database": "files",
        "collection": "resumes",
    }
)

# create your first collection
collection_id = client.create_collection()
```

**Configure and initiate the indexing worker**

```python
# Index file urls, raw string, or byte objects. 
index_id = client.index(["https://s3.us-east-2.amazonaws.com/resume.pdf"])
```

**Retrieve results using KNN**

```python
# Generate embedding
query = "What was Ethan's first job?"
embedding = client.embed(input=query)

# retrieve the results
results = client.retrieve(
    query={
        "corpus.embedding": query
    },
    filters={"collection_id": collection_id},
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

- [ ] CDC connection with databases for real-time sync
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
