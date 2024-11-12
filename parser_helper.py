#------------------------------------------------------------
# Data parsing helpers
#-----------------------------------------------------------*/

import re

def get_name(html):
    try:
        name = html.text.strip()
    except AttributeError as e:
        print(e)
        return None
    return name

def get_text_helper(html, strong_tag):
    regex = re.compile(strong_tag)
    try:
        text = html.find('strong', string= regex).next_sibling.strip()
    except AttributeError as e:
        print(e)
        return None
    return text

def get_title(html):
    return get_text_helper(html, 'Title')

def get_office(html):
    return get_text_helper(html, 'Office')

def get_phone(html):
    return get_text_helper(html, 'Phone')

def get_email(html):
    regex = re.compile('Email')
    try:
        text = html.find('strong', string= regex).find_next_sibling('a').text.strip()
    except AttributeError as e:
        print(e)
        return None
    return text

def get_website(html):
    regex = re.compile('Web')
    try:
        text = html.find('strong', string= regex).find_next_sibling('a').get('href').strip()
    except AttributeError as e:
        print(e)
        return None
    return text