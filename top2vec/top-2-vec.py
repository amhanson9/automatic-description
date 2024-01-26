import pandas as pd
from top2vec import Top2Vec

# Would need to make input.json for this to work.
df = pd.read_json("path/input.json")

# "descriptions" is a column in the dataframe in the example.
# It is a list of strings.
docs = df.descriptions.tolist()

# Cleans data, makes vectors, and finds topics efficiently.
model = Top2Vec(docs)

# How many documents in each topic, and how many total topics.
topic_sizes, topic_nums = model.get_topic_sizes()

# Most common words for the 10 most common topics.
# Zip is a way to iterate over more than one list at a time.
topic_words, word_scores, topic_nums = model.get_topics(10)
for words, num in zip(topic_words, topic_nums):
    print(num)
    print(f"Words: {words}")

# Get the text of the top 10 documents associated with topic 0.
# Score is similarity, with 1 being the highest.
documents, document_scores, document_ids = model.search_documents_by_topic(topic_num=0, num_docs=10)
for doc, score, doc_id in zip(documents, document_scores, document_ids):
    print(f"Document: {doc_id}, Score: {score}")
    print(doc)
    print()
    