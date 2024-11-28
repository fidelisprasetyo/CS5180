#------------------------------------------------------------
# ENCAPSULATE DATABASE FUNCTIONS
#-----------------------------------------------------------*/

from pymongo import MongoClient

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017
COL_NAME = "terms"

class TermsDatabase():

    def __init__(self):
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = client[DB_NAME]
            print("Connected to " + DB_NAME + " database, collection: " + COL_NAME)

        except:
            print("Database not connected successfully")
        
        self.__col = self.db[COL_NAME]

    def create_document(self, term, pos, docs=[]):

        doc = {"term": term,
               "pos": pos,
               "docs" : docs}

        if self.find_document(term) is None:
            self.__col.insert_one(doc)

    
    def push_idf(self, term, doc_ref, idf):

        doc = {"$push": {
            "docs": {"doc:" : doc_ref, "idf": idf}
        }}

        self.__col.update_one({"term": term}, doc)

    def find_document(self, term):
        return self.__col.find_one({"term" : term})


