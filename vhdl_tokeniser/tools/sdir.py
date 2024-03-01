import os
import sys

# ANSI escape codes for colors
COLORS = [
    '\033[97m',  # WHITE
    '\033[92m',  # GREEN
    '\033[94m',  # BLUE
    '\033[93m',  # YELLOW
    '\033[96m',  # CYAN
    '\033[95m',  # MAGENTA
    '\033[0m',   # RESET
]

def print_directory_tree(folder_path, indent='',depth=0):
    """
    Print the directory tree structure for the given folder..

    Args:
    - folder_path: The path to the folder.
    - indent: Current indentation level for printing.
    """
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if depth == -1:
            color_index = 0
            color = COLORS[0]
        else:
            color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
            color = COLORS[color_index]
        if os.path.isfile(item_path) and (item.endswith('.vhd') or item.endswith('.vhdl')):
            print(color + indent + '- ' + item)
        elif os.path.isdir(item_path):
            print(color+ indent + '|- ' + item)
            if depth == -1:
                new_depth = depth + 1
            else:
                new_depth = 0
            print_directory_tree(item_path, indent + '|  ',new_depth)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ftype.py <search_term> [directory]")
        sys.exit(1)

    folder_path = sys.argv[1]
    depth = -1 # make this come from the comand line as an optinal extra to use color

    if not os.path.isdir(folder_path):
        print(f"Error: Directory '{folder_path}' does not exist.")
    else:
        print(f"Directory tree structure for '{folder_path}':")
        print_directory_tree(folder_path,'',depth)
