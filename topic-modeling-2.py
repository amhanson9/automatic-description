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


descriptions = load_data("data/trc_dn.json")["descriptions"]
names = load_data("data/trc_dn.json")["names"]