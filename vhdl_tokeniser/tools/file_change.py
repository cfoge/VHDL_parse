import os
import time

# need to change this so it only checks the relivent vhdl files for a project

CHANGE_LOG_FILE = "change_log.txt"

def files_have_changed(directory):
    """
    Check if any files in the directory have changed since the last check.

    Args:
    - directory: The directory to check for file changes.
    """
    last_checked_time = load_last_checked_time()

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            modified_time = os.path.getmtime(file_path)
            if modified_time > last_checked_time:
                return True

    return False

def load_last_checked_time():
    """
    Load the last checked time from the change log file.
    If no previous time is stored, return a default value (e.g., 0).
    """
    if os.path.exists(CHANGE_LOG_FILE):
        with open(CHANGE_LOG_FILE, 'r') as file:
            last_checked_time = float(file.readline().strip())
    else:
        last_checked_time = 0
    return last_checked_time

def update_last_checked_time():
    """
    Update the last checked time in the change log file to the current time.
    """
    current_time = time.time()
    with open(CHANGE_LOG_FILE, 'w') as file:
        file.write(str(current_time))

if __name__ == "__main__":
    directory = "C:/Users/robertjo/Documents/FPGA_automation_scripts/find_in_project_tools"
    if files_have_changed(directory):
        print("Files have changed since the last check.")
     
    else:
        print("No files have changed since the last check.")

    update_last_checked_time()
