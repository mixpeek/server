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
