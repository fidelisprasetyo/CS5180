from pymongo import MongoClient
import datetime

def connectDataBase():

    # Creating a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createDocument(col, id, text, title, date, category):

    doc = {"_id": id,
            "text": text,
            "title": title,
            "date":  date,
            "category": category}
    
    col.insert_one(doc)

def updateDocument(col, id, text, title, date, category):

    doc = {"$set": {
            "text": text,
            "title": title,
            "date": date,
            "category": category}}
    
    col.update_one({"_id": id}, doc)

def deleteDocument(col, id):

    col.detele_one({"_id": id})

def getIndex(col):
    
    pipeline = [{"$split": {}}]


    for doc in col.find():
        termcount = {}
        for term in doc["text"].split():
            lterm = term.lower()
            termcount[lterm] = termcount.get(lterm, 0) + 1
        print(termcount)