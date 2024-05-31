import os
import re

# Define the path to scan and the replacement pattern
scan_directory = '.'
pattern = r'C:/BMD_builds/crc_error_fix'
replacement = 'Insert File path'

def replace_file_paths():
    for root, dirs, files in os.walk(scan_directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                file_content = f.read()
            
            # Replace the pattern
            new_content = re.sub(pattern, replacement, file_content)

            # Write the new content back to the file
            with open(file_path, 'w') as f:
                f.write(new_content)

if __name__ == "__main__":
    replace_file_paths()
