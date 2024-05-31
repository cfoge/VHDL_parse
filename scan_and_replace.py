import os
import re

# Define the path to scan and the replacement pattern
scan_directory = '.'
patterns = [r'"[^"]*BMD[^"]*"', r'"[^"]*bmd[^"]*"', r'"[^"]*c:/[^"]*"', r'"[^"]*server[^"]*"']
replacement = '"Insert File path"'

def replace_file_paths():
    for root, dirs, files in os.walk(scan_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                # Replace the patterns
                new_content = file_content
                for pattern in patterns:
                    new_content = re.sub(pattern, replacement, new_content)

                # Write the new content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    replace_file_paths()
