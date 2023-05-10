"""
    HTML Utilities

    Some function to :
    - transform relative references into global `turn_relative_into_absolute()`
    - extract the list of images referenced in a HTML Dom `get_list_of_img_from_html()`
    - rewrite the references to the img files if they are local `rewrite_reference()` 
                (pb with local files for MHTML)
    - rewrite the references into the HTML Dom in for consistance with renamed references
                `rewrite_reference_in_html()`
"""
import logging
import urllib.parse
import pathlib
import bs4  # For HTML easy parsing and management
import typing

URL = str

def turn_relative_into_absolute(htmlcontent: str, sourcefilepath: str,
                                tag: str = "img", att: str = "src") -> str:
    """
        Transform relative references into global

        >>> turn_relative_into_absolute('<!DOCTYPE html><img src="img.jpg">',"http://www.test.fr/index.html")
        '<!DOCTYPE html>\\n<img src="http://www.test.fr/img.jpg"/>'

        >>> turn_relative_into_absolute('<!DOCTYPE html><img src="../img.jpg">',"http://www.test.fr/dir/index.html")
        '<!DOCTYPE html>\\n<img src="http://www.test.fr/img.jpg"/>'
    """

    logging.info(f"Sourcefilepath: {sourcefilepath}")
    # Is the sourcefile path a url or a local path?
    urlsrc = urllib.parse.urlparse(sourcefilepath)
    src_is_local = urlsrc.scheme == ''

    # May throw a FileNotFound exception
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')

    for i in soup.find_all(tag):
        if i.has_attr(att):
            srcimg = i[att]

            logging.info(f'Before:{srcimg}')

            if src_is_local:
                pathimg = pathlib.Path(srcimg)
                logging.info(f"Path {tag}: {pathimg}")
                if urllib.parse.urlparse(srcimg).scheme == '':
                    if not pathimg.is_absolute():
                        sourcepath = pathlib.Path(sourcefilepath)
                        logging.info(f"Sourcepath: {sourcepath}")
                        path2 = sourcepath.parent / pathimg
                        i[att] = path2.resolve()
                    else:
                        i[att] = pathimg.resolve()
            else:
                pathurl = urllib.parse.urlparse(srcimg)
                path_is_relative = pathurl.scheme == ''

                if path_is_relative:
                    i[att] = urllib.parse.urljoin(sourcefilepath, srcimg)

            logging.info(f'After:{i[att]}')

    logging.debug(str(soup))

    return str(soup)


def get_list_of_img_from_html(htmlcontent: str) -> list[URL]:
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
    # May throw a FileNotFound exception
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')

    return [str(u.get('src')) for u in soup.find_all("img")]

def get_list_of_css_from_html(htmlcontent: str) -> list[URL]:
    """
        Returns the list of URLs corresponding to the css files
        referenced in the html file
    """
    logging.info(f"CONTENT {htmlcontent}")
    # May throw a FileNotFound exception
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')

    listhref = [str(u.get('href')) for u in soup.find_all("link")]

    if listhref is None: listhref = list()

    listhrefdata = [str(u.get('data-href')) for u in soup.find_all("link")]

    if listhrefdata: listhref.append(listhrefdata)
    
    return listhref


def rewrite_reference_fake_http(localurl: str) -> str:
    """
        Transform a local reference into a fake http reference

        Don't know why but mime related do not work with file:// or local names

        Simply add a fake "http://" protocol in front of the actual name

        TODO: check if it works even with file:// protocol

        >>> rewrite_reference_fake_http("img.jpg")
        'http://img.jpg'
    """
    return f"http://{localurl}"


def rewrite_reference_in_html(htmlcontent: str, reference: str, 
        rewrite_func: typing.Callable[[str],str] = rewrite_reference_fake_http) -> str:
    """
        rewrite the references into the HTML Dom for consistancy with renamed references
                `rewrite_reference_in_html()`
        
        >>> rewrite_reference_in_html('<!DOCTYPE html><img src="img.jpg">', "img.jpg")
        '<!DOCTYPE html>\\n<img src="http://img.jpg"/>'

    """
    soup = bs4.BeautifulSoup(htmlcontent, 'html.parser')
    for i in soup.find_all('img'):
        if i.get('src') == reference:   # If the found img is the one referenced
            im = soup.new_tag('img')
            im['src'] = rewrite_func(reference)
            i.replace_with(im)
    return str(soup)
