from urllib.parse import urlparse, unquote
import os


def get_filename_from_cd(cd):
    """
    Extract filename from content-disposition header if available.
    """
    if not cd:
        return None
    fname = cd.split("filename=")[1]
    if fname.lower().startswith(("'", '"')):
        fname = fname[1:-1]
    return unquote(fname)


def generate_filename_from_url(url):
    """
    Extract filename from URL if possible.
    """
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)
