# automatic-description

Experiment in how to automatically describe born-digital archives for UGA, January-July 2024.

## parse-file-list

Completed proof of concept for extracting words from a text file that has the paths for a group of files.

## read-files

Draft proof of concept for extracting words from doc, docx, pdf, and text files.
Currently, it can get a byte string of the contents of doc and text but not docx or pdf.
Have not added word extraction or clean up yet.

## topic-modeling-2

This is a copy from a YouTube tutorial by Dr. W.J.B. Mattingly that uses scikit-learn divide text from documents 
into 20 topical clusters, and creates a text file with the 10 most frequent words in each cluster.

The input text is already in one json file, but it is read into a list of strings 
where each string is the contents of one document.

## topic-modeling-3

This is a copy from a YouTube tutorial by Dr. W.J.B. Mattingly that uses gensim and spacy for an LDA analysis.
It is not complete yet.