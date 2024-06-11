# This script is designed to go through the process of creating and checking the connections of a Xilinx FPGA project from scematic through to top level design.

# importing os module
import os
 
def copy_and_rename_os(src_path, new_name):
    # Copy the file
    os.copyfile(src_path, f"{new_name}")

# setup the project settings
filename = "test"#sys.argv[1]
netlist_filename = 'BMDPCB1118A_NETLIST.txt' #sys.argv[2] 
chip_id = 'U17' #sys.argv[3]  #this si the symbol in the scematic for the FPGA ic ----!!!! NOTE: make sure that this has a captial leter designator (eg: U17)
# prefix = "pl" # this is the prefix that sits in front of your pin names if that is how your scematic is layed out


# read the scematic file and make a VHDL file with ports matching the PLI,PLO,PLIO,PADI,PADO,PADIO net name
os.system(f"python make_tld_from_sch.py {filename} {netlist_filename} {chip_id}")

# make a constraints file from this top level VHDL file with XXX for all of the pin locations (for now)
os.system(f"python make_xdc.py {filename} {filename}_gen.vhd ")

# get the pin names and locations from the scematic file and apply them to the contraints file
os.system(f"python get_sch_loc.py {filename}.xdc {netlist_filename} {chip_id}")

# check, to be sure the pin matches between NETLIST AND CONTRSINTS file
os.system(f"python check_sch.py matched_pins_with_sch.xdc {netlist_filename}")
# check, to be sure the pin/ports matche between VHDL AND CONTRSINTS file
os.system(f"python check_xdc.py {filename}.xdc {filename}_gen.vhd")

# Copy generated files and rename 
copy_and_rename_os("matched_pins_with_sch.xdc", f"{filename}_gen.xdc")