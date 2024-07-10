# A command line program for listing what is inside a vhdl file (note: this ignores generate statemenets and removes duplicates)
# Arg 1 is the vhdl file
# Robert D Jordan 2022

import sys
import re
from token_test import *
import os
import argparse


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


show_att = True
show_var = True
show_const = True
show_sig = True
show_pros = True
show_comp = True
show_func = True
show_gen = True
show_lib = True
show_types = True

# if not (
#     (len(sys.argv) == 2) | (len(sys.argv) == 3)
# ):  # check for correct number of arguments
#     print(
#         "This script needs one or two inputs, the first is a vhdl file, the second (optional) a paramiter"
#     )
#     print(
#         '2nd arg "f" show all, "a" show attributes, "v" show variables, "c" show constants, "p" show processes, "s" show signals'
#     )
#     print("example: get_info.py input.vhd a")
#     sys.exit(1)

# if len(sys.argv) == 3:  # if there is a 2ndrd argument
#     if "f" in sys.argv[2]:
#         show_att = True
#         show_var = True
#         show_const = True
#         show_sig = True
#         show_pros = True
#     if "a" in sys.argv[2]:
#         show_att = True
#     if "v" in sys.argv[2]:
#         show_var = True
#     if "c" in sys.argv[2]:
#         show_const = True
#     if "p" in sys.argv[2]:
#         show_pros = True
#     if "s" in sys.argv[2]:
#         show_sig = True


# target_vhdl = parse_vhdl(sys.argv[1])
file = "tests/test8.vhdl"
target_vhdl = parse_vhdl(file)
if(isinstance(target_vhdl, str)):
    print(target_vhdl)
    exit()

print(color.GREEN + "---------------------------------------------------" + color.END)
print("Getting Info For " + color.GREEN + target_vhdl.url + color.END)
print(
    f"Name: {color.GREEN}{target_vhdl.data}{color.END}  -  Arch: {color.GREEN}{target_vhdl.arch}"
)
print(color.DARKCYAN + "   Generics:")
for i in target_vhdl.generic:
    print("        -->" + str(i))
print(color.END + color.CYAN + "   Port:")
for i in target_vhdl.port:
    print("        -->" + str(i))

print(color.BLUE + "   Components:")
for i in target_vhdl.component:
    print("        -->" + str(i.data))
print(color.END + color.PURPLE + "   Generate:")
for i in target_vhdl.generate:
    print("        -->" + str(i))
print(color.END + color.GREEN + "   Entities:")
for i in target_vhdl.children:
    print("        -->" + str(i.data))
if show_pros == True:
    print(color.END + color.YELLOW + "   Process:")
    for i in target_vhdl.process:
        print("        --> " + str(i[0])+ ": " + str(i[1]))
if show_const == True:
    print(color.END + color.DARKCYAN + "   Constants:")
    for i in target_vhdl.constant:
        print("        -->" + str(i))
if show_att == True:
    print(color.END + color.CYAN + "   Attributes:")
    for i in target_vhdl.attribute:
        print("        -->" + str(i))
if show_sig == True:
    print(color.END + color.GREEN + "   Signals:")
    for i in target_vhdl.signal:
        print("        -->" + str(i))
print(color.END + "---------------------------------------------------" + color.END)
