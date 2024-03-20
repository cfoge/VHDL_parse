from token_test import *
import os
import argparse

# ANSI escape codes for colors
COLORS = [
    '\033[97m',  # WHITE
    '\033[92m',  # GREEN
    '\033[94m',  # BLUE
    '\033[93m',  # YELLOW
    '\033[96m',  # CYAN
    '\033[95m',  # MAGENTA
    '\033[0m',   # RESET
]

def create_tree(parents, children):
    tree = {}
    for parent, child in zip(parents, children):
        if parent not in tree:
            tree[parent] = []
        if child not in tree:
            tree[child] = []           
        tree[parent].append(child)
    return tree


#dependency search
def cl_depend(root_dir,tld, print_url):
    # root_dir = 'C:/Users/robertjo/Documents/other/28_7_23_ems/src'
    # tld = 'C:/Users/robertjo/Documents/other/28_7_23_ems/src/digital_side/test_1_build/test_digital_side.vhd'
    vhdl_files = []
    #print("VHDL Files Found:")
    for root, dirs, files in os.walk(root_dir):
        for file in files: 
            if file.endswith(".vhd") or file.endswith(".vhdl"):
                #print(os.path.join(root, file))
                vhdl_files.append(os.path.join(root, file))

    vhdl_file_as_obj = []

    # make list of VHDL files as parsed objects --this reads every file maybe there is a better way to recursivly only read the needed files
    for files in vhdl_files:
        vhdl_file_as_obj.append(parse_vhdl(files))

    target_vhdl = parse_vhdl(tld)

    # search list and and attach dependent objects as childeren
    for vhdl_o in vhdl_file_as_obj:
        for child in vhdl_o.children_name:
            for vhdl_objsB in vhdl_file_as_obj:
                if len(vhdl_objsB.data)>0:

                    if vhdl_objsB.data == child.mod:
                        child.vhdl_obj = (vhdl_objsB)
                        #vhdl_o.children_name.remove(child)
                        break

    def print_child(object,depth,parent, print_url):
        url = ''
        if depth == 0:
            spacing =  ""
            object.modname = object.data
            if (print_url == True):
                url = object.url
            print (object.data + " " + url)
        if depth > 1:
            spacing =  "    " * (depth - 1) + "   " #             spacing =  "    " * (depth - 1) + "│   "
        else: 
            spacing = "    "
        if isinstance(object,vhdl_obj): 
            obj_type = "obj"
            child_var = object.children_name
            if (len(child_var) > 0):
                spacing = "    " * (depth)
                if obj_type == "obj":
                    # print (spacing + "├─ " + object.data[0])

                    for child in range(len(child_var)):
                        # hierachy_vis.append([object.modname,child_var[child].name,depth,child_var[child].mod])
                        print_child(object.children_name[child], (depth + 1),object.data[0], print_url)

        elif isinstance(object,instanc): 
            if (print_url == True) and (object.vhdl_obj != None):
                url = object.vhdl_obj.url
            obj_type = "inst"
            temp1 = object.vhdl_obj
            if temp1 != None:
                object.vhdl_obj.modname = object.name
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "":
                    print(color + spacing +"├─ " + object.name + " " + COLORS[6] + url)
                else:
                    print(color + spacing +"├─ " + object.mod + " : " + object.name + " " + COLORS[6] + url)
                hierachy_vis.append([parent,object.name,depth,object.mod])
                print_child(object.vhdl_obj, (depth + 1), object.name, print_url)
            else:
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "":
                    print(color + spacing +"├─ " + object.name + " " + COLORS[6] + url)
                else:
                    print(color + spacing +"├─ " + object.mod + " : " + object.name + " " + COLORS[6] + url)
        return 

    print("---------------------------------------------------")
    print(f"Hierarchy of {target_vhdl.data} is: \n")
    hierachy_vis = []
    for vhdl_objs in vhdl_file_as_obj:
        if len(vhdl_objs.data) > 0 :
            if (target_vhdl.data == vhdl_objs.data ):
 
                print_child(vhdl_objs,0,"",print_url)
    print("\033[0m---------------------------------------------------")

    return

if __name__ == "__main__":
    # Add argparse for command-line arguments
    parser = argparse.ArgumentParser(description='VHDL wrapper generator')
    parser.add_argument('tld', type=str, help='Input VHDL file (Your top level design)')
    parser.add_argument('-d', '--directory', type=str, help='root directory for vhdl project')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    


    # # Check if the correct number of arguments is provided
    args = parser.parse_args()


tld = args.tld
ROOT_DIR = os.path.dirname(tld)
root_dir = args.directory if args.directory is not None else ROOT_DIR

cl_depend(root_dir,tld, args.verbose)


print("")