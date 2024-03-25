"""Experiment with reading the contents of files into Python for topical analysis using textract library

For testing, want to read plain text, Microsoft Word (doc and docx), and PDF.

Parameters:
    input_directory (required): path to folder with files
"""
import os
import sys
import re
import textract


def read_file(path):
    """Reads the file and returns the text, and if there was an error"""

    # Starts variables for the function results.
    text = None
    read_error = False

    # If it works as expected, on a format that it can read.
    try:
        text = textract.process(path)
        text = text.decode("utf-8")

    # If it works as expected, on a format that it cannot read.
    except (ModuleNotFoundError, re.error):
        read_error = True

    # Some formats (currently doc and pdf) are not working and should be.
    except (FileNotFoundError, textract.exceptions.ShellError):
        read_error = True
        print("Can't find the file")

    return text, read_error


def success_rate(success, failure):
    """Calculate and print the number, and percent, of files that could be read."""
    total_files = success + failure
    percent_success = round((read_true / total_files) * 100, 2)
    print("\nSuccess rate for reading the documents:")
    print(f"{read_true} files out of {total_files} read ({percent_success}%)")


if __name__ == '__main__':
    # Assigns script argument to a variable
    coll_directory = sys.argv[1]

    # Starts a variable for the text that is read.
    full_text = []

    # Starts variables for calculating the success rate of reading the files.
    read_true = 0
    read_false = 0

    # For each AIP (first level folder within coll_directory),
    # finds and tries to read each file in that AIP.
    for aip in os.listdir(coll_directory):

        # Starts variables for reading every file in the AIP directory.
        aip_text = []
        aip_files = 0

        # Gets the path to each file in the input directory.
        for root, dirs, files in os.walk(os.path.join(coll_directory, aip)):
            for file in files:
                file_path = os.path.join(coll_directory, aip, root, file)
                # Reads the file and updates the read count.
                file_text, file_read_error = read_file(file_path)
                if file_read_error:
                    read_false += 1
                else:
                    full_text.append(file_text)
                    read_true += 1

    # Calculates and prints the success rate of reading the files.
    success_rate(read_true, read_false)
