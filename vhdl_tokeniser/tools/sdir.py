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
    "\033[0m",   # RESET
]


def print_directory_tree(folder_path, indent="", depth=0, find_string=None):
    """
    Print the directory tree structure for the given folder.

    Args:
    - folder_path: The path to the folder.
    - indent: Current indentation level for printing.
    - depth: Depth to control color cycling.
    - find_string: String to find in filenames and folder names.
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
        color = COLORS[0] if depth == -1 else COLORS[color_index]

        if os.path.isfile(item_path):
            if item.endswith(".vhd") or item.endswith(".vhdl"):
                if find_string and find_string in item:
                    print(f"\033[91m  \033[4m{indent}- {item}\033[0m")
                else:
                    print(f"{color}{indent}- {item}")
        elif os.path.isdir(item_path):
            if find_string and find_string in item:
                print(f"\033[91m \033[4m{indent}|- {item}\033[0m")
            else:
                print(f"{color}{indent}|- {item}")
            new_depth = depth + 1 if depth != -1 else -1
            print_directory_tree(item_path, indent + "|  ", new_depth, find_string)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print directory tree structure with optional features."
    )
    parser.add_argument(
        "directory", nargs="?", type=str, default=None, help="Directory to print the tree structure of."
    )
    parser.add_argument(
        "-d", "--dir", type=str, help="Directory to print the tree structure of."
    )
    parser.add_argument("-color", action="store_true", help="Enable colorized output.")
    parser.add_argument(
        "-find","-f", type=str, help="String to find in filenames and folder names."
    )
    args = parser.parse_args()

    # Determine the directory path
    folder_path = args.directory if args.directory else args.dir
    if folder_path is None:
        print("Error: No directory specified.")
        sys.exit(1)

    depth = 0 if args.color else -1
    find_string = args.find

    if not os.path.isdir(folder_path):
        print(f"Error: Directory '{folder_path}' does not exist.")
        sys.exit(1)

    print(f"Directory tree structure for '{folder_path}':")
    print_directory_tree(folder_path, "", depth, find_string)
