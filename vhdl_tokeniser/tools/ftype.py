import os
import sys
import glob
from pfind import search_files
## make version for constant, signal, variable  ,subtype , package, library (also search use)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ftype.py <search_term> [directory]")
        sys.exit(1)

    search_term = sys.argv[1]
    directory = sys.argv[2] 

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    found_files = search_files(search_term,'type', directory)

    if found_files:
        print("Files containing both search term and 'type' on the same line:")
        for file_name in found_files:
            print(file_name)
    else:
        print("No files found containing both search term and 'type' on the same line.")
        print(f"Directory = '{directory}'")
