"""
    Tests for html2mhtml conversion
"""

import pathlib
import mhtmlconverter.mhtml


def test_html() -> None:
    """
        Test HTML
    """
    out = pathlib.Path("./tests/resources/results/test.mhtml")

    if out.exists():    out.unlink()

    mhtmlconverter.mhtml.url_to_mhtml("./tests/resources/test.html","./tests/resources/results/test.mhtml")

    assert(out.exists())

def test_local_html() -> None:
    """
        Test Local HTML

    """
    out = pathlib.Path("./tests/resources/results/test_local.mhtml")

    if out.exists():    out.unlink()

    mhtmlconverter.mhtml.url_to_mhtml("./tests/resources/test_local.html","./tests/resources/results/test_local.mhtml")

    assert(out.exists())

def test_css_html() -> None:
    """
        Test HTML
    """
    out = pathlib.Path("./tests/resources/results/test_css.mhtml")

    if out.exists():    out.unlink()

    mhtmlconverter.mhtml.url_to_mhtml("https://github.com/arnaudrevel/MHTMLconverter","./tests/resources/results/test_css.mhtml")

    assert(out.exists())    