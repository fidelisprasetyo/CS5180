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

#store document database
docId = []
for i, d in enumerate(documents):
    _id = docsDB.insert_one({"content": d})
    docId.insert(i,_id.inserted_id)
    documents[i] = rem_punc_and_lower(documents[i])

#calculate tf-idf
vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1,3))
result = vectorizer.fit_transform(documents)

#store terms data and its position
vocabulary = vectorizer.vocabulary_
for term in vocabulary:
    term_obj = {
        "term": term,
        "pos": vocabulary[term],
        "docs": []
    }
    termsDB.insert_one(term_obj)

#iterate through all non-zero indices in the vector
terms = vectorizer.get_feature_names_out()
doc_idx, term_idx = result.nonzero()
for i,j in zip(doc_idx, term_idx):
    
    term_obj = {"$push": {
        "docs": {
            "doc": docId[int(i)],
            "idf": float(result[i,j]) }
        }}
    
    termsDB.update_one({"term": str(terms[j])}, term_obj)

q1_vector = vectorizer.transform([q1])
q1_nonzero = vectorizer.inverse_transform(q1_vector)[0] #return terms with nonzero entries

cosine_sim = cosine_similarity(q1_vector, result).flatten()
print(cosine_sim)

# #calculate cosine similarities for every query
# for q in queries:
#     q_vector = vectorizer.transform([q])
#     cosine_sim = cosine_similarity(q_vector, result).flatten()
#     print(cosine_sim)


