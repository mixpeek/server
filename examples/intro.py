from mixpeek import Mixpeek
from pydantic import BaseModel

# initiatlize mixpeek client using a collection_id tenant
client = Mixpeek(
    connection={
        "storage": "mongodb",
        "connection_string": "mongodb+srv://username:password@hostname",
        "database": "files",
        "collection": "resumes",
    },
    embedding_model={
        "name": "all-MiniLM-L6-v2",
        "version": "latest",
    },
    embed_suffix="embedding",
)


# Define how you'd like to index the content
class StorageModel(BaseModel):
    file_metadata: dict
    raw_content: str


# Index file urls, raw string, or byte objects. Returns a unique id for the index.
index_id = client.index(
    input=[
        "https://nux-sandbox.s3.us-east-2.amazonaws.com/marketing/ethan-resume.pdf",
    ],
    upsert={"collection_id": "1"},
    data_model={
        "schema": StorageModel.to_dict(),  # optional
        "fields_to_embed": [
            "raw_content",
            "file_metadata.name",
        ],
        "metadata": {
            "name": "Ethan's Resume",
        },
    },
)
# this should also create the mongo index.

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
