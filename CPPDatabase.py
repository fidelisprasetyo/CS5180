from pymongo import MongoClient
import string

DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017

class CPPDatabase():

    def __init__(self):
        try:
            client = MongoClient(host=DB_HOST, port=DB_PORT)
            self.db = client[DB_NAME]
            print("Connected to " + DB_NAME + " database")

        except:
            print("Database not connected successfully")

    def create_document(self, col, url, html):

        doc = {"url": url, 
               "html": html}
        
        self.db[col].insert_one(doc)

    def update_document(self, col, url, html):

        doc = {"$set": {
                "url": url,
                "html": html}}

        self.db[col].update_one({"url": url}, doc)

    def create_or_update_if_exist(self, col, url, html):

        doc_exists = self.db[col].find_one({"url" : url}) is not None
        
        if doc_exists:
            self.update_document(col, url, html)
        else:
            self.create_document(col, url, html)
    
# def getIndex(col):

#     # Query the database to return the documents where each term occurs with their corresponding count. Output example:
#     # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
#     # We are simulating an inverted index here in memory.

#     output = {}
    
#     pipeline = [
#         {"$unwind": {"path": "$terms"}},
#         {"$sort": {"terms.term": 1}}]
    
#     docs = col.aggregate(pipeline)

#     for doc in docs:
#         term = doc["terms"]["term"]
#         title_count = doc["title"] + ": " + str(doc["terms"]["count"])

#         if term not in output:
#             output[term] = title_count
#         else:
#             output[term] += ", " + title_count

#     return output