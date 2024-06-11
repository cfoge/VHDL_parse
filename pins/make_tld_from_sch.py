import re
import sys

## This script takes a Mentor Graphics netlist and createsa a VHDL TLD from it given the designator of the FPGA (eg u17), this can be used to create a TLD or as part of checking pins, contrants ect...

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

# if not ((len(sys.argv) == 4)): #check for correct number of arguments 
#     print('This script needs 2 inputs, new file name and the netlist file')
#     print('example: tld_name netlist.txt u12')
#     sys.exit(1)

filename = "test"#sys.argv[1]
netlist_filename = 'BMDPCB1118A_NETLIST.txt'# sys.argv[2] 
chip_id = sys.argv[3]  #this si the symbol in the scematic for the FPGA ic
prefix = "pl" # this is the prefix that sits in front of your pin names if that is how your scematic is layed out

#add method for saying what the prefix for pins should be

# filename = sys.argv[1]
# netlist_filename = sys.argv[2] 
# chip_id = sys.argv[3] 

try:
    with open(netlist_filename) as f:
        netlist = f.readlines()
except:
    print("Error opening netlist file!!! check File exists, matches the name/path given")

pin_list = []
possible_pin_list = []

for line in netlist:
    if(("net") in line.lower()) and (("flatnet") not in line.lower()): 
        chip_id = chip_id.lower()
        line_lc = line.lower()    
        if (chip_id in line_lc):
            signal_name = extract_text_between_single_quotes(line)
            signal_name = f"{str(signal_name):<25}"
            if "plo_" in line.lower():
                pin_list.append(f'{signal_name.lower()} : out   std_logic;')
            elif "pli_" in line.lower():    
                pin_list.append(f'{signal_name.lower()} : in    std_logic;')
            elif "plio_" in line.lower():    
                pin_list.append(f'{signal_name.lower()} : inout std_logic;')
            elif prefix.lower() in line.lower(): 
                pin_list.append(f'{signal_name.lower()} : <in/out/inout> std_logic;')
            elif 'pad' in line.lower(): ## look for padi pado naming convention
                if 'padi_' in line.lower():
                    pin_list.append(f'{signal_name.lower()} : in    std_logic;')
                elif 'pado_' in line.lower():
                    pin_list.append(f'{signal_name.lower()} : out   std_logic;')
                elif 'padio_' in line.lower():
                    pin_list.append(f'{signal_name.lower()} : inout std_logic;')
                else:
                    pin_list.append(f'{signal_name.lower()} : <in/out/inout> std_logic;')
    # to help find when a resistor is in the way of the pin
            else: # look for pins connected to the FPGA that dont have PL in the signal name
                signal_name = extract_text_between_single_quotes(line)
                connected_part_name = extract_text_between_space_dash_quotes(line)
                if 'r' in connected_part_name.lower(): # if there is a resistor connected to the FPGA add it as a possible pin
                    possible_pin_list.append([signal_name.lower(),connected_part_name.lower()])

if len(possible_pin_list) > 0: #now check all the pins on the FPGA that are connected to resistors and see if any of those reisitors are connected to a net with a prefix we are interested in
    for line in netlist:
        for possible_pin in possible_pin_list:
            test = line.lower()
            test2 =str(possible_pin[1]).lower()
            if((possible_pin[1].lower() in line.lower()) and (possible_pin[1] != "") ):# and (chip_id.lower() in line.lower())):
                if "plo_" in possible_pin[0]:
                    pin_list.append(f'{possible_pin[0].lower()} : out std_logic;')
                elif "pli_" in possible_pin[0]:    
                    pin_list.append(f'{possible_pin[0].lower()} : in std_logic;')
                elif "plio_" in possible_pin[0]:    
                    pin_list.append(f'{possible_pin[0].lower()} : inout std_logic;')

result = rearrange_and_group_strings(pin_list)
if len(result) < 1:
    print("Error: No Matching Nets Found, VHDL file not created")
    exit()
else:
    print(f"Nets Found = {len(result)}")
    result[-1] = result[-1] [0:-1] # remove last semi colon


# Writing the VHDL file
entity_name = filename.split('.')[0]
vhdl_filename = f"{filename}_gen.vhd"
# vhdl_filename = f"../src/{filename}_gen.vhd"

with open(vhdl_filename, 'w') as f:
    f.write(f"entity {entity_name} is\n")
    f.write("  port (\n")
    f.write("    " + "\n    ".join(result) + "\n")
    f.write("  );\n")
    f.write("end entity;\n")

print(f"Generated {vhdl_filename}")
