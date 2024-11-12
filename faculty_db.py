#------------------------------------------------------------
# ENCAPSULATE DATABASE FUNCTIONS
#-----------------------------------------------------------*/

from pymongo import MongoClient

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017
COL_NAME = "professors"

class FacultyDatabase():

    def __init__(self):
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = client[DB_NAME]
            print("Connected to " + DB_NAME + " database, collection: " + COL_NAME)

        except:
            print("Database not connected successfully")
        
        self.__col = self.db[COL_NAME]

    def create_document(self, name, title, office, phone, email, website):

        doc = {"name": name,
               "title": title,
               "office": office,
               "phone": phone,
               "email": email,
               "website": website}
        
        self.__col.insert_one(doc)

    def update_document(self, name, title, office, phone, email, website):

        doc = {"$set": 
               {"name": name,
               "title": title,
               "office": office,
               "phone": phone,
               "email": email,
               "website": website}}

        self.__col.update_one({"name": name}, doc)

    def find_document(self, name):
        return self.__col.find_one({"name" : name})

    def create_or_update_if_exist(self, name, title, office, phone, email, website):

        if self.find_document(name) is not None:
            self.update_document(name, title, office, phone, email, website)
        else:
            self.create_document(name, title, office, phone, email, website)
