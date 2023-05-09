"""
"""

import mhtmlconverter.mhtml

import pathlib

import markdown

import shutil

def test_mhtml() -> None:
    """
        Test MHTML
    """
    out = pathlib.Path("./tests/resources/test_mhtml.html")
    outdir = pathlib.Path("./tests/resources/_resources")
    
    if out.exists():    out.unlink()
    if outdir.exists():
        shutil.rmtree(outdir.resolve())
    
    mhtmlconverter.mhtml.mhtml_to_html("./tests/resources/test_mhtml.mhtml","test_mhtml.html")

    assert(out.exists())