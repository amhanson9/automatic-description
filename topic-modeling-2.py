"""
Example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
Lesson 02.03 TF-IDF in Python with Scikit Learn
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import string
from nltk.corpus import stopwords
import json
import glob
import re


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data


def write_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def remove_stops(text, stops):
    """Clean up a single document. Remove unique IDs, stop words, punctuation, numbers, and extra spaces."""

    # Remove unique identifiers from text, for example AC/2000/142.
    text = re.sub(r"AC\/\d{1,4}\/\d{1,4", "", text)

    # Remove all stop words (articles, conjunctions, etc.)
    # Said this is more verbose than necessary to be more clear. Did not show more concise way.
    words = text.split()
    final = []
    for word in words:
        if word not in stops:
            final.append(word)
    final = " ".join(final)

    # Remove punctuation
    final = final.translate(str.maketrans("", "", string.punctuation))

    # Remove numbers
    final = "".join([i for i in final if not i.isdigit()])

    # Remove extra spaces
    while "  " in final:
        final = final.replace("  ", " ")

    return final


def clean_docs(docs):
    """Clean up every document."""

    # Update standard stops list with the months, for removing dates.
    stops = stopwords.words("english")
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    stops = stops + months

    # Iterate on every document and add the cleaned version to a list.
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc, stops)
        final.append(clean_doc)
    return final


# Read the data set, which contains two data types - descriptions and names.
descriptions = load_data("data/trc_dn.json")["descriptions"]
names = load_data("data/trc_dn.json")["names"]

# Clean up the descriptions.
cleaned_docs = clean_docs(descriptions)
print(descriptions[0])
print(cleaned_docs[0])
