"""
Copy of example from YouTube series Topic Modeling by Python Tutorials for Digital Humanities (Dr. W.J.B. Mattingly)
with additional edits to make more sense to me. Lesson 4 spaCy (part 2)
"""
import spacy
from ml_datasets import imdb

# To test on a file from the same data set. Change the index number to get a different one.
# It takes a few minutes to load.
# train_data, valid_data = imdb()
# text = train_data[3000]

# To test on supplied text, to skip loading the data and save time.
texts = [("First of all, this movie reminded me of movies I used to watch in school, and that's NOT a good thing. "
          "Basically, it's just preachy and pretentious, like other terrible series I could name. "
          "I'm not offended by the genre in general, but I am when they are extremely awful. "
          "Just avoid this if at all possible. I hated it.", "negative long movie"),
         ("This was my favorite thing I saw all year! Beautiful set, wonderful story, "
          "had me at the edge of my seat the whole time. I could not recommend this more. It was amazing. "
          "Go see it right now! It will be the best cinematic experience of your year, "
          "maybe even of your entire life", "positive long movie"),
         ("Chocolate is so yummy. It is smooth and tasty and smells so very good. "
          "This brand is superior to others in quality and ethically sourced. 10/10 would recommend. "
          "You won't regret giving this one a try. I'm sure you'll enjoy it too", "positive long food"),
         ("I loved this great movie.", "positive short movie")]

# Results from the best model
print("\nBest model:")
nlp = spacy.load("output/model-best")
for text in texts:
    doc = nlp(text[0])
    print(f"Text is {text[1]}, score is {doc.cats}")

# Results from the best model
print("\nLast model:")
nlp = spacy.load("output/model-last")
for text in texts:
    doc = nlp(text[0])
    print(f"Text is {text[1]}, score is {doc.cats}")
