"""
This package intends to provide a tool to convert html files including
images to a single MHTML self-content file
"""
import logging
import click
from .. import mhtml

logging.basicConfig(level=logging.INFO,format="\x1b[32;20m %(filename)s > \x1b[34;20m %(funcName)s : \x1b[0m %(message)s")


@click.command(help="HTML to MHTML converter")
@click.option("-i","--input","htmlfile",default="myindex_local.html",help="html input filename")
@click.option("-o","--output","outputfile",default="output.mhtml",help="mhtml output filename")
def main(htmlfile,outputfile):
    """
    Main program
    Converts the 'htmlfile' with references to images into an mhtml single file
    """
    mhtml.url_to_mhtml(htmlfile,outputfile)

 # Main entry point
if __name__ == "__main__":
    main()
    