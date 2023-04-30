"""
MHTML is mainly a multipart e-mail file with a mhtml or mht extension
"""

# TODO: include css

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.generator import Generator

import logging

import fileutility
import htmlutility

from typing import Tuple

URL = str
FILENAME = str

def create_mhtml_header() -> MIMEMultipart:
    """
    Create the empty mhtml structure
    
    According to https://en.wikipedia.org/wiki/MHTML

    An MHTML file is a:
    - MIME multipart/related file

    """
    mhtmlfile = MIMEMultipart('related')
    mhtmlfile['From'] = '<Saved by Quantic Rabbit>'
    
    # Unused declarations
    #mhtmlfile['Subject'] = '<No>'
    #mhtmlfile['Snapshot-Content-Location'] = sourcename
    #mhtmlfile['Date'] = "Wed, 26 Apr 2023 18:14:43 -0000"

    return mhtmlfile

def add_html_part(mhtmlfile: MIMEMultipart, sourcename: URL, htmlcontent: str) -> MIMEMultipart:

    html_part = MIMEText(htmlcontent, 'html')
    mhtmlfile.attach(html_part)

    return mhtmlfile

isLocalFile = bool

def add_img_part(mhtmlfile: MIMEMultipart, sourceurl: URL) -> Tuple[MIMEMultipart, isLocalFile]:
    """
        The image is encoded and its related location is set to the name
        of its reference into the HTML file
    """
    content, isLocal = fileutility.get_content(sourceurl)

    if isLocal: # Don't know why but mime related do not work with file:// or local names
        # It's indentifier must be rewrited
        sourceurl = htmlutility.rewrite_reference(sourceurl)

    image_part = MIMEImage(content , sourceurl.split(".")[-1])    # Quick and dirty way to find image encoding :/
    image_part.add_header('Content-Location', sourceurl)
    mhtmlfile.attach(image_part)

    return mhtmlfile, isLocal

def url_to_mhtml(input:URL, output: FILENAME) -> None:
    """
        Transform an html file into a mhmtl file
    """
    # Read HTML file content
    htmlcontent=fileutility.get_html_content(input)
    logging.debug(htmlcontent)
    html_content_to_mhtml(htmlcontent,output, input)

def html_content_to_mhtml(htmlcontent:str, output: FILENAME, sourcefilepath:str) -> None:
    """
        Transform an htmlcontent into a mhmtl file

        The sourcefile is needed if relative links must be rewritten
    """

    # Turn all the img relative links into absolute links
    htmlcontent = htmlutility.turn_relative_into_absolute(htmlcontent, sourcefilepath)

    # TODO : Turn all the css relative links into absolute links
    # htmlcontent = htmlutility.turn_relative_into_absolute(htmlcontent, sourcefilepath, tag='link',att='href')
    # TODO: Add css file into the MHTML

    # Retrieve all the embedded images
    logging.debug(f"*** Input : {input}")
    list_of_img = htmlutility.get_list_of_img_from_html(htmlcontent)
    logging.debug(f"*** Images : {list_of_img}")

    # Create the mhtml file
    mhtmlfile = create_mhtml_header()

    # Add images
    for img in list_of_img:
        logging.debug(img)

        # # If the link to the image is relative rewrite it in reference to
        # # the directory where's the html file
        # img = fileutility.rewrite_if_relative(sourcefile, img)

        mhtmlfile, isLocal = add_img_part(mhtmlfile, img)

        if isLocal: # Don't know why but mime related do not work with file:// or local names
            htmlcontent = htmlutility.rewrite_reference_in_html(htmlcontent, img)

    # Add htmlcontent
    mhtmlfile = add_html_part(mhtmlfile, input, htmlcontent)

    # Create output file
    with open(output, 'w') as f:
        gen = Generator(f, False)
        gen.flatten(mhtmlfile)