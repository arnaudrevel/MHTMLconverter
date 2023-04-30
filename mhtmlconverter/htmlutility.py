import bs4  # For HTML easy parsing and management
import logging

import urllib.parse
import pathlib

def turn_relative_into_absolute(htmlcontent: str, sourcefilepath: str, tag: str = "img", att: str="src") -> str:

    logging.info(f"Sourcefilepath: {sourcefilepath}")
    # Is the sourcefile path a url or a local path?
    urlsrc = urllib.parse.urlparse(sourcefilepath)
    srcIsLocal = (urlsrc.scheme=='')

    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')    # May throw a FileNotFound exception

    for i in soup.find_all(tag):
        srcimg = i[att]

        logging.info(f'Before:{srcimg}')

        if srcIsLocal:
            pathimg = pathlib.Path(srcimg)
            logging.info(f"Path {tag}: {pathimg}")
            if urllib.parse.urlparse(srcimg).scheme=='':
                if not pathimg.is_absolute():
                    sourcepath = pathlib.Path(sourcefilepath)
                    logging.info(f"Sourcepath: {sourcepath}")
                    path2 = sourcepath.parent / pathimg
                    i[att]=path2.resolve()
                else:
                    i[att]=pathimg.resolve()
        else:
                pathurl = urllib.parse.urlparse(srcimg)
                pathIsRelative = (pathurl.scheme=='')

                if pathIsRelative:
                    i[att] = urllib.parse.urljoin(sourcefilepath,srcimg)

        logging.info(f'After:{i[att]}')

    logging.debug(str(soup))

    return str(soup)

def get_list_of_img_from_html(htmlcontent: str) -> list[str]:
    """
        Returns the list of URLs corresponding to the img
        referenced in the html file

        >>> get_list_of_img_from_html('<!DOCTYPE html><img src="testok.jpg">')
        ['testok.jpg']

        >>> get_list_of_img_from_html('<!DOCTYPE html>')
        []

    """
    # logging.debug(f"get_list_of_img - URL {url}")
    # content = urllib.request.urlopen(url).read()
    logging.debug(f"CONTENT {htmlcontent}")
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')    # May throw a FileNotFound exception

    return [str(u.get('src')) for u in soup.find_all("img")]

def rewrite_reference(localurl: str) -> str:
    """
        Transform a local reference into a fake http reference

        Don't know why but mime related do not work with file:// or local names
    """
    return f"http://{localurl}"

def rewrite_reference_in_html(htmlcontent: str, reference: str) -> str:
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')
    for i in soup.find_all('img'):
        if i.get('src') == reference:
            im = soup.new_tag('img')
            im['src'] = rewrite_reference(reference)
            i.replace_with(im)
    return str(soup)