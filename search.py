import requests
import time
from bs4 import BeautifulSoup
import re
import lxml
import cchardet
import pickle
import numpy as np

print("Loading...")
with open('song_links.pkl', 'rb') as fp:
    song_links = pickle.load(fp)

with open('song_names.pkl', 'rb') as fp:
    song_names = pickle.load(fp)

def rank(docs): # Function for calculating tf-idf of all songs
    words_dict = {}
    n_docs = len(docs)

    # Dictionary with words in doc
    for i, doc in enumerate(docs):
        words = doc.split(' ')
        for word in words:
            if word not in words_dict:
                words_dict[word] = len(words_dict)

    n_words_set = len(words_dict)  # Number of unique words

    # empty 2d array of size n_docs x n_words_set
    tf = np.zeros((n_docs, n_words_set))

    s = 0.2
    tot_dl = 0

    # Calculate average document length
    for i in range(n_docs):
        tot_dl += len(words)
    avdl = tot_dl / n_docs

    # Calculate term frequency
    for i, doc in enumerate(docs):
        words = doc.split(' ')
        dl = len(words)
        tot_dl += dl
        for word in words:
            word_index = words_dict[word]
            if tf[i][word_index] == 0:
                tf[i][word_index] = 1
            tf[i][word_index] = ((1 + np.log10(1 + np.log10(tf[i][word_index]))) / ((1 - s) + s * (dl / avdl))) if dl > 0 else 0

    #calculate inverse document frequency
    idf = {}
    for word, index in words_dict.items():
        df = np.count_nonzero(tf[:, index])  # Number of documents containing the word

        idf[word] = np.log10((n_docs + 1) / df)

    tf_idf = {}

    #combine term frequency and inverse document frequency
    for word, index in words_dict.items():
        tf_idf[word] = tf[:, index] * idf[word]
    return tf_idf


def search_docs(tf_idf, query): # Function for allowing user to search through the tf-idf
    # Split query into separate words & lowercase all searches
    query_words = query.lower().split()
    relevance_scores = np.zeros(len(docs))

    for word in query_words:
        if word in tf_idf:
            relevance_scores += tf_idf[word]

    if np.sum(relevance_scores) == 0:
        return {"Sorry, no matching songs were found with your query!": ""}

    indexes = np.argsort(relevance_scores)[::-1][:5]
    # Return the top 5 most relevant documents
    return {song_names[i]: song_links[i] for i in indexes}

with open('song_dict.pkl', 'rb') as fp:
    docs = [x.lower() for x in pickle.load(fp)]

tf_idf = rank(docs)

print("Hello! Try out the music search engine! Type a song lyric, vibe, etc. and I will return the top 5 songs I think match!\n\n")
while(1):
    search_term = input("What do you want to search? Type 'q' to quit:\n")
    if(search_term == 'q'):
        exit(1)
    else:
        search_out = search_docs(tf_idf, search_term)
    print("\nYour search matched these songs:")
    print('\n'.join("{}: {}".format(k, v) for k, v in search_out.items()))
    print("\n")
