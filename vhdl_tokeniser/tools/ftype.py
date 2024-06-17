import os
import sys
import glob
import argparse
from pfind import search_files

## make version for constant, signal, variable  ,subtype , package, library (also search use)
search_type = "type"

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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print verbose output (prints the next few lines after it finds a match)",
    )

    args = parser.parse_args()

    search_term = args.search_term
    directory = args.directory
    verbose = args.verbose

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    print(
        f"Searching for {search_type} with '{search_term}' in directory: {directory}..."
    )
    found_files = search_files(search_term, search_type, directory, verbose)
