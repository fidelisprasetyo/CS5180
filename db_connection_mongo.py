#-------------------------------------------------------------------------
# AUTHOR: Fidelis Prasetyo
# FILENAME: db_connection_mongo
# SPECIFICATION: CRUD documents with pymongo
# FOR: CS 5180- Assignment #2
# TIME SPENT: 1 day
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries

from pymongo import MongoClient
import string

def connectDataBase():

    # Create a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    terms = []
    termCount = {}

    # create a dictionary (document) to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.

    for text in docText.split():
        term = text.translate(str.maketrans('', '', string.punctuation)).lower()
        termCount[term] = termCount.get(term, 0) + 1

    # create a list of dictionaries (documents) with each entry including a term, its occurrences, and its num_chars. Ex: [{term, count, num_char}]
    for term in termCount.keys():
        entry = {"term" : term, "count" : termCount[term], "num_char" : len(term)}
        terms.append(entry)

    #Producing a final document as a dictionary including all the required fields
    doc = {"_id": docId,
            "text": docText,
            "title": docTitle,
            "date": docDate,
            "category": docCat,
            "terms": terms}

    # Insert the document
    col.insert_one(doc)

def deleteDocument(col, docId):

    # Delete the document from the database
    col.detele_one({"_id": id})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    doc = {"$set": {
            "text": docText,
            "title": docTitle,
            "date": docDate,
            "category": docCat}}

    # Create the document with the same id
    col.update_one({"_id": docId}, doc)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3', ...}
    # We are simulating an inverted index here in memory.

    output = {}
    
    pipeline = [
        {"$unwind": {"path": "$terms"}},
        {"$sort": {"terms.term": 1}}]
    
    docs = col.aggregate(pipeline)

    for doc in docs:
        term = doc["terms"]["term"]
        title_count = doc["title"] + ": " + str(doc["terms"]["count"])

        if term not in output:
            output[term] = title_count
        else:
            output[term] += ", " + title_count

    return output
