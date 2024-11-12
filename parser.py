#-------------------------------------------------------------------------
# AUTHOR: Fidelis Prasetyo
# FILENAME: parser.py
# SPECIFICATION: parse faculty members' data from crawler's database
# FOR: CS 5180- Assignment #3
# TIME SPENT: 2 days
#-----------------------------------------------------------*/

from bs4 import BeautifulSoup

from pages_db import *
from faculty_db import *
from parser_helper import *

TARGET_URL = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

def parse_faculty_data(html, faculty_db):
    bs = BeautifulSoup(html['html'], 'html.parser')

    #find all h2 headers
    h2_tags = bs.find('div', id='main').find_all('h2')

    for h2_tag in h2_tags:

        #find the paragraph tag
        p_tag = h2_tag.find_next_sibling('p')

        name = get_name(h2_tag)
        title = get_title(p_tag)
        office = get_office(p_tag)
        phone = get_phone(p_tag)
        email = get_email(p_tag)
        website = get_website(p_tag)

        faculty_db.create_or_update_if_exist(name, title, office, phone, email, website)

if __name__ == '__main__':

    pages_db = PagesDatabase()
    html = pages_db.find_document(TARGET_URL)

    faculty_db = FacultyDatabase()
    parse_faculty_data(html, faculty_db)



