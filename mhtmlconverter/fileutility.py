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

# def rewrite_if_relative(sourcefile: URL, img: URL) -> URL:

#     # If it is not a local file img stay unchanged
#     if urllib.parse.urlparse(img).scheme!='': return img

#     path = pathlib.Path(img)

#     if not path.is_absolute():
#         sourcepath = pathlib.Path(sourcefile).parent
#         path2 = sourcepath / path
#         return path2.resolve()
    
#     return img