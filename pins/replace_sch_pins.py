import sys

def process_files(file1_path, file2_path, marker):
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        lines_file1 = f1.readlines()
        lines_file2 = f2.readlines()

    output_lines = []

    for line1 in lines_file1:
        replaced = False

        for line2 in lines_file2:
            # Extract strings within curly braces
            match1 = get_string_in_braces(line1)
            match2 = get_string_in_braces(line2)

            # Check if strings match and if line1 contains the marker
            if match1 is not None and match2 is not None and match1 == match2 and marker in line1:
                output_lines.append(line2)
                replaced = True
                break

        if not replaced:
            output_lines.append(line1)

    with open(file1_path, 'w') as f1:
        f1.writelines(output_lines)

def get_string_in_braces(line):
    start_index = line.find('{')
    end_index = line.find('}')
    
    if start_index != -1 and end_index != -1 and start_index < end_index:
        return line[start_index + 1:end_index].strip()
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("This script puts pin locations from pin locations in the contraints file made by make_xdc.py with locations from get_sch_loc.py")
        print("Usage: python replace_sch_pins.py <contraints.xdc> matched_pins_with_sch.xdc XXX")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    marker = sys.argv[3]

    process_files(file1_path, file2_path, marker)
