import os
import filecmp


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
    directory1 = "//switcher-build2/users/robertj/rev_0x5_fix/fpga/src"
    directory2 = "//switcher-build2/users/robertj/am_300mhz_process/fpga/src"
    extensions = ".vhd"  # tuple(input("Enter file extensions separated by space (e.g., .vhd .vhdl): ").split())
    main(directory1, directory2, extensions)
