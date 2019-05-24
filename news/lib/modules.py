from urllib.request import urlopen
from urllib.parse import urlparse
from urllib import request
import requests
from bs4 import BeautifulSoup
import favicon
#import requests

def get_fi_link(url):
    parsed_uri = urlparse(url)
    host = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    icons = favicon.get(host)
    for icon in icons:
        if icon.format == 'ico':
            icon_link=icon.url
    return (icon_link)
