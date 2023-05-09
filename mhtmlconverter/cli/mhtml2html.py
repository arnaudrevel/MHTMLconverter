"""
This module provides a tool to convert mhtml files to an HTML file with
linked resources are stored in a local directory
"""
import logging
import click
from .. import mhtml

logging.basicConfig(level=logging.INFO,format="\x1b[32;20m %(filename)s > \x1b[34;20m %(funcName)s : \x1b[0m %(message)s")


@click.command(help="MHTML to HTML converter")
@click.option("-i","--input","mhtmlfile",required=True, help="mhtml input filename")
@click.option("-o","--output","outputfile",default="output.html",help="html output filename")
def main(htmlfile:str = "index.mhtml",outputfile:str = "output.html")-> None:
    """
    Main program
    Converts the 'mhtmlfile' into an html file
    """
    mhtml.mhtml_to_html(htmlfile,outputfile)

 # Main entry point
if __name__ == "__main__":
    main()