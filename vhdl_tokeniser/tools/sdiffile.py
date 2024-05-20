import os


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
    print(files_in_dir1_not_in_dir2)

    print("\nFiles in", dir2, "but not in", dir1, ":")
    print(files_in_dir2_not_in_dir1)


if __name__ == "__main__":
    dir1 = "//switcher-build2/users/robertj/rev_0x5_fix/broadcast_common/audio_meter_v2"  # input("Enter the path to the first directory: ")
    dir2 = "//switcher-build2/users/robertj/rev_0x5_fix/new/broadcast_common/audio_meter_v2"  # input("Enter the path to the second directory: ")

    compare_directories(dir1, dir2)
