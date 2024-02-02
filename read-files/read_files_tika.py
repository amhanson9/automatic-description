"""Experiment with reading the contents of files into Python for topical analysis using the tika library

For testing, want to read plain text, Microsoft Word (doc and docx), and PDF.
Also including another file (.xps) that don't expect to be read by the script, but Tika could read it.

Parameter:
    input_directory (required): path to folder with files

Returns:
    A list, with eaach item being another list of the words (cleaned up) for a single document.
"""
import os
import pandas as pd
import re
import sys
from tika import parser


def read(path):
    """Read the contents of a file

    :parameter
        path : path to a file (string)

    :return
        A list with the words, after cleanup, in the file
    """
    parsed = parser.from_file(path)
    text = parsed['content']
    text_list = text_to_clean_list(text)
    return text_list


def success_rate(success, total):
    """Calculate the number, and percent, of files that could be read and prints the result

    :parameter
        success : number of files with text in the full_text list (integer)
        total : number of files in the input directory (integer)

    :return
        None
    """
    percent_success = round((success / total) * 100, 2)
    print("\nSuccess rate for reading the documents:")
    print(f"{success} files out of {total} read ({percent_success}%)")


def test_result():
    """For the proof of concept, test that test_input_directory gives the expected result."""
    expected = [['test', 'file', 'text', 'test', 'test', 'test'],
                ['file', 'skipped', '/docprops/thumbnailjpeg'],
                ['word', 'test', 'file', 'word', 'word', 'word', 'word', 'word'],
                ['another', 'word', 'test', 'file', 'test', 'file', 'test', 'file'],
                ['multiple', 'page', 'page', '1',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'multiple', 'page', 'page', '2', 'line', 'text', 'line', 'text', 'line', 'text'],
                ['first', 'test', 'one', 'one', 'one', 'one', 'one', 'one'],
                ['second', 'test', 'file', 'two', 'two', 'two', 'two', 'two', 'two'],
                ['test', 'file', 'text', 'test', 'test', 'test']]
    result_match = full_text == expected

    if result_match is True:
        print("\nSuccess!")
    else:
        print("\nResults were not as expected. Texts that are not correct:")
        for index, text in enumerate(full_text):
            if not expected[index] == text:
                print("\nIndex position", index)
                print("Expected:", expected[index])
                print("Result:  ", text)


def text_to_clean_list(text_string):
    """Convert a string to a list of words, with some clean up

    Parameter:
        text_string : text contents of a file (string)

    Returns:
        List of words, lowercase and without stop words
    """
    # Makes all characters lowercase.
    text_string = text_string.lower()

    # Removes punctuation and other non-word characters to reduce the variation of words.
    # These cannot be removed as stop words because they are not entire words.
    remove_characters = ['.', '!', '?', ',', ';', '\r', '\t']
    for character in remove_characters:
        text_string = text_string.replace(character, '')

    # Makes a list of words by splitting the string at spaces and newlines, and then removing empty strings.
    text_list = re.split('[\n ]', text_string)
    text_list = [x for x in text_list if x]

    # Reads a CSV of default words to remove that do not indicate subjects, like "the", into a list.
    df = pd.read_csv(os.path.join(os.getcwd(), '..', 'parse-file-list', 'stop_list.csv'))
    stop_words = df['Term'].to_list()

    # Makes a list of every word in text_list that is not in stop_words.
    clean_text_list = []
    for word in text_list:
        if word not in stop_words:
            clean_text_list.append(word)

    return clean_text_list


if __name__ == '__main__':

    # Assigns script argument to a variable
    input_directory = sys.argv[1]

    # Starts variables for the text that is read and the total number of texts.
    full_text = []
    number_texts = 0

    # Gets the path to each file in the input directory and reads the file.
    for root, dirs, files in os.walk(input_directory):
        number_texts += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            file_text = read(file_path)
            full_text.append(file_text)

    # Calculates and prints the success rate of reading the files.
    success_rate(len(full_text), number_texts)

    # Test that test_input_directory gave the expected output.
    test_result()
