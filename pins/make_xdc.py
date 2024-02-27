# A command line program for creating an XDC file from the VHDL top level design
# Arg 1 is the XDC file name to write to, Arg 2 is the Vhdl Top level file
# Robert D Jordan 2022

import sys
import re

quartus = False

if not (
    (len(sys.argv) == 3) | (len(sys.argv) == 4)
):  # check for correct number of arguments
    print(
        "This script needs two inputs, .XDC output file name and the input Top level .vhd file."
    )
    print(
        'example: check_xdc.py output input.vhd (opt 3rd argument "q" generates Quartus output'
    )
    sys.exit(1)

if len(sys.argv) == 4:  # if there is a 3rd argument
    if "q" in sys.argv[3]:
        print("Running with settings (Quartus .tlc)")
        quartus = True
else:
    print("Running with default settings (Xilinx .xdc)")


with open(sys.argv[2]) as f:  # import xdc file as string
    vhd = f.readlines()

portStart = []
portEnd = []
portName = []
portNameFinal = []
commentedOut = []

# iterate through list of elements to find "port (" , the start of the port declaration and "end entity"
for i in vhd:
    if "port (" in i:
        # Find possible index for the start of port declaration
        portStart.append(vhd.index(i))

    if "end entity" in i:
        # Find possible index for the end of port declaration
        portEnd.append(vhd.index(i))

del vhd[
    portEnd[0] : len(vhd)
]  # remove from after port declaration, do this first to preserve indexing
del vhd[0 : portStart[0]]  # remove from before port declaration


# iterate through list of elements and if ":" extract up until ":", which should be the port name
for i in vhd:
    if ":" in i:
        line = vhd.index(i)
        match = re.search(":", vhd[line])
        if ("downto") in i:
            portWidth = re.findall(r"\d+", i[match.end() :])
            portWidthSize = (int(portWidth[0]) + 1) - int(
                portWidth[1]
            )  # doesn't handle inverted declarations (eg 0 down to 7)
            portnameCleaned = re.sub(
                r"[- ]", "", i[0 : match.start()]
            )  # remove empty spaces and --
            portName.append(
                [portnameCleaned, portWidthSize, portWidth[0], portWidth[1]]
            )
        else:
            portnameCleaned = re.sub(
                r"[- ]", "", i[0 : match.start()]
            )  # remove empty spaces and --
            portName.append([portnameCleaned, 1])
        if "--" in i:  # If line was commented out create a list of them
            commentedOut.append(portnameCleaned)  # add commented out ports to a list

# generate the .xdc or .tcl file with pins from the portName list and its widths
if quartus == False:
    outputFileName = sys.argv[1] 
else:
    outputFileName = sys.argv[1] + ".tcl"

f = open(outputFileName, "w")  # create file

if quartus == True:
    for i in portName:
        if (
            i[1] > 1
        ):  # if the port width is greater then 1 break each bit out to a separate pin
            for j in range(i[1]):
                f.writelines(
                    "set_location_assignment XXX  -to "
                    + i[0]
                    + "["
                    + str(j + int(i[3]))
                    + "]\n"
                )
        else:
            f.writelines("set_location_assignment XXX  -to " + i[0] + "\n")
else:
    for i in portName:
        if (
            i[1] > 1
        ):  # if the port width is greater then 1 break each bit out to a separate pin
            for j in range(i[1]):
                f.writelines(
                    "set_property PACKAGE_PIN XXX [get_ports {"
                    + i[0]
                    + "["
                    + str(j + int(i[3]))
                    + "]"
                    "}]\n"
                )
        else:
            f.writelines("set_property PACKAGE_PIN XXX [get_ports {" + i[0] + "}]\n")


print(outputFileName + " created from " + sys.argv[2])
print("**************************************************")
print("Commented out Ports not added to the output file:")
print(*commentedOut, sep="\n")
print("**************************************************")
