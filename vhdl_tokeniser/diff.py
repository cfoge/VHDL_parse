# A command line program for diffing what is inside a vhdl file based on VHDL keywords (note: this ignores generate statemenets and removes duplicates)
# Arg 1 is a vhdl file, Arg 2 is a vhdl file
# Robert D Jordan 2022

import sys
from token_test import *
import os
import argparse

class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# if not ((len(sys.argv) == 3)): #check for correct number of arguments
#     print('This script needs two inputs, both shuld be VHDL files')
#     print('example: diff_vhdl.py inputA.vhd inputB.vhd ')
#     sys.exit(1)


def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def make_lists_equal_length(list1, list2):
    len1, len2 = len(list1), len(list2)

    if len1 < len2:
        list1 += [""] * (len2 - len1)
    elif len2 < len1:
        list2 += [""] * (len1 - len2)

    return list1, list2


def print_lists_aligned(list1, list2):
    try:
        max_length = max(len(str(item)) for item in list1)
    except:
        return 0

    for item1, item2 in zip(list1, list2):
        if len(item1)==0:
            item1 = "[none]"
        if len(item2)==0:
            item2 = "[none]"
        spacing = max_length - len(str(item1)) + 12
        print(f"     {item1}{'-' * spacing}{item2}")


def print_mismatch(name, list1, list2, col = {color.END}):
    if len(list1) != len(list2):
        result_a, result_b = make_lists_equal_length(list1, list2)
        print(f"{col}{name}{color.END}")
        print_lists_aligned(result_a, result_b)
    else:
        print(f"{col}{name}{color.END}")
        print_lists_aligned(list1, list2)

def get_longer(list1,list2):
    if len(list1)>=len(list2):
        return len(list1)
    else:
        return len(list2)

def calculate_dif(self, other):  # != operator returns the differences as a string
    diff_obj = vhdl_obj()
    if self.data == other.data:
        diff_obj.data = []
    else:
        diff_obj.data = [self.data, other.data]
        print(f"Name:")
        print(f"     {color.BOLD}{self.data:<25}             {other.data:<25}{color.END} ")

    if len(diff(self.generic, other.generic)) != 0:
        diff_obj.generic.append([self.generic, other.generic])
        print_mismatch("Generic:", self.generic, other.generic)
    if len(diff(self.port, other.port)) != 0:
        diff_obj.port.append([self.port, other.port])
        print_mismatch("Port:", self.port, other.port, color.RED)
    if len(diff(self.children, other.children)) != 0:
        diff_obj.children.append([self.children, other.children])
        print_mismatch("Childeren:", self.children, other.children)
    if len(diff(self.component, other.component)) != 0:
        diff_obj.component.append([self.component, other.component])
        print_mismatch("Component:", self.component, other.component,color.BLUE)
    if len(diff(self.attribute, other.attribute)) != 0:
        diff_obj.attribute.append([self.attribute, other.attribute])
        print_mismatch("Attribute:", self.attribute, other.attribute)
    if len(diff(self.constant, other.port)) != 0:
        diff_obj.constant.append([self.constant, other.constant])
        print_mismatch("Constant:", self.constant, other.constant)
    if len(diff(self.process, other.process)) != 0:
        diff_obj.process.append([self.process, other.process])
        print_mismatch("Process:", self.process, other.process,color.YELLOW)
    if len(diff(self.signal, other.signal)) != 0:
        diff_obj.signal.append([self.signal, other.signal])
        print_mismatch("Signal:", self.signal, other.signal, color.GREEN)
    return diff_obj


file1 = parse_vhdl("vhdl_tokeniser/tests/test1.vhdl")  # parse_vhdl(sys.argv[1])
file2 = parse_vhdl("vhdl_tokeniser/tests/test2.vhdl")  # parse_vhdl(sys.argv[2])


print("---------------------------------------------------")
# print("Getting Diff For " + color.GREEN + sys.argv[1] + color.END + " and " + + color.GREEN + sys.argv[2] + color.END) 
print()
diff_obj = calculate_dif(file1, file2)

print("---------------------------------------------------")
