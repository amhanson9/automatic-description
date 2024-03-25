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


def save_text(id, text_list):
    """Save the text to a text file for later analysis, with one line for each document's words"""
    with open(os.path.join(coll_directory, 'extracted_text', f'{id}_text.txt'), 'w') as f:
        for line_list in text_list:
            try:
                f.write(f'{"|".join(line_list)}\n')
            except UnicodeEncodeError:
                print('Skipped line, unicode issues')


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
    expected = [['file', 'skipped', '/docprops/thumbnailjpeg'],
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
    result_match = coll_text == expected

    if result_match is True:
        print("\nSuccess!")
    else:
        print("\nResults were not as expected. Texts that are not correct:")
        for index, text in enumerate(coll_text):
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
    coll_directory = sys.argv[1]

    # Makes a folder for script output in the coll_directory, if it doesn't already exist.
    # It is only likely to exist when running this script repeatedly for testing.
    if not os.path.exists(os.path.join(coll_directory, 'extracted_text')):
        os.mkdir(os.path.join(coll_directory, 'extracted_text'))

    # Starts variables for reading every file in the collection directory.
    coll_text = []
    coll_files = 0

    # For each AIP (first level folder within coll_directory),
    # finds and tries to read each file in that AIP.
    for aip in os.listdir(coll_directory):

        # Skip the output folder. During testing, each technique had a different output folder.
        if aip.startswith('extracted_text'):
            continue

        # Starts variables for reading every file in the AIP directory.
        aip_text = []
        aip_files = 0

        for root, dirs, files in os.walk(os.path.join(coll_directory, aip)):
            coll_files += len(files)
            aip_files += len(files)

            for file in files:
                file_path = os.path.join(coll_directory, aip, root, file)
                file_text = read(file_path)
                coll_text.append(file_text)
                aip_text.append(file_text)

        # Saves the AIP text to a file in coll_directory.
        save_text(aip, aip_text)

    # Saves the collection text to a file in coll_directory.
    save_text(os.path.basename(coll_directory), coll_text)

    # Calculates and prints the success rate of reading the files.
    success_rate(len(coll_text), coll_files)

    # Test that test_input_directory gave the expected output.
    # test_result()
