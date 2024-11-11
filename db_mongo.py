from pymongo import MongoClient
import string

def connectDataBase():
    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        print("Connected to " + DB_NAME + " database")
        return db

    except:
        print("Database not connected successfully")

def createDocument(col, url, html):

    doc = {"url": url, 
           "html": html}
    col.insert_one(doc)

def updateDocument(col, url, html):

    # Delete the document
    doc = {"$set": {
            "url": url,
            "html": html}}

    col.update_one({"url": url}, doc)

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