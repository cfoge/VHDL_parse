import os
import argparse


def list_files(directory):
    """
    Recursively list all files in a directory.
    """
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.relpath(os.path.join(root, file), directory))
    return files_list


def compare_directories(dir1, dir2):
    """
    Compare files in two directories and list files present in one directory but not in the other.
    """
    dir1_files = set(list_files(dir1))
    dir2_files = set(list_files(dir2))

    files_in_dir1_not_in_dir2 = dir1_files - dir2_files
    files_in_dir2_not_in_dir1 = dir2_files - dir1_files

    print("Files in", dir1, "but not in", dir2, ":")
    for file in files_in_dir1_not_in_dir2:
        print(file)

    print("\nFiles in", dir2, "but not in", dir1, ":")
    for file in files_in_dir2_not_in_dir1:
        print(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare files in two directories.")
    parser.add_argument(
        "dir1", type=str, help="Path to the first directory."
    )
    parser.add_argument(
        "dir2", type=str, help="Path to the second directory."
    )
    args = parser.parse_args()

    compare_directories(args.dir1, args.dir2)
