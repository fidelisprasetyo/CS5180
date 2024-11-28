#------------------------------------------------------------
# ENCAPSULATE DATABASE FUNCTIONS
#-----------------------------------------------------------*/

from pymongo import MongoClient

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017
COL_NAME = "documents"

class DocumentsDatabase():

    def __init__(self):
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = client[DB_NAME]
            print("Connected to " + DB_NAME + " database, collection: " + COL_NAME)

        except:
            print("Database not connected successfully")
        
        self.__col = self.db[COL_NAME]

    def create_document(self, content):

        doc = {"content": content}
        
        return self.__col.insert_one(doc)

    # def update_document(self, id, content):

    #     doc = {"$set": 
    #            {"content": content}}

    #     self.__col.update_one({"_id": id}, doc)

    # def find_document(self, id):
    #     return self.__col.find_one({"_id" : id})

    # def create_or_update_if_exist(self, id, content):

    #     if self.find_document(id) is not None:
    #         self.update_document(id, content)
    #     else:
    #         self.create_document(id, content)
