#------------------------------------------------------------
# ENCAPSULATE DATABASE FUNCTIONS
#-----------------------------------------------------------*/

from pymongo import MongoClient

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017
COL_NAME = "pages"

class PagesDatabase():

    def __init__(self):
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = client[DB_NAME]
            print("Connected to " + DB_NAME + " database, collection: " + COL_NAME)

        except:
            print("Database not connected successfully")
        
        self.__col = self.db[COL_NAME]

    def create_document(self, url, html):

        doc = {"url": url, 
               "html": html}
        
        self.__col.insert_one(doc)

    def update_document(self, url, html):

        doc = {"$set": {
                "url": url,
                "html": html}}

        self.__col.update_one({"url": url}, doc)

    def find_document(self, url):
        return self.__col.find_one({"url" : url})

    def create_or_update_if_exist(self, url, html):

        if self.find_document(url) is not None:
            self.update_document(url, html)
        else:
            self.create_document(url, html)
