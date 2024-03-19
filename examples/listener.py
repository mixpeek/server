from nuxai import NUX

# initiaize client with where you want the data stored, can be localhost
nux = NUX(storage_url="mongodb://localhost:27017/")

# create a collection for each listener 
collection_id = nux.create_collection(
    topic="cosentyx",
    listener="reddit"
)

# define embedding model for each 
index_id = nux.index(
    embedding_model="clinical_bert",
    collection_id=collection_id
)

# query the data, which spans each listener
results = nux.retrieve(query="Where was the least popular region for cosentyx?", listeners=["reddit"])

# llm to generate a report based on predfined prompt/parameters. llm can be local
report = nux.generate(
    context=results,
    model="local_llama",
    task="classification"
)

[{
    "sentiment": "positive",
    "source": {"type": "url", "https://www.reddit.com/r/Psoriasis/comments/p4rd1a/have_you_tried_cosentyx_secukinumab_any_side/"},
    "text": "I have been on Cosentyx for 3 years now and it has been a game changer for me.",
    "timestamp": "2022-03-09T14:00:00Z",
    "user": "u/psoriasis_throwaway"
}]

