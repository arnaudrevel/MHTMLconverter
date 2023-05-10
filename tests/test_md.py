"""
"""

import mhtmlconverter.mhtml

import pathlib

import markdown

def test_md() -> None:
    """
        Test MD
    """
    out = pathlib.Path("./tests/resources/results/test_md.mhtml")

    if out.exists():    out.unlink()

    with open("./tests/resources/test.md","r") as md_file:
        htmlcontent = markdown.markdown(md_file.read())
        mhtmlconverter.mhtml.html_content_to_mhtml(htmlcontent,"./tests/resources/results/test_md.mhtml", "./tests/resources/test_local.md")

    assert(out.exists())

def test_local_md() -> None:
    """
        Test local MD

    """
    out = pathlib.Path("./tests/resources/results/test_localmd.mhtml")

    if out.exists():    out.unlink()

    with open("./tests/resources/test_local.md","r") as md_file:
        htmlcontent = markdown.markdown(md_file.read())
        mhtmlconverter.mhtml.html_content_to_mhtml(htmlcontent,"./tests/resources/results/test_localmd.mhtml", "./tests/resources/test_local.md")

    assert(out.exists())