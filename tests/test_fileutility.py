"""
"""

import mhtmlconverter.fileutility

import pathlib

import markdown

def test_rewrite_if_relative() -> None:
    """
        Test fileutility
    """

    # Test relative file with no absolute path > returns absolute path
    assert(mhtmlconverter.fileutility.to_absolute("test_mhtml.mhtml")
        ==str((pathlib.Path(".")/"test_mhtml.mhtml").resolve()))

    # Test relative relative dir with relative path > returns path relative to relative dir
    assert(mhtmlconverter.fileutility.to_absolute("_resources","test_mhtml.mhtml")
        ==str((pathlib.Path(".")/"_resources").resolve()))

    # Test relative path with absolute path > returns path relative to absolute path
    assert(mhtmlconverter.fileutility.to_absolute("_resources",pathlib.Path("test.mhtml").resolve())
        ==str((pathlib.Path(".")/"_resources").resolve()))

    # Test absolute path with absolute path > stays the path unchanged
    assert(mhtmlconverter.fileutility.to_absolute(pathlib.Path("../_resources").resolve(),
        pathlib.Path("test.mhtml").resolve())==str(pathlib.Path("../_resources").resolve()))

def test_get_res_path() -> None:
    """
        Test get_res_path()
    """
    assert(mhtmlconverter.fileutility.get_res_path("https://storage.googleapis.com/pai-images/72cd017dc3724f3bb987813afac8dec5.jpeg")
           =="/pai-images/72cd017dc3724f3bb987813afac8dec5.jpeg")