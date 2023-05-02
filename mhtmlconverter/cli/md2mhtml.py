"""
This package intends to provide a tool to convert markdown files including
images to a single MHTML self-content file
"""
import logging
import click
import markdown
from .. import mhtml

logging.basicConfig(level=logging.INFO,format="%(filename)s - %(funcName)s - %(message)s")


@click.command(help="MD to MHTML converter")
@click.option("-i","--input","mdfile", required=True,help="md input filename")
@click.option("-o","--output","outputfile",default="output.mhtml",help="mhtml output filename")
def main(mdfile:str = "README.md",outputfile: str = "output.mhtml") -> None:
    """
    Main program
    Converts the 'mdfile' with references to images into an mhtml single file
    """
    with open(mdfile,"r") as md_file:
        htmlcontent = markdown.markdown(md_file.read())
        mhtml.html_content_to_mhtml(htmlcontent,outputfile, mdfile)

 # Main entry point
if __name__ == "__main__":
    main()
    