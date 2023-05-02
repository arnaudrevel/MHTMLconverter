"""
MHTML is mainly a multipart e-mail file with a mhtml or mht extension
"""

# TODO: include css

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.generator import Generator

import logging
from typing import Tuple

from . import fileutility
from . import htmlutility

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
    # mhtmlfile['Subject'] = '<No>'
    # mhtmlfile['Snapshot-Content-Location'] = sourcename
    # mhtmlfile['Date'] = "Wed, 26 Apr 2023 18:14:43 -0000"

    return mhtmlfile


def add_html_part(mhtmlfile: MIMEMultipart, sourcename: URL, htmlcontent: str) -> MIMEMultipart:
    """
        Add the html content to the MHTML file
    """

    html_part = MIMEText(htmlcontent, 'html')
    mhtmlfile.attach(html_part)

    return mhtmlfile


IsLocalFile = bool


def add_img_part(mhtmlfile: MIMEMultipart, sourceurl: URL) -> Tuple[MIMEMultipart, IsLocalFile]:
    """
        The image is encoded and its related location is set to the name
        of its reference into the HTML file
    """
    content, is_local = fileutility.get_content(sourceurl)

    if is_local:  # Don't know why but mime related do not work with file:// or local names
        # It's indentifier must be rewrited
        sourceurl = htmlutility.rewrite_reference(sourceurl)

    # Quick and dirty way to find image encoding :/
    image_part = MIMEImage(content, sourceurl.split(".")[-1])
    image_part.add_header('Content-Location', sourceurl)
    mhtmlfile.attach(image_part)

    return mhtmlfile, is_local


def url_to_mhtml(input_file: URL, output: FILENAME) -> None:
    """
        Transform an html file into a mhmtl file
    """
    # Read HTML file content
    htmlcontent = fileutility.get_html_content(input_file)
    logging.debug(htmlcontent)
    html_content_to_mhtml(htmlcontent, output, input_file)


def html_content_to_mhtml(htmlcontent: str, output: FILENAME, sourcefilepath: str) -> None:
    """
        Transform an htmlcontent into a mhmtl file

        The sourcefile is needed if relative links must be rewritten
    """

    # Turn all the img relative links into absolute links
    htmlcontent = htmlutility.turn_relative_into_absolute(
        htmlcontent, sourcefilepath)

    # TODO : Turn all the css relative links into absolute links
    # htmlcontent = htmlutility.turn_relative_into_absolute(htmlcontent, sourcefilepath, tag='link',att='href')
    # TODO: Add css file into the MHTML

    # Retrieve all the embedded images
    logging.debug(f"*** Input : {htmlcontent}")
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

        mhtmlfile, is_local = add_img_part(mhtmlfile, img)

        if is_local:  # Don't know why but mime related do not work with file:// or local names
            htmlcontent = htmlutility.rewrite_reference_in_html(
                htmlcontent, img)

    # Add htmlcontent
    mhtmlfile = add_html_part(mhtmlfile, input, htmlcontent)

    # Create output file
    with open(output, 'w') as f:
        gen = Generator(f, False)
        gen.flatten(mhtmlfile)
