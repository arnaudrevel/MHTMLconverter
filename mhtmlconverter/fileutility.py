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

def to_absolute(infile: str, absolute: str = None) -> str:
    """
        If the infile path is relative, rewrite it in reference to absolutepath
        
        If no absolutepath is given, make infile absolute
    """
    inpath = pathlib.Path(infile).parent
    
    if absolute is None:
        if inpath.exists():
            return str(pathlib.Path(infile).resolve())
        else:
                raise FileNotFoundError
    else:
        absolutepath = pathlib.Path(absolute).parent
        if absolutepath.exists(): # The parent directory should exist
            if inpath.resolve() == inpath: # Absolute path
                return str(pathlib.Path(infile).resolve())
            else:
                return str((absolutepath / pathlib.Path(infile)).resolve()) # Path is relative to output file path
        else:
            raise FileNotFoundError
        
def get_res_path(url: str):
    """
        Returns path to the resource without protocol and server
    """
    res = urllib.parse.urlparse(url)
    return res.path

def create_file(relpath: str, resourcesdir: str = "", content: bytes = None) -> None:
    """
        Create a file in the resourcedir
    """
    path = pathlib.Path(resourcesdir+relpath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)

def find_relative_path(pathsrcstr: str, path2str: str) -> str:
    """
        Returns the relative path for absolute path2 in reference to absolute pathsrc

        >>> find_relative_path("/path/to/html/index.html", "/path/to/html/_resources/img.jpg")
        '_resources/img.jpg'
        >>> find_relative_path("/path/to/html/index.html", "/path/to/_resources/img.jpg")
        '../_resources/img.jpg'
        >>> find_relative_path("/path/to/html/index.html", "/another/path/to/_resources/img.jpg")
        '/another/path/to/_resources/img.jpg'

    """
    pathsrc = pathlib.Path(pathsrcstr)
    path2 = pathlib.Path(path2str)

    partssrc=pathsrc.parts
    partspath2 = path2.parts

    i=0

    while i < len(partssrc) and i < len(partspath2) and partssrc[i] == partspath2[i]:
        i+=1

    if i==0 or i==1: # No common part
        return path2.as_posix()

    prefix = (len(partssrc)-i-1)*[".."] # Add as many ".." as subdirectories to find the html file

    return (pathlib.Path(*prefix) / pathlib.Path(*partspath2[i:])).as_posix()