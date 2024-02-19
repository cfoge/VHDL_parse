import os
import sys


def print_directory_tree(folder_path, indent=''):
    """
    Print the directory tree structure for the given folder..

    Args:
    - folder_path: The path to the folder.
    - indent: Current indentation level for printing.
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and (item.endswith('.vhd') or item.endswith('.vhdl')):
            print(indent + '- ' + item)
        elif os.path.isdir(item_path):
            print(indent + '|- ' + item)
            print_directory_tree(item_path, indent + '|  ')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ftype.py <search_term> [directory]")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: Directory '{folder_path}' does not exist.")
    else:
        print(f"Directory tree structure for '{folder_path}':")
        print_directory_tree(folder_path)
