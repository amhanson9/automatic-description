"""Experiment with reading the contents of files into Python for topical analysis

For testing, want to read plain text, Microsoft Word (doc and docx), and PDF.

Parameters:
    input_directory (required): path to folder with files
"""
import os
import sys


def get_extension(path):
    """Calculate and return the lowercase version of the file extension."""
    path_list = path.split(".")
    ext = path_list[-1]
    ext_lower = ext.lower()
    return ext_lower


def success_rate(success, failure):
    """Calculate and print the number, and percent, of files that could be read."""
    total_files = success + failure
    percent_success = round((read_true / total_files) * 100, 2)
    print("\nSuccess rate for reading the documents:")
    print(f"{read_true} files out of {total_files} read ({percent_success}%)")


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
        print("Path is:", file_path)

        # Gets the file extension to determine which library to use.
        extension = get_extension(file_path)

        # Reads the file, if there is a library for that function, and updates the read count.

# Calculates and prints the success rate of reading the files.
success_rate(read_true, read_false)
