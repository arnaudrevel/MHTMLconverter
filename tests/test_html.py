"""
"""

import mhtmlconverter.mhtml

import pathlib

def test_html() -> None:
    """
        Test HTML
    """
    out = pathlib.Path("./tests/resources/test.mhtml")

    if out.exists():    out.unlink()

    mhtmlconverter.mhtml.url_to_mhtml("./tests/resources/test.html","./tests/resources/test.mhtml")

    assert(out.exists())

def test_local_html() -> None:
    """
        Test Local HTML

    """
    out = pathlib.Path("./tests/resources/test_local.mhtml")

    if out.exists():    out.unlink()

    mhtmlconverter.mhtml.url_to_mhtml("./tests/resources/test_local.html","./tests/resources/test_local.mhtml")

    assert(out.exists())