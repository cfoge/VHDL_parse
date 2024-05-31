# A command line program for listing what is inside a vhdl file (note: this ignores generate statemenets and removes duplicates)
# Arg 1 is the vhdl file
# Robert D Jordan 2022

import sys
import re


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


show_att = False
show_var = False
show_const = False
show_sig = False
show_pros = False

if not (
    (len(sys.argv) == 2) | (len(sys.argv) == 3)
):  # check for correct number of arguments
    print(
        "This script needs one or two inputs, the first is a vhdl file, the second (optional) a paramiter"
    )
    print(
        '2nd arg "f" show all, "a" show attributes, "v" show variables, "c" show constants, "p" show processes, "s" show signals'
    )
    print("example: what_in.py input.vhd a")
    sys.exit(1)

if len(sys.argv) == 3:  # if there is a 2ndrd argument
    if "f" in sys.argv[2]:
        show_att = True
        show_var = True
        show_const = True
        show_sig = True
        show_pros = True
    if "a" in sys.argv[2]:
        show_att = True
    if "v" in sys.argv[2]:
        show_var = True
    if "c" in sys.argv[2]:
        show_const = True
    if "p" in sys.argv[2]:
        show_pros = True
    if "s" in sys.argv[2]:
        show_sig = True


with open(sys.argv[1]) as f:
    file_in = f.readlines()

with open(sys.argv[1]) as f:
    vhd = f.readlines()


class vhdl_obj(object):
    def __init__(self, type, data, ln):
        self.type = type
        self.data = data
        self.line_num = ln
        self.children = []
        self.generic = []
        self.port = []

    def add_child(self, obj):
        self.children.append(obj)

    def add_generic(self, obj):
        self.generic.append(obj)

    def add_port(self, obj):
        self.port.append(obj)


entity_vhdl = []
instance_vhdl = []
component_vhdl = []
process_vhdl = []
constant_vhdl = []
variable_vhdl = []
attribute_vhdl = []
signal_vhdl = []

for i in vhd:
    if ("entity" in i) & ("is" in i):
        tmp1 = re.findall("entity (.*) is", i)
        entity_vhdl.append(vhdl_obj("entity", tmp1[0].strip(), vhd.index(i)))
    if ("entity" in i) & (":" in i):
        tmp1 = i.strip()
        instance_vhdl.append(vhdl_obj("instance", tmp1, vhd.index(i)))
    if ("component" in i) & ("is" in i):
        tmp1 = re.findall("component (.*) is", i)
        component_vhdl.append(vhdl_obj("component", tmp1, vhd.index(i)))
    if ("process" in i) & ("(" in i) & (")" in i):
        tmp1 = i.strip()
        process_vhdl.append(vhdl_obj("process", tmp1, vhd.index(i)))
    if ("constant" in i) & (":=" in i) & (";" in i):
        tmp1 = i.strip()
        constant_vhdl.append(tmp1)
    if ("Variable" in i) & (":" in i) & (";" in i):
        tmp1 = i.strip()
        variable_vhdl.append(tmp1)
    if ("attribute" in i) & (":" in i) & (";" in i):
        tmp1 = i.strip()
        attribute_vhdl.append(tmp1)
    if (("signal" in i) & (":" in i) & (";" in i)) & ("attribute" not in i):
        tmp1 = i.strip()
        signal_vhdl.append(tmp1)


# # create dependency graph from results
# tr = Tree()
# n1 = tr.root
# n2 = TreeNode(entity_final[0])
# nodes = []
# for i in range(len(instance_final_nodup)):
#     nodes.append(TreeNode(instance_final_nodup[i]))
# for i in nodes:
#     n2.add_child(i)
# for i in nodes:
#     n2.add_depth(n2)


print(color.GREEN + "---------------------------------------------------" + color.END)
print(
    "Running list entity, components, ect... in "
    + color.YELLOW
    + sys.argv[1]
    + color.END
)
print(color.BOLD + entity_vhdl[0].data + color.END)
print(color.BLUE + "   components:")
for i in range(len(component_vhdl)):
    print("        --" + str(component_vhdl[i].data))
print(color.END + color.GREEN + "   entities:")
for i in range(len(instance_vhdl)):
    print("        --" + instance_vhdl[i].data)
if show_pros == True:
    print(color.END + color.YELLOW + "   process:")
    for i in range(len(process_vhdl)):
        print("        --" + process_vhdl[i].data)
if show_const == True:
    print(color.END + color.DARKCYAN + "   constants:")
    for i in range(len(constant_vhdl)):
        print("        --" + constant_vhdl[i])
if show_var == True:
    print(color.END + color.PURPLE + "   variables:")
    for i in range(len(variable_vhdl)):
        print("        --" + variable_vhdl[i])
if show_att == True:
    print(color.END + color.CYAN + "   attributes:")
    for i in range(len(attribute_vhdl)):
        print("        --" + attribute_vhdl[i])
if show_sig == True:
    print(color.END + color.RED + "   signals:")
    for i in range(len(signal_vhdl)):
        print("        --" + signal_vhdl[i])
print(
    color.END
    + color.GREEN
    + "---------------------------------------------------"
    + color.END
)
