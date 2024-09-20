#-------------------------------------------------------------------------
# AUTHOR: Fidelis Prasetyo
# FILENAME: indexing.py
# SPECIFICATION: calculates the tf-idf to get the document-term matrix
# FOR: CS 5180- Assignment #1
# TIME SPENT: 
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])

print("Documents: ", documents)

#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
stopWords = {"i", "my", "she", "her", "he", "his", "they", "their", "and"}
filtered_docs = []

for d in documents:
    words = d.split()
    words = [word for word in words if word.lower() not in stopWords]
    filtered_docs.append(words)

print("After stopword removal: ", filtered_docs)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
stemming = {
    "cat" : "cat",
    "cats" : "cat",
    "dog" : "dog",
    "dogs" : "dog",
    "love" : "love",
    "loves" : "love",
    "loving" : "love",
    "loved" : "love"
}
stemmed_docs = []

for words in filtered_docs:
    words = [stemming[word] for word in words]
    stemmed_docs.append(words)
        
print("After stemming: ", stemmed_docs)

#Identifying the index terms.
terms = []
for d in stemmed_docs:
    for term in d:
        if term not in terms:
            terms.append(term)

print("Terms in this collection: ", terms)

#Building the document-term matrix by using the tf-idf weights.

def tf(d):
    tf_dict = {}
    terms_count = len(d)
    for term in terms:
        tf_dict[term] = 0   
    for term in d:
        tf_dict[term] += 1/terms_count
    return tf_dict

def df(D):
    df_dict = {}
    for d in D:
        for term in set(d):
            if term not in df_dict:
                df_dict[term] = 0
            df_dict[term] += 1
    return df_dict

def idf(D):
    idf_dict = {}
    size_of_D = len(D)
    df_dict = df(D)
    for term in df_dict:
        idf_dict[term] = math.log10(size_of_D/df_dict[term])
    return idf_dict

def tf_idf(D):
    tf_idf_dict = {}
    idf_dict = idf(D)
    for d in D:
        tf_dict = tf(d)
        tf_idf_dict[d] = []
        for term in terms:
            tf_idf_dict[d].append(tf_dict[term] * idf_dict[term])
    return tf_idf_dict

print(tf_idf(stemmed_docs))

#docTermMatrix = []

#Printing the document-term matrix.
#--> add your Python code here