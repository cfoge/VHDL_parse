import os
import argparse

class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"




def search_log_files(directory, search_string):
    found_strings = []
    files_found = set()

    # Define the order of log files based on filename endings
    log_files_order = [
        "_synth.log",
        "_link.log",
        "_opt.log",
        "_place.log",
        "_route.log",
    ]

    # Function to get the index of suffix in log_files_order
    def get_suffix_index(filename):
        for i, suffix in enumerate(log_files_order):
            if filename.endswith(suffix):
                return i
        return len(log_files_order)  # Return a large index if no match found

    def check_suffix_in_string(string, suffix_list):
        for suffix in suffix_list:
            if suffix in string:
                return True
        return False

    # Iterate over the log files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".log"):
            if check_suffix_in_string(filename, log_files_order):
                files_found.add(filename)
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines):
                        if search_string in line:
                            found_strings.append((line, filename, line_number + 1))

    # Warn about missing log files
    missing_suffixes = []
    for suffix in log_files_order:
        matching_files = [file for file in files_found if file.endswith(suffix)]
        if not matching_files:
            missing_suffixes.append(suffix)

    if missing_suffixes:
        print(f"{color.YELLOW}Warning:{color.END} No log files found with suffixes: {', '.join(missing_suffixes)}")

    # Sort found strings based on log file order
    found_strings.sort(key=lambda x: get_suffix_index(x[1]))

    return found_strings


def main():
    parser = argparse.ArgumentParser(
        description="Search log files in a directory for a specific string."
    )
    parser.add_argument(
        "directory", nargs="?", type=str, default=None, help="Directory to search log files in."
    )
    parser.add_argument(
        "-d", "--dir", type=str, help="Directory to search log files in."
    )
    parser.add_argument(
        "-s", "--search", type=str, required=True, help="String to search for in the log files."
    )
    args = parser.parse_args()

    # Determine the directory path
    directory = args.directory if args.directory else args.dir
    if directory is None:
        print(f"{color.RED}Error:{color.END} No directory specified.")
        exit(1)

    search_string = args.search

    print("*******************************************")
    print(f"{color.GREEN}Searching log files in {directory} for '{search_string}'{color.END}")

    log_files_name = ["Synthesis", "Link", "Optimization", "Placement", "Routing"]
    log_files_order = [
        "_synth.log",
        "_link.log",
        "_opt.log",
        "_place.log",
        "_route.log",
    ]
    found_strings = search_log_files(directory, search_string)
    index = 0
    for log_type in log_files_order:
        print(f"\n{log_files_name[index]}:")
        for found_string in found_strings:
            if found_string[1].endswith(f"{log_type.lower()}"):
                highlight = {color.END}
                if "error" in found_string[0]:
                    highlight = {color.red}
                elif "warnning" in found_string[0]:
                    highlight = {color.YELLOW}
                print(f"{highlight}    {found_string[0]}{color.END}")  # found in '{found_string[1]}' at line {found_string[2]}'")
        index += 1


if __name__ == "__main__":
    main()
