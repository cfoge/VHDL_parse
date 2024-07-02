import re
import sys

## This script takes a Mentor Graphics netlist and creates a VHDL TLD from it given the designator of the FPGA (e.g., u17). This can be used to create a TLD or as part of checking pins, constraints, etc.

def extract_text_between_single_quotes(text):
    pattern = r"'(.*?)'"
    match = re.search(pattern, text, flags=re.DOTALL)
    if match:
        return match.group(1).replace(' ', '').replace('\n', '')
    else:
        return ""

def extract_text_between_space_dash_quotes(text):
    pattern = r"' (.*?)-"
    match = re.search(pattern, text, flags=re.DOTALL)
    if match:
        return match.group(1).replace(' ', '').replace('\n', '')
    else:
        return ""

def extract_res(text):
    # Use regex to find all substrings starting with " r" and ending with "-"
    pattern = r" r(.*?)-"
    matches = re.findall(pattern, text)
    # Prepend "r" to each match
    segments = [f"r{match}" for match in matches]
    return segments

def remove_duplicates(input_list):
    seen = set()
    result = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def rearrange_and_group_strings(strings):
    # Step 1: Split the strings into three groups based on whether they contain "debug", " in ", " out ", or " inout "
    contains_debug = [s for s in strings if "debug" in s]
    contains_clk_vcxo = [s for s in strings if s not in contains_debug and ("clk" in s or "vcxo" in s)]
    remaining_strings = [s for s in strings if s not in contains_debug + contains_clk_vcxo]

    # Sort strings containing " in ", " out ", and " inout "
    def sort_in_out_inout(s):
        if " in " in s:
            return 0
        elif " out " in s:
            return 1
        elif " inout " in s:
            return 2
        else:
            return 3

    contains_clk_vcxo.sort(key=sort_in_out_inout)
    remaining_strings.sort(key=sort_in_out_inout)

    # Step 2: Sort all remaining strings in alphabetical order ignoring everything before and including the first "_"
    contains_clk_vcxo.sort(key=lambda x: x.split('_', 1)[-1])
    remaining_strings.sort(key=lambda x: x.split('_', 1)[-1])

    # Step 3: Group strings based on the substring between the first and second "_"
    grouped_strings = {}
    for s in remaining_strings:
        key = s.split('_')[1]  # Get the substring between the first and second "_"
        grouped_strings.setdefault(key, []).append(s)

    # Combine strings containing "clk" or "vcxo" with the grouped strings
    result = contains_clk_vcxo + [item for sublist in grouped_strings.values() for item in sublist] + contains_debug
    return result

if not ((len(sys.argv) == 4)): # Check for correct number of arguments
    print('This script needs 2 inputs, new file name and the netlist file')
    print('example: tld_name netlist.txt u12')
    sys.exit(1)

filename = sys.argv[1]
netlist_filename = sys.argv[2] 
chip_id = sys.argv[3] 

try:
    with open(netlist_filename) as f:
        netlist = f.readlines()
except:
    print("Error opening netlist file!!! Check if the file exists and matches the name/path given")

pin_list = []
possible_pin_list = []
print()
print(f"Searching {netlist_filename} for nets connected to {chip_id}")

# Define search patterns and their corresponding VHDL declarations
search_patterns = {
    "plo_": "out   std_logic;",
    "pli_": "in    std_logic;",
    "plio_": "inout std_logic;",
    "pado_": "out   std_logic;",
    "padi_": "in    std_logic;",
    "padio_": "inout std_logic;",
    "sdi_": "{in/out/inout} std_logic;",
    "sfp_": "{in/out/inout} std_logic;",
    "lcd_": "{in/out/inout} std_logic;",
    "eth_": "{in/out/inout} std_logic;"
}

for line in netlist:
    if(("net") in line.lower()) and (("flatnet") not in line.lower()): 
        chip_id = chip_id.lower()
        line_lc = line.lower()    
        if (chip_id in line_lc):
            signal_name = extract_text_between_single_quotes(line)
            signal_name = f"{str(signal_name):<25}"
            for pattern, vhdl_decl in search_patterns.items():
                if pattern in line_lc:
                    pin_list.append(f'{signal_name.lower()} : {vhdl_decl}')
                    break
            else: # Look for pins connected to the FPGA that don't have PL in the signal name
                signal_name = extract_text_between_single_quotes(line)
                resistors = line.lower().count(' r')
                if 'r' in line.lower(): # If there is a resistor connected to the FPGA, add it as a possible pin
                    resistors = extract_res(line.lower())
                    for res in resistors:
                        possible_pin_list.append([signal_name.lower(), res])

if len(possible_pin_list) > 0: # Now check all the pins on the FPGA that are connected to resistors and see if any of those resistors are connected to a net with a prefix we are interested in
    pins_with_res_inseries = []
    for line in netlist:
        for possible_pin in possible_pin_list:
            linelower = line.lower()
            test2 = str(possible_pin[1]).lower()
            if((possible_pin[1].lower() in line.lower()) and (possible_pin[1] != "")): # Find the resistor in the netlist that is connected to the FPGA
                signal_name = extract_text_between_single_quotes(line).lower()
                if "gnd" not in possible_pin[0] and "vcc" not in possible_pin[0] and "+" not in possible_pin[0]: 
                    if signal_name not in pin_list:
                        signal_name = f"{str(signal_name):<25}"
                        for pattern, vhdl_decl in search_patterns.items():
                            if pattern in linelower:
                                pin_list.append(f'{signal_name} : {vhdl_decl}')
                                pins_with_res_inseries.append([signal_name, possible_pin[0], possible_pin[1]])
                                break

result = rearrange_and_group_strings(pin_list)
result = remove_duplicates(result)
if len(result) < 1:
    print("Error: No Matching Nets Found, VHDL file not created")
    print("Matching strings used to find pins are:")
    for strings in search_patterns:
        print(strings)
    exit()
else:

    print("")
    print(f"Pin search strings = {search_patterns.keys()}")
    print("*If you need to add more for a specific project, add them to the 'search_patterns' variable.")
    print("")
    print(f"-----> Nets connected to {chip_id} matching the search strings found = {len(result)}")
    print(f"Nets containing strings: 'gnd', 'vcc' or '+' are ignored")
    print("")
    result[-1] = result[-1][0:-1] # Remove last semicolon

if len(pins_with_res_inseries) > 0:
    print(f"Found nets connected to {chip_id} with series resistors")
    print("PL net name / net connected to FPGA name / resistor name")

    for nets in pins_with_res_inseries:
        print(f"    {nets}")

# Writing the VHDL file
entity_name = filename.split('.')[0]
vhdl_filename = f"{filename}_gen.vhd"

with open(vhdl_filename, 'w') as f: # Make out TLD.vhd
    f.write(f"entity {entity_name} is\n")
    f.write("  port (\n")
    f.write("    " + "\n    ".join(result) + "\n")
    f.write("  );\n")
    f.write("end entity;\n")



print(f"Generated {vhdl_filename}")
print()
