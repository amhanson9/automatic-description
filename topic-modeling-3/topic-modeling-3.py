"""
Copy of example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
with additional comments and some renaming and functions to make more sense to me.
Lesson 3 LDA Toipic Modeling
"""

# Demo started with this and then deleted it.
# Running the code gives message that the package is up to date, so may not need it every time.
# import nltk
# nltk.download("stopwords")

import numpy as np
import json
import glob

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
from nltk.corpus import stopwords
import pyLDAvis
import pyLDAvis.gensim


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def lemmatization(texts, allowed_postags=("NOUN", "ADJ", "VERB", "ADV")):
    """Reduce words to their base, to have less variation."""
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    texts_out = []
    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out


def gen_words(texts):
    """Reduce text to individual words and remove stop words."""
    final = []
    for text in texts:
        # deacc is removing accents.
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final


# Load English stopwords, which is a list of 179 terms (as of 1/12/2024) we'll ignore.
stopwords = stopwords.words("english")

# Load text part of the input file (JSON).
data = load_data("ushmm_dn.json")["texts"]

# Limit variations in the words. Makes the text more machine-readable, less human-readable.
# It is time consuming; expect it to take a few  minutes.
# TODO: untested. Didn't have time to run.
lemmatized_texts = lemmatization(data)

# Further clean up the words.
# TODO: untested.
data_words = gen_words(lemmatized_texts)

# Make a dictionary with word frequency and makes a list of tuples (corpus),
# where the first value is the index number of the word and the second is the word frequency.
# TODO: untested.
id2word = corpora.Dictionary(data_words)
corpus = []
for text in data_words:
    new = id2word.doc2bow(text)
    corpus.append(new)

# Make the model. Started with 30 topics, knowing that it is too many to demonstrate adjustments.
# TODO: untested.
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=30, random_state=100,
                                            update_every=1, chunksize=100, passes=10, alpha="auto")

# Vizualize the data.
# TODO: untested
pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
vis
