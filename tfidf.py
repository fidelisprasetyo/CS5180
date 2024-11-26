import csv
import math
import string

documents = ["After the medication, headache and nausea were reported by the patient.", 
             "The patient reported nausea and dizziness caused by the medication",
             "Headache and dizziness are common effects of this medication.",
             "The medication caused a headache and nausea, but no dizziness was reported."]

def cleanseString(d):
    d = d.translate(str.maketrans('','',string.punctuation)).lower()
    return d

for i, d in enumerate(documents):
    documents[i] = cleanseString(d)

#Identifying the index terms.
#--> add your Python code here

terms = []
tokens = []

for i, doc in enumerate(documents):
    tokens.append(doc.split(" "))
    while '' in tokens[i]:
        tokens[i].remove('')
    for token in tokens[i]:
        if token not in terms:
            terms.append(token)

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here

for i, doc in enumerate(tokens):
    TF = []
    IDF = []
    TF_IDF = []
    for term in terms:
        TF = doc.count(term) / len(tokens[i])
        tokenSet = list(map(set, tokens)) #converting tokens to a set to eliminate duplicates
        wordsDocList = list(map(list, tokenSet)) #converting tokens back to a list to count occurrences
        DF = sum(x.count(term) for x in wordsDocList)
        IDF = math.log(len(tokens) / DF, 10)
        TF_IDF.append(TF * IDF)

#Printing the document-term matrix.
#--> add your Python code here
