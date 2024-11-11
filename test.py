from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

html = open("index.html")

bs = BeautifulSoup(html, 'html.parser')

print(bs.table.find_all('img'))