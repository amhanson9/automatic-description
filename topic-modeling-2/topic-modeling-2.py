"""
Copy of example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
with additional comments and some renaming and functions to make more sense to me.
Lesson 02.03 TF-IDF in Python with Scikit Learn
"""
import json
import os
import re
import string
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def load_json(file_path):
    """Read the json of the file at the provided path into a Python dictionary."""
    with open(file_path, "r", encoding="utf-8") as open_file:
        data_dictionary = json.load(open_file)
        return data_dictionary


def clean_one_description(text, stops):
    """Clean up a single description (string).
    Removes unique IDs, stop words, punctuation, numbers, and extra spaces."""

    # Remove unique identifiers from text, for example AC/2000/142.
    text = re.sub(r"AC\/\d{1,4}\/\d{1,4", "", text)

    # Remove all stop words (articles, conjunctions, etc.)
    # Tutorial said this is more verbose than necessary to be more clear. Did not show more concise way.
    words_list = text.split()
    cleaned_list = []
    for word in words_list:
        if word not in stops:
            cleaned_list.append(word)

    # Combine every item in the word list back into a single string.
    cleaned_description = " ".join(cleaned_list)

    # Remove all punctuation.
    cleaned_description = cleaned_description.translate(str.maketrans("", "", string.punctuation))

    # Remove all numbers.
    cleaned_description = "".join([i for i in cleaned_description if not i.isdigit()])

    # Remove extra spaces.
    # For as long as there are two consecutive spaces in the string, will replace 2 spaces with 1.
    while "  " in cleaned_description:
        cleaned_description = cleaned_description.replace("  ", " ")

    # Returns the cleaned description (string).
    return cleaned_description


def clean_descriptions(descriptions):
    """Clean up every description (string) in a list of descriptions."""

    # Update standard stops list with the months, for removing dates.
    # Stopwords are things like 'a', 'the', etc.
    stops = stopwords.words("english")
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    stops = stops + months

    # Iterate on every description in the list, clean it with a different function,
    # and add the cleaned version to a new list.
    cleaned_list = []
    for description in descriptions:
        cleaned_description = clean_one_description(description, stops)
        cleaned_list.append(cleaned_description)

    # Returns a list of the cleaned descriptions.
    return cleaned_list


def cluster(descriptions):
    """Divide the documents into 20 clusters based on word frequency."""

    # Customize vectorizer parameters to get better results.
    # max_df and min_df are the range of words to include; anything outside is too common or rare and excluded.
    # ngram = the number of words to consider as a phrase (bigram, trigram, etc.)
    vectorizer = TfidfVectorizer(lowercase=True, max_features=100, max_df=0.8, min_df=5, ngram_range=(1, 3),
                                 stop_words="english")
    vectors = vectorizer.fit_transform(descriptions)
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense()
    denselist = dense.tolist()

    # TODO: when have a smaller data set, print what this is doing to understand it
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
    # true_k is the number of clusters.
    true_k = 20
    model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)
    model.fit(vectors)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    return order_centroids, terms


def save_result(order_centroids, terms, true_k):
    """Save the 10 most frequent terms for each cluster to a text file."""

    # Document is named results.txt and saved to the same folder as the input data.
    with open(os.path.join("topic-modeling-2", "results.txt"), "w", encoding="utf-8") as f:

        # Make a block of text for each cluster.
        for i in range(true_k):
            f.write(f"Cluster {i}")
            f.write("\n")

            # Select the 10 most frequent terms for the cluster.
            for ind in order_centroids[i, :10]:
                f.write('-  %s' % terms[ind],)
                f.write("\n")
            f.write("\n")


# Read the descriptions from the input data, which is json, into a list.
# The json has two components, names and descriptions.
# Each description is a string with one or more sentences and may include an identifier.
descriptions_list = load_json(os.path.join("topic-modeling-2", "input_data.json"))["descriptions"]

# Remove portions of the descriptions which will interfere with the analysis,
# like stop words and punctuation.
descriptions_list = clean_descriptions(descriptions_list)

# Divide descriptions into 20 clusters.
clusters, terms = cluster(descriptions_list)

# Save the 10 most frequent terms for each cluster to a single text file.
save_result(clusters, terms, 20)
