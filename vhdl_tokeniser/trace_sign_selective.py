# A command line program for tracing signals through hieracys of of vhdl docs
# Robert D Jordan 2022

import os
from token_test import *
import graphviz
import sys

COLORS = [
    "\033[97m",  # WHITE
    "\033[92m",  # GREEN
    "\033[94m",  # BLUE
    "\033[93m",  # YELLOW
    "\033[96m",  # CYAN
    "\033[95m",  # MAGENTA          ---Important notes
    "\031[95m",  # RED              ---ERRORS
    "\033[0m",  # RESET
]
########################### search node
class TreeNode(object):
    def __init__(self, fname, search, hdl_type, if_mod_name, assigned_to, subset = "", infileassign= ""):
        self.filename = fname
        self.search_term = search
        self.type = hdl_type
        self.if_mod_name = if_mod_name
        self.assigned_to = assigned_to
        self.assign_subset = subset
        self.infileassign = infileassign # for handaling the printout where a signal has had its name changed in a file before being passed to a sub module
        self.parent = []
        self.children = []
        self.full_assignment_string = ""  # used only if there is (x downto Y) in the LHS of the asignment, this needs to be kept seperate and retreved later

    def paths(self):
        return_data = get_data_slim(self)
        if not self.children:
            return [[return_data]]  # one path: only contains self.value
        paths = []
        for child in self.children:

            for path in child.paths():

                paths.append([return_data] + path)
        return paths

    def add_child(self, obj):
        self.children.append(obj)

    def add_perent(self, obj):
        self.parent.append(obj)


class Tree:
    def __init__(self):
        self.root = TreeNode("ROOT", "NONE", "")

    def preorder_trav(self, node):
        if node is not None:
            print(node.data)
            print("   ", end="")
            if len(node.children) != 0:
                for n in node.children:
                    for x in range(node.depth):
                        print("   ", end="")
                    print("|--", end="")
                    self.preorder_trav(n)


######################################################################

# def get_data(node):
#     path_list = ""
#     if (node.type == "file"):
#         path_list = str("file: " + node.filename)
#     if (node.type == "port"):
#         path_list = str(node.type + ": " + node.search_term)
#     if (node.type == "signal"):
#         path_list = str(node.type + ": " + node.search_term)
#     if (node.type == "component port"):
#         path_list = str(node.type + ": " + node.search_term)
#     if (node.type == "module"):
#         path_list = str(node.type + ": "+ node.if_mod_name + ": "+ node.assigned_to +" <= "+ node.search_term)
#     return path_list


def get_data_slim(node):
    path_list = ""
    if node.type == "file":
        path_list = node.filename
    elif node.type == "port":
        path_list = node.search_term
    elif node.type == "signal":
        path_list = node.search_term
    elif node.type == "component port":
        path_list = node.search_term
    elif node.type == "module":
        # path_list = [f"{node.if_mod_name}:{node.filename}" , node.assigned_to]
        path_list = [node, node.assigned_to]
    return path_list


def attach_dependent_objects(
    parent_vhdl_obj, entity_texts_with_path
):  # this function creates a vhdl object hieracy of only instanciated vhdl entitys
    try:
        for child in parent_vhdl_obj.children_name:
            for vhdl_found_entities in entity_texts_with_path:
                if len(vhdl_found_entities[0]) > 0:
                    if vhdl_found_entities[0] == child.mod:
                        new_child = parse_vhdl(vhdl_found_entities[1])
                        child.vhdl_obj = new_child
                        attach_dependent_objects(
                            new_child, entity_texts_with_path
                        )  # Recursive call
                        break

    except Exception as e:
        error_log.append(["file_path_error", e])

def search_assignement(vhdl_obj_in, find_str, curent_node, in_file_assignments):
    for (
        x
    ) in (
        vhdl_obj_in.assign
    ):  # find asignments in assignment not in functions, processes ect..
        if (find_str in x[0]) or (find_str in x[1]):
            if (
                x[1] == find_str 
            ):  # if a direct assignment with no logic add the signal our search string is beign assigned to as a node

                assignments.append(
                    [vhdl_obj_in.data, x[0], x[1]]
                )  # filen name, assigned to,
                full_assign_list.append(
                    f"Combinational Assignment in {vhdl_obj_in.data}: {x[0]} <= {x[1]} "
                    
                )
                in_file_assignments.append(x[0])
                temp = [find_str]
                find_str = temp
                find_str.append(x[0])
                break
            elif find_str in x[1]:
                if "." in x[1]: # lets see if the assignment into a sub module is done using a record txpe (eg: signal.subsignal)
                        search_length = len(find_str)
                        if (x[1][:search_length] == find_str) and (x[1][search_length+1] == "."):
                            full_assign_list.append(f"Combinational Assignment in {vhdl_obj_in.data}: {x[0]} <= {x[1]} ") ########################## need to add a method for introducing this as a new search term!!!
                            in_file_assignments.append(x[0])
                elif "(" in x[1] and ")" in x[1]: # lets see if a subset of the signal is beign assigned (eg: signal(4 downto 0))
                        search_length = len(find_str)
                        if (x[1][:search_length] == find_str) and (x[1][search_length] == "("):
                            full_assign_list.append(f"Combinational Assignment in {vhdl_obj_in.data}: {x[0]} <= {x[1]} ")
                            in_file_assignments.append(x[0])
                # this detects if the source of the assignment had the keyword in it, need to be more specific
                # possible_assignments.append(['?Combinational Assignment',vhdl_obj_in.data, x[0],x[1] ]) # filen name, assigned to
                break
    for y in vhdl_obj_in.process:  # find asignments in processes
        for x in y[2]:
            if type(find_str) != list:
                if find_str in x[0] or find_str in x[1]:
                    if (
                        x[1] == find_str
                    ):  # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                        temp = [find_str]
                        find_str = temp
                        find_str.append(x[0])
                        full_assign_list.append(
                            f"Process Assignment in {vhdl_obj_in.data}/{y[0]}({y[1]}): {x[0]} <= {x[1]} "
                        )
                        break
                    else:
                        # this acidently finds the keyword in the rocess trigger
                        # possible_assignments.append([f'?Process: {y[0]}({y[1]})',vhdl_obj_in.data, x[0],x[1] ]) # filen name, assigned to
                        break
            else:
                for string in find_str:
                    if (
                        x[1] == find_str
                    ):  # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                        temp = [find_str]
                        find_str = temp
                        find_str.append(x[0])
                        full_assign_list.append(
                            f"Process Assignment in {vhdl_obj_in.data}/{y[0]}({y[1]}): {x[0]} <= {x[1]} "
                        )

                        break
                    else:
                        # this acidently finds the keyword in the rocess trigger
                        # possible_assignments.append([f'?Process: {y[0]}({y[1]})',vhdl_obj_in.data, x[0],x[1] ]) # filen name, assigned to
                        break

    # search generate statements for direct assignments
    for y in vhdl_obj_in.generate:  # find asignments in generate statements
        for x in y[2]:
            if type(find_str) != list:
                if find_str in x[0] or find_str in x[1]:
                    if (
                        x[1] == find_str
                    ):  # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                        temp = [find_str]
                        find_str = temp
                        find_str.append(x[0])
                        full_assign_list.append(
                            f"Generate Assignment in {vhdl_obj_in.data}/{y[0]}: {x[0]} <= {x[1]} "
                        )

                        break
                    else:
                        possible_assignments.append(
                            [vhdl_obj_in.data, x[0], x[1]]
                        )  # filen name, assigned to
                        break
            else:
                for string in find_str:
                    if (
                        x[1] == find_str
                    ):  # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                        temp = [find_str]
                        find_str = temp
                        find_str.append(x[0])
                        full_assign_list.append(
                            f"Generate Assignment in {vhdl_obj_in.data}/{y[0]}: {x[0]} <= {x[1]} "
                        )

                        break
                    else:
                        possible_assignments.append(
                            [vhdl_obj_in.data, x[0], x[1]]
                        )  # filen name, assigned to
                        break    
    return in_file_assignments


# root_dir = 'C:/Users/robertjo/Downloads/ems_directory fixup/fpga'
root_dir = "C:/BMD_builds/crc_error_fix"
# target_vhdl_in = 'C:/Users/robertjo/Downloads/ems_directory fixup/fpga/src/digital_side/test_1_build/test_digital_side.vhd'
target_vhdl_in = (
    "C:/BMD_builds/crc_error_fix/fpga/src/audio_monitor_12g_g3.vhd"
)
# search for arg 2 in each each part of the top level file
# search for other lines involving this signal
# search each child for
# find_str = "clk_300mhz"

# find_str = 'plo_lcd_sda'
find_str = 'iab_lcd_pen'
# find_str = 'genlock_sof'
verbose = True

vhdl_files = []
# print("VHDL Files Found:")
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".vhd") or file.endswith(".vhdl"):
            # print(os.path.join(root, file))
            vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []
print(f"{len(vhdl_files)} vhdl files found")
# check for duplicate file names!!!! print waring!!!! this may cause issues

###### FIND AND REMOVE DUPLICTES
# Dictionary to store encountered filenames and their corresponding paths
filename_to_path = {}

# List to store duplicate filenames
duplicate_filenames = []

# Iterate over entity_texts_with_path
for file_path in vhdl_files:
    # Extract the filename from the file path
    filename = os.path.basename(file_path)
    # Check if the filename is already in the dictionary
    if filename in filename_to_path:
        # If it is, add it to the list of duplicate filenames
        duplicate_filenames.append(filename)
    else:
        # Otherwise, add it to the dictionary with its path
        filename_to_path[filename] = file_path

# Remove duplicates from entity_texts_with_path
entity_texts_with_path_unique = []
for file_path in vhdl_files:
    filename = os.path.basename(file_path)
    if filename in duplicate_filenames:
        # Skip duplicates
        continue
    # Add non-duplicates to the unique list
    entity_texts_with_path_unique.append(file_path)

    # Update entity_texts_with_path to contain only unique filenames
vhdl_files = entity_texts_with_path_unique

# Print the number of duplicate files found
print(f"{len(duplicate_filenames)} duplicate files found")
if (len(duplicate_filenames)) > 0:
    print(
        f"{COLORS[5]}Duplicate files with the same name can create issues when searching through VHDL hierachys, so duplicates have been removed{COLORS[7]}\n"
    )


# Read each VHDL file, extract text between 'entity' and 'is', and store it with file path
entity_texts_with_path = []
unreadible_files = 0
for file_path in vhdl_files:
    try:
        with open(file_path, "r") as f:
            file_text = f.read()
            # Extract text between 'entity' and 'is'
            start_index = file_text.find("entity") + len("entity")
            end_index = file_text.find("is", start_index)
            if start_index != -1 and end_index != -1:
                entity_text = file_text[start_index:end_index].strip()
                # Exclude if the text contains "\n" unless it's at the very end
                if "\n" not in entity_text[:-1]:
                    entity_texts_with_path.append([entity_text, file_path])
    except:
        unreadible_files = unreadible_files + 1

if unreadible_files != 0:
    print(f"{COLORS[6]}{unreadible_files} vhdl files unreadable{COLORS[7]}")


target_vhdl = parse_vhdl(target_vhdl_in)
if isinstance(target_vhdl, str) == True:
    print(target_vhdl)
    sys.exit()

# see if the search term is a port or a signal in the TLD
search_is_port = False
search_is_signal = False
similer_search = []
for port in target_vhdl.port:  
    if find_str == port[0]:
        print(f"{COLORS[4]}{find_str}{COLORS[7]} is a port in {target_vhdl.data} --> {COLORS[4]}{port[0]}{COLORS[7]}  : {port[2]} length {port[3]}")
        search_is_port = True
    if find_str in port[0]:
        similer_search.append(port[0])
for sig in target_vhdl.signal:  
    if find_str == sig[0]:
        print(f"{COLORS[4]}{find_str}{COLORS[7]} is a signal in {target_vhdl.data} --> {COLORS[4]}{sig[0]}{COLORS[7]}  : {sig[2]} length {sig[3]}")
        search_is_signal = True
    if find_str in sig[0]:
        similer_search.append(sig[0])

if search_is_port == False and search_is_signal == False:      
    print(f"{COLORS[4]}{find_str}{COLORS[7]} was not found in {target_vhdl.data}!!!")
    if len(similer_search)>0:
        print(f"Similarly named ports and signals include: {COLORS[1]}{similer_search}{COLORS[7]}")
    sys.exit()


attach_dependent_objects(target_vhdl, entity_texts_with_path)


nodes = []
search_list_modules = []
assignments = []
assign_log = []
possible_assignments = []
full_assign_list = []
search_term_assigned_to_port = [] # a list to handle the case where signals being searched for are assigned to ports in the TLD


nodes.append(TreeNode(target_vhdl.data, find_str, "file", "", ""))

###################################


def create_path(vhdl_obj_in, find_str, curent_node):
    find_str_sub = ""
    in_file_assignments = [] # assignments that happen inside the file either in prcesses or combinational ect get put here and later added to the search terms
    # this part looks for ways that the signals name may have changed via being assigned to another signal
    in_file_assignments = search_assignement(vhdl_obj_in, find_str, curent_node, in_file_assignments)

    # # if in file assignements were detected add them to the search terms
    if len(in_file_assignments)>0:
        find_string_latch = find_str
        # if 
        # find_str = [find_str] + in_file_assignments


        if vhdl_obj_in.data == target_vhdl.data: # if we are on the TLD and there have been in file assignements check to see if any of those were to a port
            for assigns in in_file_assignments:
                for port in target_vhdl.port:  
                    if assigns == port[0]:
                        search_term_assigned_to_port.append([[assigns,port[1]], find_string_latch])


    if type(find_str) == list:
        for string in find_str:
            # string = find_str
            for (
                x
            ) in (
                vhdl_obj_in.children_name
            ):  # search for assignments in sub modules that have our search term going into them
                for y in x.port:
                    record_type_found = False
                    assing_subset = ""
                    if "." in y[1]: # lets see if the assignment into a sub module is done using a record type (eg: signal.subsignal)
                        search_length = len(string)
                        if (y[1][:search_length] == string) and (y[1][search_length+1] == "."):
                            record_type_found = True
                            assing_subset = y[1].split('.')[1].strip()
                            assing_subset = f".{assing_subset}"
                    elif "(" in y[1] and ")" in y[1]: # lets see if a subset of the signal is beign assigned (eg: signal(4 downto 0))
                        search_length = len(string)
                        if (y[1][:search_length] == string) and (y[1][search_length+1] == "("):
                            record_type_found = True
                            assing_subset = y[1].split('.')[1].strip()
                            assing_subset = f"{assing_subset}"

                    if y[1] == string or (record_type_found == True):
                        find_str_sub = y[0]
                        #########################################
                        
                        if y[1] in in_file_assignments: # only attach an infile assignment to a node if that re assigned signal was actualy used in the assignment in question
                            for in_file_ass in in_file_assignments:
                                if y[1]  == in_file_ass:
                                    infile_ass_checked = in_file_ass
                                    break
                        else:
                            infile_ass_checked = ""
                        new_node = TreeNode(x.mod, y[0], "module", x.name, find_str_sub, assing_subset, infile_ass_checked)
                        ###################################
                        new_node.full_assignment_string = y[
                            0
                        ]  # assign the full LHS to s specila veriable
                        curent_node.add_child(new_node)
                        if x.vhdl_obj != None:
                            create_path(x.vhdl_obj, find_str_sub, new_node)
    else:
        string = find_str
        for (
            x
        ) in (
            vhdl_obj_in.children_name
        ):  # search for assignments in sub modules that have our search term going into them
            for y in x.port:
                if string in y[1]:
                    record_type_found = False
                    assing_subset = ""
                    if "." in y[1]: # lets see if the assignment into a sub module is done using a record type (eg: signal.subsignal)
                        search_length = len(string)
                        if (y[1][:search_length] == string) and (y[1][search_length+1] == "."):
                            record_type_found = True
                            assing_subset = y[1].split('.')[1].strip()
                            assing_subset = f".{assing_subset}"
                    elif "(" in y[1] and ")" in y[1]: # lets see if a subset of the signal is beign assigned (eg: signal(4 downto 0))
                        search_length = len(string)
                        if (y[1][:search_length] == string) and (y[1][search_length+1] == "("):
                            record_type_found = True
                            assing_subset = y[1][search_length:].strip()

                    if y[1] == string or (record_type_found == True):
                        find_str_sub = y[0]

                        #########################################
                        if y[1] in in_file_assignments: # only attach an infile assignment to a node if that re assigned signal was actualy used in the assignment in question
                            for in_file_ass in in_file_assignments:
                                if y[1] == in_file_ass:
                                    infile_ass_checked = in_file_ass
                                    break
                        else:
                            infile_ass_checked = ""
                            ###################

                        new_node = TreeNode(x.mod, y[0], "module", x.name, find_str_sub, assing_subset, infile_ass_checked)
                        new_node.full_assignment_string = y[
                            0
                        ]  # assign the full LHS to s specila veriable
                        curent_node.add_child(new_node)
                        if x.vhdl_obj != None:
                            create_path(x.vhdl_obj, find_str_sub, new_node)

    return


treetop = target_vhdl
path_unsorted = create_path(treetop, find_str, nodes[0])

# # aditional assignments:
# for ass in assignments:
#     assigned_path_unsorted = create_path(treetop, ass[1], nodes[0])

path_tree = nodes[0].paths()

print(f"---------------------------------------------------")
print(f"Searching for {COLORS[4]}{find_str}{COLORS[7]} in {target_vhdl.data}")

for path in path_tree:
    for step in path:
        try: ################################################################### do this properly
            if len(step[0].infileassign)>0: ########################handle inflie assignments that change a signals name pre assignment ot a sub modukle
              infile_ass  = f" => '{step[0].infileassign}'"
            else:
                infile_ass = ""
            print(f"{step[0].assign_subset}'{infile_ass}{COLORS[7]}  --> ", end="")
        except:
            print(f" --> ", end="")
        if len(step) == 2:
            if verbose == False:
                print(f"{COLORS[1]}{step[0].if_mod_name}{COLORS[7]} = '{step[1]}' ", end="")
            else:
                print(
                    f"{COLORS[3]}{step[0].if_mod_name}{COLORS[7]} : {step[0].filename} = {COLORS[4]}'{step[1]}'{COLORS[7]} ", end=""
                )
        else:
            print(f"{step} = {COLORS[4]}'{find_str}", end="")
    print("")
    
print("")    
if len(search_term_assigned_to_port)>0: # if there were assignements of signals to ports in the TLD show them
    for sig_to_port in search_term_assigned_to_port:
        print(f"{COLORS[4]}'{sig_to_port[1]}'{COLORS[7]} assigned to port {COLORS[4]}'{sig_to_port[0][0]}'{COLORS[7]} of type {COLORS[4]}'{sig_to_port[0][1]}'{COLORS[7]} in {target_vhdl.data}")


print("")
print("---------------------------------------------------")


if verbose == True:  ##print the full line for each assignment for context
    print(full_assign_list)
    print(possible_assignments)
    # what to do with possible assignements


# def create_tree(data):
#     tree = graphviz.Digraph(format="png")
#     parent_node = None
#     existing_edges = set()

#     for path in data:
#         for item in path:
#             if isinstance(item, str):
#                 parent_node = item
#                 tree.node(parent_node, shape="note", label=f"{item}\\n{find_str}")
#             elif isinstance(item, list):
#                 if len(item) == 1:
#                     node_label = item[0]
#                     child_node = f"{node_label}_Self"
#                     tree.node(child_node, label=node_label)
#                     if parent_node is not None:
#                         edge = (parent_node, child_node)
#                         if edge not in existing_edges:
#                             tree.edge(parent_node, child_node)
#                             existing_edges.add(edge)
#                 elif len(item) == 2:
#                     node_label, edge_label = item
#                     node_label_mod_name = node_label.if_mod_name
#                     node_label_fine_name = node_label.filename
#                     child_node = f"{node_label}_{edge_label}"
#                     if verbose == False:
#                         tree.node(
#                             child_node,
#                             shape="box",
#                             label=f"{node_label_mod_name}\\n'{edge_label}'",
#                         )
#                     else:
#                         tree.node(
#                             child_node,
#                             shape="box",
#                             label=f"{node_label_mod_name} : {node_label_fine_name}\\n'{edge_label}'",
#                         )
#                     if parent_node is not None:
#                         edge = (parent_node, child_node)
#                         if edge not in existing_edges:
#                             tree.edge(parent_node, child_node)
#                             existing_edges.add(edge)
#                     parent_node = child_node
#                 else:
#                     raise ValueError("Invalid data format")
#     return tree


# data = path_tree

# tree_map = create_tree(data)
# tree_map.render("tree", format="png", view=True)


print("")
