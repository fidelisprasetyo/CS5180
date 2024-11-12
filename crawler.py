#-------------------------------------------------------------------------
# AUTHOR: Fidelis Prasetyo
# FILENAME: crawler.py
# SPECIFICATION: crawl the CPP's CS dept website until reach target URL
# FOR: CS 5180- Assignment #3
# TIME SPENT: 2 days
#-----------------------------------------------------------*/

import ssl
import certifi

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
from urllib.error import URLError

from pages_db import *

URL_SEED = 'https://www.cpp.edu/sci/computer-science/'
BASE_URL = 'https://www.cpp.edu/'

def scrape_urls(html):
    url_list = []
    for url_tag in html.find_all('a', href=True):

        # handle relative url
        parsed_url = url_tag.get('href')
        abs_url = urljoin(BASE_URL, parsed_url)

        url_list.append(abs_url)
    return url_list

def crawlerThread(frontier, pages_db):

    is_visited = {}
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
        pages_db.create_or_update_if_exist(url, str(bs))

        # target url criteria
        header = bs.find('h1', class_='cpp-h1')
        if header is not None:
            if header.text == 'Permanent Faculty':
                flag = url
                frontier.clear()
                print("Target URL found!! -- " + flag)
        else:
            url_list = scrape_urls(bs)
            for url_found in url_list:
                if is_visited.get(url_found) is None:
                    frontier.append(url_found)

    return flag

if __name__ == '__main__':

    frontier = []
    frontier.append(URL_SEED)
    db = PagesDatabase()

    target_page_url = crawlerThread(frontier, db)