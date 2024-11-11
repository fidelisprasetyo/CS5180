import ssl
import certifi

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from urllib.error import URLError

from CPPDatabase import *

URL_SEED = 'https://www.cpp.edu/sci/computer-science/'
BASE_URL = 'https://www.cpp.edu/'

is_visited = {}

def extract_urls(html):
    url_list = []
    for url in html.find_all('a', href=True):

        # handle relative url
        parsed_url = url['href']
        abs_url = urljoin(BASE_URL, parsed_url)

        if url not in is_visited:
            url_list.append(abs_url)

    return url_list

def crawlerThread(frontier, col_name):

    db = CPPDatabase()
    context = ssl.create_default_context(cafile=certifi.where())

    while(frontier):
        url = frontier.pop(0)

        try:
            html = urlopen(url, context=context)
        except (HTTPError, URLError) as e:
            print(e)
            continue

        print("visiting " + url)
        is_visited[url] = True

        bs = BeautifulSoup(html, 'html.parser')
        db.create_or_update_if_exist(col_name, url, str(bs))

        ## target url criteria
        header = bs.find('h1', class_='cpp-h1')
        if header is not None:
            if header.text == 'Permanent Faculty':
                flag = url
                frontier.clear()
                print("Target URL found!! -- " + flag)
        else:
            frontier.extend(extract_urls(bs))

    return flag


if __name__ == '__main__':

    frontier = []
    frontier.append(URL_SEED)

    target_page_url = crawlerThread(frontier, 'pages')