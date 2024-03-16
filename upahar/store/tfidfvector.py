import math
from collections import Counter

def tokenize(document):
    # Tokenize the document by splitting it into individual words
    return document.split()

def calculate_tf(document):
    # Calculate the term frequency (TF) for each term in the document
    term_frequency = Counter(tokenize(document))
    total_terms = len(tokenize(document))
    tf = {term: freq/total_terms for term, freq in term_frequency.items()}
    return tf

def calculate_idf(documents):
    # Calculate the inverse document frequency (IDF) for each term
    total_documents = len(documents)
    all_tokens_set = set([token for doc in documents for token in tokenize(doc)])
    idf = {}
    for token in all_tokens_set:
        token_count = sum([1 for doc in documents if token in tokenize(doc)])
        idf[token] = math.log(total_documents / (1 + token_count))
    return idf

def calculate_tfidf(document, idf):
    # Calculate TF-IDF score for each term in the document
    tfidf = {}
    tf = calculate_tf(document)
    for term, tf_value in tf.items():
        tfidf[term] = tf_value * idf[term]
    return tfidf