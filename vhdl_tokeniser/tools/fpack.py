import os
import sys
import glob
import argparse
from pfind import search_files

search_type = "package"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=f"Search for a {search_type} by name within VHDL file directory."
    )
    parser.add_argument(
        "search_term", type=str, help="Term to search for within files."
    )
    parser.add_argument(
        "-d", "--directory", type=str, help="Directory to search within.", default="."
    )
    args = parser.parse_args()

    search_term = args.search_term
    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    print(
        f"Searching for {search_type} with '{search_term}' in directory: {directory}..."
    )
    found_files = search_files(search_term, search_type, directory)
