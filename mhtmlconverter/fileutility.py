"""
    File utilities to get content from file
"""
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

IsLocalFile = bool

def get_content(url: URL) -> Tuple[bytes, IsLocalFile]:
    """
        Low level get content from file
    """

    logging.info(url)

    print(url)

    try:
        # Let's pretend we are Mozilla to overpass HTTP 403 error
        req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read()
        return content, False
    except Exception:
        logging.debug(f"{url}")
        path = pathlib.Path(url)
        if path.exists():
            with open(path.absolute(),"rb") as html_file:
                return html_file.read(), True
        raise
