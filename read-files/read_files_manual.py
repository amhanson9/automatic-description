"""Experiment with reading the contents of files into Python for topical analysis

Uses file extensions to decide which library to use to read the files.
For testing, reading plain text, Microsoft Word (doc and docx), and PDF.
Also including another file (.xps) that cannot be read by the script.

Parameter:
    input_directory (required): path to folder with files

Returns:
    A list, with each item being another list of the words (cleaned up) for a single document.
"""
from doc2docx import convert
import os
import docx2txt
import pandas as pd
from PyPDF2 import PdfReader
import re
import sys


def get_extension(path):
    """Calculate the lowercase version of the file extension

    :parameter
        path : path to a file (string)

    :return
        Lowercase version of the file extension (string)
        If there is no extension and no period in the path, it returns the entire path
    """
    path_list = path.split('.')
    ext = path_list[-1]
    ext_lower = ext.lower()
    return ext_lower


def read(path, ext):
    """Read the contents of a file by calling another function based on its file extension

     :parameter
         path : path to a file (string)
         ext : lowercase extension of the file (string)

     :return
         A list with the words, after cleanup, in the file or None if there is no library to read that extension
    """
    if ext == 'doc':
        text_list = read_doc(path)
    elif ext == 'docx':
        text_list = read_docx(path)
    elif ext == 'pdf':
        text_list = read_pdf(path)
    elif ext == 'txt':
        text_list = read_txt(path)
    else:
        text_list = None

    return text_list


def read_doc(path):
    """Read the contents of a file with a .doc extension and convert to a list by calling another function

    Temporarily making a .docx version because the methods for reading .doc are less well supported.

    :parameter
        path : path to a file (string)

    :return
        A list with the words, after cleanup, in the file
    """
    convert(path)
    new_path = path + 'x'
    text = docx2txt.process(new_path)
    text_list = text_to_clean_list(text)
    os.remove(new_path)
    return text_list


def read_docx(path):
    """Read the contents of a file with a .docx extension and convert to a list by calling another function

    :parameter
        path : path to a file (string)

    :return
        A list with the words, after cleanup, in the file
    """
    text = docx2txt.process(path)
    text_list = text_to_clean_list(text)
    return text_list


def read_pdf(path):
    """Read the contents of a file with a .pdf file extension and convert to a list by calling another function

    :parameter
        path : path to a file (string)

    :return
        A list with the words, after cleanup, in the file
    """
    text = ''
    reader = PdfReader(path)
    for page in reader.pages:
        page_text = page.extract_text()
        text += (' ' + page_text)
    text_list = text_to_clean_list(text)
    return text_list


def read_txt(path):
    """Read the contents of file with a .txt file extension and convert to a list by calling another function

    :parameter
        path : path to a file (string)

    :return
        A list with the words, after cleanup in the file
    """
    with open(path) as f:
        text = f.read()
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
                ['word', 'test', 'file', 'word', 'word', 'word', 'word', 'word'],
                ['another', 'word', 'test', 'file', 'test', 'file', 'test', 'file'],
                ['multiple', 'page', 'pd', 'f', 'page', '1',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text', 'line', 'text',
                 'multiple', 'page', 'page', '2', 'line', 'text', 'line', 'text', 'line', 'text'],
                ['first', 't', 'est', 'one', 'one', 'one', 'one', 'one', 'one'],
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
    remove_characters = ['.', '!', '?', ',', ';']
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

    # Starts variables for the text that is read and total number of texts.
    full_text = []
    number_texts = 0

    # Gets the path to each file in the input directory.
    for root, dirs, files in os.walk(input_directory):
        number_texts += len(files)
        for file in files:
            file_path = os.path.join(root, file)

            # Gets the file extension and tries to read based on the extension.
            extension = get_extension(file_path)
            file_text = read(file_path, extension)
            if file_text:
                full_text.append(file_text)

    # Calculates and prints the success rate of reading the files.
    success_rate(len(full_text), number_texts)

    # Test that test_input_directory gave the expected output.
    test_result()
