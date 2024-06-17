import os
import argparse


def find_files(directory, extensions):
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extensions):
                found_files.append(os.path.join(root, file))
    return found_files


def compare_files(files1, files2):
    for file1 in files1:
        for file2 in files2:
            filename1 = os.path.basename(file1)
            filename2 = os.path.basename(file2)
            if filename1 == filename2:
                with open(file1, "r") as f1, open(file2, "r") as f2:
                    content1 = f1.read()
                    content2 = f2.read()
                    if content1 == content2:
                        # print(f"{file1} and {file2} have identical contents")
                        x = 1
                    else:
                        print(f"{file1} and {file2} have different contents")


def main(dir1, dir2, extensions):
    files1 = find_files(dir1, extensions)
    files2 = find_files(dir2, extensions)
    compare_files(files1, files2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare files in two directories.")
    parser.add_argument(
        "dir1", type=str, help="Path to the first directory."
    )
    parser.add_argument(
        "dir2", type=str, help="Path to the second directory."
    )
    parser.add_argument(
        "-e", "--extensions", type=str, default=".vhd", help="File extensions to search for."
    )
    args = parser.parse_args()

    extensions = tuple(args.extensions.split())
    main(args.dir1, args.dir2, extensions)
