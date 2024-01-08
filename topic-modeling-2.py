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

# Get key words for each document.
# Standard code from other sources. Can customize in different ways.
# max_df and min_df are the range of words to include; anything outside is too common or rare and excluded.
# ngram = the number of words to consider as a phrase (bigram, trigram, etc.)
vectorizer = TfidfVectorizer(lowercase=True, max_features=100, max_df=0.8, min_df=5, ngram_range=(1, 3), stop_words="english")
vectors = vectorizer.fit_transform(cleaned_docs)
feature_names = vectorizer.get_feature_names_out()
dense = vectors.todense()
denselist = dense.tolist()
all_keywords = []
for description in denselist:
    x = 0
    keywords = []
    for word in description:
        if word > 0:
            keywords.append(feature_names[x])
        x = x + 1
    all_keywords.append(keywords)

# Cluster key words from each document to see where there is overlap.
# true_k is the number of clusters. Change this number to get clusters that specify topics and don't overlap.
true_k = 20
model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)
model.fit(vectors)
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

# Save the clusters to a text file in the repo folder.
# Has the top 10 words in each cluster.
with open("data/trc_results.txt", "w", encoding="utf-8") as f:
    for i in range(true_k):
        f.write(f"Cluster {i}")
        f.write("\n")
        for ind in order_centroids[i, :10]:
            f.write(' %s' % terms[ind],)
            f.write("\n")
        f.write("\n")
        f.write("\n")

