# automatic-description

Experiment in how to automatically describe born-digital archives for UGA, January-July 2024.

## parse-file-list

Completed proof of concept for extracting words from a text file that has the paths for a group of files.

## read-files

Completed proofs of concept for extracting words from files with the extension doc, docx, pdf, and txt.
Makes lowercase, removes punctuation and stop words and creates a list of word lists, one per document.
Also calculates the prints the reading success rate.
There are three versions of the script testing different methods: 
- manual: works for everything, but requires converting doc to docx first
- textract: works for docx and txt but getting errors for doc and pdf
- tika: works for everything, including the xps file added to test not being able to read something

## top2vec

Copy of example from YouTube tutorial by Dr. W.J.B. Mattingly.
Simpler way than his topic modeling series to cluster and get the most common words for each.

## topic-modeling-2

This is a copy from a YouTube tutorial by Dr. W.J.B. Mattingly that uses scikit-learn divide text from documents 
into 20 topical clusters, and creates a text file with the 10 most frequent words in each cluster.

The input text is already in one json file, but it is read into a list of strings 
where each string is the contents of one document.

## topic-modeling-3

This is a copy from a YouTube tutorial by Dr. W.J.B. Mattingly that uses gensim for an LDA analysis.

## topic-modeling-4

This is a copy from a YouTube tutorial by Dr. W.J.B. Mattingly that uses spacy for supervised learning.