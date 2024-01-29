"""Experiment with reading the contents of files into Python for topical analysis

For testing, want to read plain text, Microsoft Word (doc and docx), and PDF.

Parameters:
    input_directory (required): path to folder with files
"""
import os
import docx2txt
import sys


def get_extension(path):
    """Calculate and return the lowercase version of the file extension."""
    path_list = path.split(".")
    ext = path_list[-1]
    ext_lower = ext.lower()
    return ext_lower


def read(ext):
    """Try to read the contents of a file based on its file extension and return as a list of words"""
    if ext == "docx":
        text = read_docx(file_path)
        return text
    elif ext == "txt":
        text = read_txt(file_path)
        return text
    else:
        return None


def read_docx(path):
    """Read the contents of docx files into a list of words and return"""
    text = docx2txt.process(path)
    text_list = text_to_clean_list(text)
    return text_list


def read_txt(path):
    """Read the contents of txt files into a list of words and return"""
    with open(path) as f:
        text = f.read()
    text_list = text_to_clean_list(text)
    return text_list


def success_rate(success, failure):
    """Calculate and print the number, and percent, of files that could be read."""
    total_files = success + failure
    percent_success = round((read_true / total_files) * 100, 2)
    print("\nSuccess rate for reading the documents:")
    print(f"{read_true} files out of {total_files} read ({percent_success}%)")


def text_to_clean_list(text_string):
    """Convert a string to a list of words, with some clean up."""

    # Replace new lines with spaces.
    text_string = text_string.replace("\n", " ")

    # Replace multiple consecutive spaces with a single space.
    while "  " in text_string:
        text_string = text_string.replace("  ", " ")

    # TODO: remove stop words and any other cleanup.
    text_string = text_string.replace(".", "")

    # Make all characters lowercase.
    text_string = text_string.lower()

    # Split the string at spaces.
    text_list = text_string.split(" ")
    return text_list


# Assigns script argument to a variable
input_directory = sys.argv[1]

# Starts a variable for the text that is read.
full_text = []

# Starts variables for calculating the success rate of reading the files.
read_true = 0
read_false = 0

# Gets the path to each file in the input directory.
for root, dirs, files in os.walk(input_directory):
    for file in files:
        file_path = os.path.join(root, file)

        # Gets the file extension and tries to read based on the extension.
        extension = get_extension(file_path)
        file_text = read(extension)
        if file_text:
            full_text.append(file_text)
            read_true += 1
        else:
            read_false += 1

# Calculates and prints the success rate of reading the files.
success_rate(read_true, read_false)

print(full_text)
