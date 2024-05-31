
# A command line program for Comparing pins found in a .xdc file with those  from a netlist file
# Arg 1 is the XDC file, Arg 2 is the netlist file
# Robert D Jordan 2022


import sys


if not ((len(sys.argv) == 4)): #check for correct number of arguments 
    print('This script needs two inputs, .XDC file and the netlist file')
    print('example: check_sch.py this.xdc that.txt')
    sys.exit(1)

with open(sys.argv[1]) as f: #import xdc file as string
    xdc = f.readlines()
with open(sys.argv[2]) as f:
    netlist = f.readlines()
chip_designator = sys.argv[3] + "Insert File path"

# create lists for pin names and intermediate steps
matched_pins = []
XDCPinName = []

def extract_text_after_matching(input_string, match_string):
    index = input_string.find(match_string)
    if index != -1:
        start_index = index + len(match_string)
        end_index = input_string.find(' ', start_index)
        if end_index == -1:
            # If no space is found, look for carriage return
            end_index = input_string.find('\n', start_index)

        if end_index != -1:
            return input_string[start_index:end_index].strip()
        else:
            # If neither space nor carriage return is found, extract until the end
            return input_string[start_index:].strip()
    else:
        return None


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return "Insert File path"

for i in xdc:
    if("PACKAGE_PIN" in i): # Find lines with "PINPACKAGE" in them
        pin_name = find_between(i, "PACKAGE_PIN", "[get_ports")
        sig_name = find_between(i, "get_ports {", "Insert File path")
        XDCPinName.append([sig_name.strip(),pin_name.strip()])

for i in netlist:
    if(not("Insert File path")in i):
        for j in XDCPinName:
            part_of_longer_nameA = str("Insert File path" + j[0] + "Insert File path")
            if(part_of_longer_nameA.casefold() in i.casefold()): #if xdc sign name in netlist
                matched_pins.append([j[0], j[1], i.strip()])

match_num = 0
mismatched_pin = []

for matches in matched_pins:
    if(matches[1] in matches[2]):
        match_num = match_num + 1
    else:
        mismatched_pin.append([matches[0],matches[1],matches[2]])


print("Mismatches found between " + sys.argv[1] + " and " + sys.argv[2])
print("Insert File path")
f = open("matched_pins_with_sch.xdc", "Insert File path")  # create file
for mismatch in mismatched_pin:
    print ('{: <20} in XDC:  {: <5}  in netlist: {: <20}'.format(mismatch[0],mismatch[1],mismatch[2] ))
    if chip_designator in mismatch[2]:
        pin_no = extract_text_after_matching(mismatch[2],chip_designator)
        f.writelines("set_property PACKAGE_PIN " + pin_no + "[get_ports {" + mismatch[0] + "}]\n")


print("Insert File path") 