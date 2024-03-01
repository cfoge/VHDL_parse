import os
import sys
import glob

def search_files(search_term, type, directory='.'):
    """
    Search for .vhd or .vhdl files containing the given search term and file type on the same line
    in the specified directory.

    Args:
    - search_term: The term to search for within files.
    - type: The type of thing to search for, eg "type", constant,library,package ect .
    - directory: The directory to search within (default is the current directory).
    """
    file_list = []
    os.chdir(directory)
    for file_name in glob.glob('*.vhd') + glob.glob('*.vhdl'):
        if os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                for line in file:
                    print(".")
                    if search_term in line and type in line:
                        file_list.append(file_name)
                        break
    return file_list

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python pfind.py <search_term> {type} [directory]")
        sys.exit(1)

    search_term = sys.argv[1]
    type = sys.argv[2]
    directory = sys.argv[3] if len(sys.argv) > 3 else '.'

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    found_files = search_files(search_term, type, directory)

    if found_files:
        print(f"Files containing both search term and {type} on the same line:")
        for file_name in found_files:
            print(file_name)
    else:
        print(f"No files found containing both search term and {type}  on the same line.")
