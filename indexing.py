from pymongo import MongoClient
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pprint

def rem_punc_and_lower(d):
    d = d.translate(str.maketrans('','',string.punctuation)).lower()
    return d

# ---------------- database connection ----------------
DB_NAME = "CPP"
DB_HOST = "localhost"
DB_PORT = 27017

try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
except:
    print("Database not connected successfully")

docsDB = db["documents"]
termsDB = db["terms"]

# -----------------------------------------------------

# ----------------- documents and queries ----------------- 
d1 = "After the medication, headache and nausea were reported by the patient."
d2 = "The patient reported nausea and dizziness caused by the medication"
d3 = "Headache and dizziness are common effects of this medication."
d4 = "The medication caused a headache and nausea, but no dizziness was reported."

q1 = "nausea and dizziness"
q2 = "effects"
q3 = "nausea and reported"
q4 = "dizziness"
q5 = "the medication"

documents = [d1,d2,d3,d4]
queries = [q1,q2,q3,q4,q5]
# ---------------------------------------------------------- 

# build document database
docId = {}
for i, d in enumerate(documents):
    _id = docsDB.insert_one({"content": d})
    docId[i] =_id.inserted_id
    documents[i] = rem_punc_and_lower(documents[i])

# calculate tf-idf
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,3))
train = vectorizer.fit_transform(documents)

# get terms mapping 
vocabulary = vectorizer.vocabulary_
terms = vectorizer.get_feature_names_out()

# build inverted index database (terms-documents)
docs_idx, terms_idx = train.nonzero()   #indices with nonzero entries
for doc_idx,term_idx in zip(docs_idx, terms_idx):
    term = str(terms[term_idx])
    position = int(term_idx)
    doc_ref = docId[int(doc_idx)]
    idf = float(train[doc_idx, term_idx])

    if termsDB.find_one({"term":term}) is None:
        data = {
            "term": term,
            "position": position,
            "docs": [{
                "doc": doc_ref,
                "idf": idf
            }]
        }
        termsDB.insert_one(data)
    else:
        data = {"$push": {
            "docs": {
                "doc": doc_ref,
                "idf": idf
            }
        }}
        termsDB.update_one({"term":term}, data)

# calculate the scores (cosine similarity)
for q in queries:
    q_vector = vectorizer.transform([q])
    q_nonzero = vectorizer.inverse_transform(q_vector)[0]
    scores = {}

    for i in range(0,4):
        scores[i] = 0.0
        for term in q_nonzero:
            term_data = termsDB.find_one({"term": term})
            position = term_data["position"]
            q_idf = q_vector[0, position]

            for doc in term_data["docs"]:
                if doc["doc"] == docId[i]:
                    d_idf = doc["idf"]
                    scores[i] += (q_idf*d_idf)

    sorted_scores = sorted(scores.items(), key=lambda item:item[1], reverse=True)

    print("Query: " + q)
    for doc, score in sorted_scores:
        doc_id = docId[doc]
        content = docsDB.find_one({"_id":doc_id})["content"]
        print(content + ', ' + str(score))
    print('\n')