import secrets
import re
import uuid
from utilities.methods import BadRequestError
import json
import random
import subprocess
import tempfile
from datetime import datetime
from bson import ObjectId
import aiohttp
from urllib.parse import quote_plus

from typing import List, Union
import ast


def generate_api_key():
    length = 50
    return secrets.token_urlsafe(length)


def generate_uuid(length=36, dashes=True):
    x = uuid.uuid4()
    if dashes:
        return str(x)[:length]
    else:
        return str(x).replace("-", "")[:length]


def current_time():
    return datetime.utcnow()


def validate_file_size(file, max_size):
    max_size_bytes = max_size * 1024 * 1024  # Convert max_size from MB to bytes
    if len(file) > max_size_bytes:
        raise BadRequestError(detail=f"File size exceeds {max_size} MB")


def random_noun_verb_combo(exclude_list=[]):
    verbs = [
        "convert",
        "map",
        "merge",
        "split",
        "aggregate",
        "filter",
        "sort",
        "normalize",
        "encode",
        "decode",
        "join",
        "extract",
        "load",
        "clean",
        "validate",
        "transform",
        "integrate",
        "migrate",
        "pivot",
        "index",
    ]
    nouns = [
        "data",
        "record",
        "field",
        "database",
        "table",
        "row",
        "column",
        "index",
        "value",
        "element",
        "entry",
        "file",
        "format",
        "structure",
        "array",
        "object",
        "string",
        "variable",
        "parameter",
        "attribute",
        "vector",
    ]

    while True:
        verb = random.choice(verbs)
        noun = random.choice(nouns)
        combo = verb + "_" + noun

        if combo not in exclude_list:
            return combo


def generate_function_name(index_id, workbook_id, db_block):
    ix = index_id[-10:]
    wb = workbook_id[-6:]
    block = db_block["block_id"]
    cell = db_block["metadata"]["cell_name"]
    return f"{ix}-{wb}-{block}-{cell}"


def convert_to_variable_name(s):
    return s.replace(" ", "_").lower()


def make_string_url_safe(s):
    """Convert a string into a URL safe string."""
    return quote_plus(s)


async def read_url_content(url):
    """
    Asynchronously fetch and return the content of the given URL.
    This could be used for web scraping or making API calls.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                # Check if the request was successful
                if response.status == 200:
                    # Read and return the content of the response
                    return await response.text()
                else:
                    print(
                        f"Failed to retrieve content from {url}. Status: {response.status}"
                    )
                    return None
        except Exception as e:
            print(f"An error occurred while fetching {url}: {e}")
            return None
