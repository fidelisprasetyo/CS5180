from pymongo import MongoClient
import string
from sklearn.feature_extraction.text import TfidfVectorizer


DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017
COL_NAME = "terms"

try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    print("Connected to " + DB_NAME + " database, collection: " + COL_NAME)
except:
    print("Database not connected successfully")

col = db[COL_NAME]
        


def cleanseString(d):
    d = d.translate(str.maketrans('','',string.punctuation)).lower()
    return d


d1 = "After the medication, headache and nausea were reported by the patient."
d2 = "The patient reported nausea and dizziness caused by the medication"
d3 = "Headache and dizziness are common effects of this medication."
d4 = "The medication caused a headache and nausea, but no dizziness was reported."

documents = [cleanseString(d1),cleanseString(d2),cleanseString(d3),cleanseString(d4)]

vectorizer = TfidfVectorizer()

tfidf = vectorizer.fit_transform(documents)

vocab = vectorizer.vocabulary_

inverted_index = {index: word for word, index in vocab.items()}

print(vocab)
print(inverted_index)
