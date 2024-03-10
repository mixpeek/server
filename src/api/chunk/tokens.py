import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm


def get_token_count(model_name, string):
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = len(encoding.encode(string))
    return num_tokens


class Chunker:
    def __init__(self):
        # Initialize the class with a `data` attribute and tokenizer, text splitter and chunks attributes
        self.tokenizer = tiktoken.get_encoding('p50k_base')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            length_function=self.tiktoken_len,
            separators=["\n\n", "\n", " ", ""]
        )
        self.chunks = []

    def tiktoken_len(self, text):
        # A helper function to calculate the length of a text in tokens
        tokens = self.tokenizer.encode(text, disallowed_special=())
        return len(tokens)

    def split_text(self, content):
        chunks = []
        # Use the `text_splitter` object to split the big content string into smaller texts
        texts = self.text_splitter.split_text(content)

        # Iterate over the list of smaller texts and append each one to the `self.chunks` list
        for text in texts:
            chunks.append(text)
        return chunks
