import secrets
import uuid
from datetime import datetime
from urllib.parse import quote_plus
from haikunator import Haikunator
from bson import ObjectId


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


def unique_name(exclude_list=[]):
    haikunator = Haikunator()

    while True:
        # token_length=0 removes the numeric token at the end
        name = haikunator.haikunate(token_length=0)
        if name not in exclude_list:
            return name


def generate_function_name(index_id, provider_id, function_name):
    # split the string at the first occurence of "ix-" and take the first 8 characters
    ix = index_id.split("ix-", 1)[1][:8]
    pv = provider_id[:6]
    fx = function_name
    return f"{ix}-{pv}-{fx}"


def convert_to_variable_name(s):
    return s.replace(" ", "_").lower()


def make_string_url_safe(s):
    """Convert a string into a URL safe string."""
    return quote_plus(s)


def convert_objectid_to_str(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = str(value)
            elif isinstance(value, dict):
                item[key] = convert_objectid_to_str(value)
    return item
