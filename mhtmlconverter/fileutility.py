import urllib.request
import urllib.parse
import urllib.error

import logging

import pathlib

from typing import Tuple

URL = str

def get_html_content(url: URL) -> str:
    """
        Get the html content given the URL
    """
    content, _ = get_content(url)

    return content.decode()

isLocalFile = bool

def get_content(url: URL) -> Tuple[bytes, isLocalFile]:
    
    logging.info(url)

    try:
        content = urllib.request.urlopen(url).read()
        return content, False
    except Exception:
        logging.debug(f"{url}")
        path = pathlib.Path(url)
        if path.exists():
            with open(path.absolute(),"rb") as f:
                return f.read(), True
        raise