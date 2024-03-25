"""Experiment with reading the contents of files into Python for topical analysis using textract library

For testing, want to read plain text, Microsoft Word (doc and docx), and PDF.

Parameters:
    input_directory (required): path to folder with files
"""
import os
import pandas as pd
import sys
import re
import textract


def read_file(path):
    """Reads the file and returns the text, and if there was an error"""

    text = None

    # If it works as expected, on a format that it can read.
    try:
        text = textract.process(path)
        text = text.decode("utf-8")
        text = text_to_clean_list(text)
    # If it works as expected, on a format that it cannot read.
    except (ModuleNotFoundError, re.error):
        print('Format cannot be read', path)
    # Unicode errors: solution tbd
    except UnicodeDecodeError:
        print('Unicode error', path)
    # Some formats (currently doc and pdf) are not working and should be.
    except (FileNotFoundError, textract.exceptions.ShellError):
        print('Path error', path)

    return text


def save_text(id, text_list):
    """Save the text to a text file for later analysis, with one line for each document's words"""
    with open(os.path.join(coll_directory, 'extracted_text', f'{id}_text.txt'), 'w') as f:
        for line_list in text_list:
            try:
                f.write(f'{"|".join(line_list)}\n')
            except UnicodeEncodeError:
                print('Skipped line, unicode issues')


def success_rate(folder, success, total):
    """Calculate the number, and percent, of files that could be read and prints the result

    parameter
        folder : name of the folder the success rate applies to (string)
        success : number of files with text in the full_text list (integer)
        total : number of files in the input directory (integer)

    return
        None
    """
    percent_success = round((success / total) * 100, 2)
    print(f"\nSuccess rate for {folder}:")
    print(f"{success} files out of {total} read ({percent_success}%)")


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

        # Gets the path to each file in the input directory.
        for root, dirs, files in os.walk(os.path.join(coll_directory, aip)):
            coll_files += len(files)
            aip_files += len(files)

            for file in files:
                file_path = os.path.join(coll_directory, aip, root, file)
                # Reads the file and updates the read count.
                file_text = read_file(file_path)
                if file_text:
                    coll_text.append(file_text)
                    aip_text.append(file_text)

        # Saves the AIP text to a file in coll_directory.
        save_text(aip, aip_text)

        # Calculates and prints the success rate of reading the files for the AIP.
        success_rate(aip, len(aip_text), aip_files)

    # Saves the collection text to a file in coll_directory.
    save_text(os.path.basename(coll_directory), coll_text)

    # Calculates and prints the success rate of reading the files for the entire collection.
    success_rate(os.path.basename(coll_directory), len(coll_text), coll_files)
