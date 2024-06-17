import os
import sys
import argparse

# ANSI escape codes for colors
COLORS = [
    "\033[97m",  # WHITE
    "\033[92m",  # GREEN
    "\033[94m",  # BLUE
    "\033[93m",  # YELLOW
    "\033[96m",  # CYAN
    "\033[95m",  # MAGENTA
    "\033[0m",  # RESET
]


def search_files(search_term, type_to_search, directory=".", verbose=False):
    """
    Search for .vhd or .vhdl files containing the given search term and type on the same line
    in the specified directory and its subdirectories.

    Args:
    - search_term: The term to search for within files.
    - type_to_search: The type of thing to search for, e.g., "type", constant, library, package, etc.
    - directory: The directory to search within (default is the current directory).
    """
    file_list = []
    error_list = []
    number_files_checked = 0
    verbose_line_num = 8

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".vhd") or file_name.endswith(".vhdl"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    number_files_checked += 1
                    try:
                        for line_number, line in enumerate(file, 1):

                            if search_term in line and type_to_search in line:
                                if (
                                    verbose == True
                                ):  # this is a terrible way to do this, is it worth doing it better?
                                    print(
                                        f"{COLORS[1]}{file_path} {COLORS[0]} : \n   {line_number}: {line.strip()}\033[0m"
                                    )

                                    for line_number_new, line_new in enumerate(
                                        file, line_number
                                    ):
                                        if (line_number_new > line_number) and (
                                            line_number_new
                                            < (line_number + verbose_line_num)
                                        ):
                                            print(
                                                f"   {line_number_new+1}: {line_new.strip()}"
                                            )
                                else:
                                    print(
                                        f"{COLORS[1]}{file_path} {COLORS[0]} : line {line_number}: {line.strip()}\033[0m"
                                    )
                                file_list.append(file_path)
                                break
                    except:
                        # error_list.append() # add exception catcher
                        x = 1
    print(f"Info: {number_files_checked} files checked.")
    return file_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a term within VHDL files.")
    parser.add_argument(
        "search_term", type=str, help="Term to search for within files."
    )
    parser.add_argument("type_to_search", type=str, help="Type of thing to search for.")
    parser.add_argument(
        "-d", "--directory", type=str, help="Directory to search within.", default="."
    )
    args = parser.parse_args()

    search_term = args.search_term
    type_to_search = args.type_to_search
    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    found_files = search_files(search_term, type_to_search, directory)

    if not found_files:
        print(
            f"{COLORS[0]}No files found containing both search term and '{type_to_search}' on the same line.\033[0m"
        )
