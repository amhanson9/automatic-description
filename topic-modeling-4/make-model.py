"""
Copy of example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
with additional edits to make more sense to me. Lesson 4 spaCy (part 1)
"""
from spacy.tokens import DocBin
from ml_datasets import imdb
import spacy


def make_docs(data):
    """
    Categorize documents as negative or positive based on second value of the tuple.
    Adapted from https://medium.com/analytics-vidhya/building-a-text-classifier-with-spacy-3-0-dd16e9979a
    """
    docs = []
    for doc, label in nlp.pipe(data, as_tuples=True):
        if label == "neg":
            doc.cats["positive"] = 0
            doc.cats["negative"] = 1
        else:
            doc.cats["positive"] = 1
            doc.cats["negative"] = 0
        docs.append(doc)
    return docs


# Load the small English model from spaCy
nlp = spacy.load("en_core_web_sm")

# Get labeled test data and splits into training and valid data sets.
# The data consists of tuples with the text from a review and then 'pos' or 'neg'.
train_data, valid_data = imdb()
num_texts = 500

train_docs = make_docs(train_data[:num_texts])
doc_bin = DocBin(docs=train_docs)
doc_bin.to_disk("train.spacy")

valid_docs = make_docs(valid_data[:num_texts])
doc_bin = DocBin(docs=valid_docs)
doc_bin.to_disk("valid.spacy")

