"""
Copy of example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
with additional edits to make more sense to me. Lesson 4 spaCy (part 4)
"""
import glob
import json
from gensim.models import Word2Vec
import gensim
from gensim.utils import simple_preprocess


def load_data(file):
    with open(file, "r", encoding="utf=8") as f:
        data = json.load(f)
    return data


def write_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# List for the final result.
final = []

# Gets all the files in a folder (at path) that ends in .txt
files = glob.glob("path/*.txt")

for file in files:
    # Take care of Windows slashes, so it doesn't cause problems
    file = file.replace("\\", "/")
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
        # Segments are based on double line break in the example.
        # You can split on whatever you want, e.g., punctuation.
        segments = text.split("\n\n")
        for segment in segments:
            # Makes a list of words, all lowercase, cleaned up.
            segment = simple_preprocess(segment, deacc=True)

            # Only includes segment if not super short.
            if len(segment) > 5:
                final.append(segment)

# Saves final result to a json file.
write_data("demo_segments.json", final)

# Read back what just saved, so have json, and make a vector model.
segments = load_data("demo_segments.json")
model = Word2Vec(segments, min_count=5)
model.save("demo.bin")

# Test the model. Get the top 10 words associated with hunger.
model = Word2Vec.load("demo.bin")
keyword = "hunger"
res = model.wv.similar_by_word(keyword, topn=10)
for item in res:
    # Item is  tuple, with the word and a number (didn't explain what it is. closeness?)
    print(item)

# List of keywords, based on the model and also own knowledge.
search_words = ["hunger", "starvation", "hungry", "starve", "starving", "malnutrition", "diarrhea", "dysentery",
                "potato", "bread", "rations"]

# If a segment contains any of the search words, label it as being about hunger (1)
# Said there is a better way to do this.
train_data = []
for segment in segments:
    match = False
    for word in search_words:
        if word in segment:
            match = True
    if match == True:
        segment = " ".join(segment)
        train_data.append((segment, 1))
write_data("demo_hunger_train.json", train_data)

# Load the hunger data back.
hunger_train = load_data("demo_hunger_train.json")
