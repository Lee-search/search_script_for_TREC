from collections import Counter

# Delete duplication
def delete_duplication(p_list: list) -> list:

    p_new = []
    for p in p_list:
        if p not in p_new:
            p_new.append(p)

    return p_new

# Counting duplicate phrase
def get_phrase_counts(p: str, p_list: list) -> int:
    counter = Counter(p_list)
    return counter[p]

# Get should queries for Elasticsearch
# s: slop count, default value is 2.
def get_should_list(p_list: list, es_fields: list, s: int = 2) -> list:
    queries = []

    p_overlapped_list = p_list
    p_list = delete_duplication(p_list)

    for p in p_list:
        # p_count: duplicated count, it used boost options
        p_count = get_phrase_counts(p, p_overlapped_list)

        # es_fields[0]: title
        queries.append({"match_phrase": {es_fields[0]: {"query": p, "slop": s, "boost": p_count}}})
        queries.append({"match_phrase": {es_fields[0]: {"query": p, "slop": s * 10, "boost": p_count}}})

        # es_fields[1]: summary
        queries.append({"match_phrase": {es_fields[1]: {"query": p, "slop": s, "boost": p_count}}})
        queries.append({"match_phrase": {es_fields[1]: {"query": p, "slop": s * 10, "boost": p_count}}})

    return queries

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

# Return 1st sentence
def get_first_sent(text: str) -> str:
    return sent_tokenize(text)[0]

# Find and return only the words in the first sentence
def find_terms(text, words):
    return [ w for w in words if w in text ]