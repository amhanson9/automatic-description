"""Experiment with converting a text file with paths to a list of words.

For initial testing, using a single text file, with path provided as an argument.
Real data may be multiple text files in a single folder
or may need to search a folder recursively for text files that match a naming convention.

Parameters:
    path_doc (required) : the path to the text file with the directory print
    skip_number (required) : the number of spaces at the beginning of each path to not include
"""
import os
import pandas as pd
import re
import sys


def doc_to_lines_list(doc):
    """Convert a text file into a list with one item (string) per row."""
    with open(doc) as doc_open:
        doc_list = doc_open.read().splitlines()
    return doc_list


def path_to_words_list(row):
    """Convert a path (string) to a list of words/strings."""

    # Splits on dashes, underscores, spaces, periods, and backslashes.
    row_list = re.split(r'[-_ .\\]', row)

    # Removes the specified number of items from the beginning of the list that are the same for every path.
    row_list = row_list[skip_number:]

    # Makes every item in the list lowercase.
    row_list = [item.lower() for item in row_list]

    return row_list


def remove_stop_words(list_words):
    """Remove stop words from the word list."""

    # Reads the stop words, which are in the "Term" column of the stop_list.csv file in this repo.
    df = pd.read_csv(os.path.join(os.getcwd(), 'stop_list.csv'))
    stop_words = df['Term'].to_list()

    # Makes a list of every word that is not in stop_words.
    reduced_words = []
    for word in list_words:
        if word not in stop_words:
            reduced_words.append(word)
    return reduced_words


if __name__ == '__main__':

    # Assigns script arguments to variables.
    path_doc = sys.argv[1]
    skip_number = int(sys.argv[2])

    # Reads the text file into a list.
    path_list = doc_to_lines_list(path_doc)

    # Splits each path into a list of words and adds them to the word list.
    word_list = []
    for path in path_list:
        words = path_to_words_list(path)
        word_list.extend(words)

    # Removes common words and strings that do not indicate subjects, like "the" and file extensions.
    word_list = remove_stop_words(word_list)

    # Just for proof of concept: prints the result for using example_paths.txt as the input.
    expected = ['formats', 'file', 'format', 'desktop', 'recommendations', '2022', 'held', 'trust', 'report', 'held',
                'trust', 'report', '2']
    print("\nMatch expected list?", word_list == expected)
