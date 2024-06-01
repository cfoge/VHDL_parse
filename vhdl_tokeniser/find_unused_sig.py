import os
import argparse
from token_test import parse_vhdl  # Adjust the import if needed

COLORS = [
    "\033[97m",  # WHITE
    "\033[92m",  # GREEN
    "\033[94m",  # BLUE
    "\033[93m",  # YELLOW
    "\033[96m",  # CYAN
    "\033[95m",  # MAGENTA
    "\033[0m",  # RESET
]

def find_string_matches(file_path, search_string):
    """
    Find occurrences of a string in a text document and return the number of matches and the lines where the matches are found.

    Args:
        file_path (str): The path to the text document.
        search_string (str): The string to search for.

    Returns:
        tuple: A tuple containing the number of matches found and a list of lines where the matches are found.
    """
    # Initialize variables
    match_count = 0
    matched_lines = []

    # Open the text document
    with open(file_path, "r") as file:
        # Iterate through each line in the file
        for line_number, line in enumerate(file, start=1):
            # Check if the search string is in the line
            if search_string in line:
                match_count += line.count(search_string)
                matched_lines.append((line_number, line.strip()))

    return match_count, matched_lines

def main():
    parser = argparse.ArgumentParser(description='Search a VHDL file for declared but unused signals.')
    parser.add_argument('file_path', type=str, help='Path to the VHDL file to be analyzed.')
    args = parser.parse_args()

    # Parse the VHDL file
    target_vhdl = parse_vhdl(args.file_path)
    signals = target_vhdl.signal

    for signal in signals:
        num_strings_match, num_line_match = find_string_matches(args.file_path, signal[0])
        if num_strings_match < 2:
            if len(num_line_match) > 0:
                print(
                    f"{COLORS[1]}{signal[0]}{COLORS[6]} found in file {num_strings_match} time(s). line {COLORS[1]}{num_line_match[0][0]}{COLORS[6]}"
                )

if __name__ == "__main__":
    main()
