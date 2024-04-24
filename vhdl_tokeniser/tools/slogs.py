import os

def search_log_files(directory, search_string):
    found_strings = []

    # Define the order of log files based on filename endings
    log_files_order = ['_synth.log', '_link.log', '_opt.log', '_place.log', '_route.log']

    # Function to get the index of suffix in log_files_order
    def get_suffix_index(filename):
        for i, suffix in enumerate(log_files_order):
            if filename.endswith(suffix):
                return i
        return len(log_files_order)  # Return a large index if no match found
    
    def check_suffix_in_string(string, suffix_list):
        for suffix in suffix_list:
            if suffix in string:
                return True
        return False

    # Iterate over the log files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.log'):
            if check_suffix_in_string(filename, log_files_order):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    lines = file.readlines()
                    for line_number, line in enumerate(lines):
                        if search_string in line:
                            found_strings.append((line, filename, line_number + 1))

    # Sort found strings based on log file order
    found_strings.sort(key=lambda x: get_suffix_index(x[1]))

    return found_strings

def main():
    directory = "//switcher-build2/users/robertj/smartview_regs_2/fpga/syn"
    search_string = "ossigh_out"

    print("*******************************************")
    print(f"Searching log files in {directory} for '{search_string}'")

    log_files_name = ['Synthesis', 'Link', 'Optimization', 'Placement', 'Routing']
    log_files_order = ['_synth.log', '_link.log', '_opt.log', '_place.log', '_route.log']
    index = 0
    for log_type in log_files_order:
        print(f"\n{log_files_name[index]}:")
        found_strings = search_log_files(directory, search_string)
        index = index + 1
        for found_string in found_strings:
            if found_string[1].endswith(f'{log_type.lower()}'):
                print(f"    {found_string[0]}")#found in '{found_string[1]}' at line {found_string[2]}")

if __name__ == "__main__":
    main()
