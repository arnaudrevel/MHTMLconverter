"""
MHTML is mainly a multipart e-mail file with a mhtml or mht extension
"""

# TODO: include css

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.generator import Generator

import email

import logging
from typing import Tuple

from . import fileutility
from . import htmlutility

import base64

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
        sourceurl = htmlutility.rewrite_reference_fake_http(sourceurl)

    # Quick and dirty way to find image encoding :/
    image_part = MIMEImage(content, sourceurl.split(".")[-1])
    image_part.add_header('Content-Location', sourceurl)
    mhtmlfile.attach(image_part)

    return mhtmlfile, is_local

def add_css_part(mhtmlfile: MIMEMultipart, sourcecss: URL) -> Tuple[MIMEMultipart, IsLocalFile]:
    """
        The css file is encoded and its related location is set to the name
        of its reference into the HTML file
    """
    try:
        content, is_local = fileutility.get_content(sourcecss)

        if is_local:  # Don't know why but mime related do not work with file:// or local names
            # It's indentifier must be rewrited
            sourcecss = htmlutility.rewrite_reference_fake_http(sourcecss)

        # Is it really a css file?


        # Quick and dirty way to find image encoding :/
        css_part = MIMEImage(content, "css")
        css_part.add_header('Content-Location', sourcecss)
        mhtmlfile.attach(css_part)

        return mhtmlfile, is_local
    except:
        return mhtmlfile, False # If the file cannot be loaded


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

    # Turn all the css relative links into absolute links
    htmlcontent = htmlutility.turn_relative_into_absolute(htmlcontent, sourcefilepath, tag='link',att='href')
    htmlcontent = htmlutility.turn_relative_into_absolute(htmlcontent, sourcefilepath, tag='link',att='data-href')

    # Retrieve all the embedded images
    logging.debug(f"*** Input : {htmlcontent}")
    list_of_img = htmlutility.get_list_of_img_from_html(htmlcontent)
    logging.debug(f"*** Images : {list_of_img}")

    # Create the mhtml file
    mhtmlfile = create_mhtml_header()

    # Add images
    for img in list_of_img:
        logging.debug(img)

        mhtmlfile, is_local = add_img_part(mhtmlfile, img)

        if is_local:  # Don't know why but mime related do not work with file:// or local names
            htmlcontent = htmlutility.rewrite_reference_in_html(
                htmlcontent, img)

    # Retrieve all the embedded css
    logging.debug(f"*** Input : {htmlcontent}")
    list_of_css = htmlutility.get_list_of_css_from_html(htmlcontent)
    logging.debug(f"*** Images : {list_of_css}") 

    # Add css file into the MHTML
    for css in list_of_css:
        logging.debug(css)

        mhtmlfile, is_local = add_css_part(mhtmlfile, css)

        if is_local:  # Don't know why but mime related do not work with file:// or local names
            htmlcontent = htmlutility.rewrite_reference_in_html(
                htmlcontent, css)

    # Add htmlcontent
    mhtmlfile = add_html_part(mhtmlfile, input, htmlcontent)

    # Create output file
    with open(output, 'w') as f:
        gen = Generator(f, False)
        gen.flatten(mhtmlfile)

def mhtml_to_html(mhtmlfile: str, htmlfile: str, resourcesdir: str = "_resources") -> None:
    """
        Convert mhtml to local html file 
    """
    mimefile, _ = fileutility.get_content(mhtmlfile)

    msg = email.message_from_bytes(mimefile)

    htmlcontent: str
    img_content_dict: dict[str,str] = dict()

    for part in msg.walk():
        if part.get_content_type()=="text/html":
            htmlcontent = part.get_payload(decode=True).decode()

        if part.get_content_type().startswith("image"):
            if not part.get_content_type().endswith("css"):
                urlname = part['Content-Location'].strip()
                imagecontent = base64.b64decode(part.get_payload())
                img_content_dict[urlname]=imagecontent
                ### TODO: CSS

    mhtmlfile = fileutility.to_absolute(mhtmlfile)
    htmlfile = fileutility.to_absolute(htmlfile, mhtmlfile)
    resourcesdir = fileutility.to_absolute(resourcesdir, htmlfile) # Path to resourcedir

    for i,content in img_content_dict.items():
        rewrited_path=fileutility.get_res_path(i)
        fileutility.create_file(rewrited_path,resourcesdir,content)

        ### Rewrite with relative reference to htmlfile dir
        htmlcontent = htmlutility.rewrite_reference_in_html(htmlcontent, i, 
            lambda s: fileutility.find_relative_path(htmlfile,resourcesdir)+fileutility.get_res_path(s))

    fileutility.create_file(htmlfile,content=htmlcontent.encode())

    return None
