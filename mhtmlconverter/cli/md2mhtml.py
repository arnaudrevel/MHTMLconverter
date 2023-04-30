"""
This package intends to provide a tool to convert markdown files including
images to a single MHTML self-content file
"""
import logging
from .. import mhtml
import click
import markdown


logging.basicConfig(level=logging.INFO,format="%(filename)s - %(funcName)s - %(message)s")


@click.command(help="MD to MHTML converter")
@click.option("-i","--input","mdfile", required=True,help="md input filename")
@click.option("-o","--output","outputfile",default="output.mhtml",help="mhtml output filename")
def main(mdfile,outputfile):
    with open(mdfile,"r") as f:
        htmlcontent = markdown.markdown(f.read())
        mhtml.html_content_to_mhtml(htmlcontent,outputfile, mdfile)

 # Main entry point
if __name__ == "__main__":
    main()
    