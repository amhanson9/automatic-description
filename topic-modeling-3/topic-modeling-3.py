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
from gensim.models import CoherenceModel
from gensim.models import TfidfModel

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
    """Reduce words to their root, to have less variation."""
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


def make_bigrams(texts):
    return [bigram[doc] for doc in texts]


def make_trigrams(texts):
    return [trigram[bigram[doc]] for doc in texts]


def sublist_sort(sub_li):
    """Sort the list based on index 1 (second item in the list)
    https://www.geeksforgeeks.org/python-sort-list-according-second-element-sublist/
    """
    sub_li.sort(key = lambda x: x[1])
    sub_li.reverse()
    return sub_li


# Load English stopwords, which is a list of 179 terms (as of 1/12/2024) we'll ignore.
stopwords = stopwords.words("english")

# Load text part of the input file (JSON).
data = load_data("ushmm_dn.json")["texts"]

# Limit variations in the words. Makes the text more machine-readable, less human-readable.
# It is time consuming; expect it to take a few  minutes.
lemmatized_texts = lemmatization(data)

# Further clean up the words.
data_words = gen_words(lemmatized_texts)

# Add bigrams and trigrams to the list of words, modified from www.machinelearningplus.com
bigrams_phrases = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigrams_phrases = gensim.models.Phrases(bigrams_phrases[data_words], threshold=100)
bigram = gensim.models.phrases.Phraser(bigrams_phrases)
trigram = gensim.models.phrases.Phrases(trigrams_phrases)

data_bigrams = make_bigrams(data_words)
data_bigrams_trigrams = make_trigrams(data_bigrams)

# TF-IDF removal of frequently occurring words, which usually are without subject meaning
# Does risk removing important words that are extremely frequent.
# Replaces the following code block from making the corpus from the earlier video (commented out).
# From https://stackoverflow.com/questions/24688116/how-to-filter-out-words-with-low-tf-idf-in-a-corpus-with-gensim/35951190
id2word = corpora.Dictionary(data_bigrams_trigrams)
corpus = [id2word.doc2bow(text) for text in data_bigrams_trigrams]
tfidf = TfidfModel(corpus, id2word=id2word)
low_value = 0.03
words = []
words_missing_in_tfidf = []
for i in range(0, len(corpus)):
    bow = corpus[i]
    tfidf_ids = [id for id, value in tfidf[bow]]
    bow_ids = [id for id, value in bow]
    low_value_words = [id for id, value in tfidf[bow] if value < low_value]
    drops = low_value_words + words_missing_in_tfidf
    for item in drops:
        words.append(id2word[item])
    words_missing_in_tfidf = [id for id in bow_ids if id not in tfidf_ids] # for score of 0
    new_bow = [b for b in bow if b[0] not in low_value_words and b[0] not in words_missing_in_tfidf]
    corpus[i] = new_bow


# # Make a dictionary with word frequency and makes a list of tuples (corpus),
# # where the first value is the index number of the word and the second is the word frequency.
# id2word = corpora.Dictionary(data_words)
# corpus = []
# for text in data_words:
#     new = id2word.doc2bow(text)
#     corpus.append(new)

# Make the model. Started with 30 topics, knowing that it is too many to demonstrate adjustments.
# Added the slice to corpus in 03.05 to show using part of your data to train and part, here the last doc, to test.
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus[:-1], id2word=id2word, num_topics=15, random_state=100,
                                            update_every=1, chunksize=100, passes=10, alpha="auto")

# Use model on additional text (the last document left out of initial training)
# new_vector has the topics sorted in order of most frequent.
test_doc = corpus[-1]
vector = lda_model[test_doc]
new_vector = sublist_sort(vector)

# Save the model and load back into memory under different name to show it works.
lda_model.save("test_model.model")
new_model = gensim.models.ldamodel.LdaModel.load("test_model.model")

# # Vizualize the data. This only works in Jupyter notebooks.
# pyLDAvis.enable_notebook()
# vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word, mds="mmds", R=30)
# vis
