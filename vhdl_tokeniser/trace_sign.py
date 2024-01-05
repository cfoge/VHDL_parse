# A command line program for tracing signals through hieracys of of vhdl docs
# Robert D Jordan 2022

import os
from token_test import *
import graphviz

########################### search node
class TreeNode(object):

    def __init__(self, fname,search,hdl_type, if_mod_name, assigned_to):
            self.filename = fname
            self.search_term = search
            self.type = hdl_type
            self.if_mod_name = if_mod_name
            self.assigned_to = assigned_to
            self.parent = []
            self.children = []
            
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
        self.root = TreeNode('ROOT',"NONE","")

    def preorder_trav(self, node):
        if node is not None:
            print (node.data)
            print("   " , end="" )
            if len(node.children) != 0:
                for n in node.children:
                    for x in range(node.depth):
                        print("   " , end="" )
                    print("|--" , end="" )
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
    if (node.type == "file"):
        path_list = node.filename
    elif (node.type == "port"):
        path_list = node.search_term
    elif (node.type == "signal"):
        path_list = node.search_term
    elif (node.type == "component port"):
        path_list = node.search_term
    elif (node.type == "module"):
        # path_list = [f"{node.if_mod_name}:{node.filename}" , node.assigned_to]
        path_list = [node , node.assigned_to]
    return path_list
    


root_dir = 'C:/Users/robertjo/Documents/other/28_7_23_ems/src'
# root_dir = 'C:/BMD_builds/ava_2019_fresh'
target_vhdl = parse_vhdl('C:/Users/robertjo/Documents/other/28_7_23_ems/src/digital_side/test_1_build/test_digital_side.vhd')
# target_vhdl = parse_vhdl('C:/BMD_builds/ava_2019_fresh/atemava1/src/atemava1.vhd')
# search for arg 2 in each each part of the top level file
# search for other lines involving this signal
#search each child for 
# find_str = 'f1i_vclk_p'
# find_str = 'rst'
find_str = 'RBG_out'
# find_str = 'genlock_sof'
verbose = False

vhdl_files = []
#print("VHDL Files Found:")
# for root, dirs, files in os.walk('C:/Users/robertjo/Documents/other/28_7_23_ems/src'):
for root, dirs, files in os.walk(root_dir):

    for file in files: 
        if file.endswith(".vhd"):
             #print(os.path.join(root, file))
             vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []

# make list of VHDL files as parsed objects
for files in vhdl_files:
    vhdl_file_as_obj.append(parse_vhdl(files))



for vhdl_o in vhdl_file_as_obj: # make external function!!!
    for child in vhdl_o.children_name:
        for vhdl_objsB in vhdl_file_as_obj:
            if vhdl_objsB.data != None: # data is none if the file is just constants or functions or somthing like that
                if len(vhdl_objsB.data)>0:
                    if vhdl_objsB.data == child.mod:
                        child.vhdl_obj = (vhdl_objsB)
                        #vhdl_o.children_name.remove(child)
                        break









nodes = []
search_list_modules = []
assignments = []
nodes.append(TreeNode(target_vhdl.data,find_str,"file", "", ""))

###################################


def create_path(vhdl_obj_in, find_str, curent_node):
    find_str_sub = ''
    # this part looks for ways that the signals name may have changed via being assigned to another signal
    for x in vhdl_obj_in.assign: #find asignments in assignment not in functions, processes ect..
        if (find_str in x[0] or find_str in x[1] ):       
                if (x[1] == find_str):   # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                    
                    assignments.append([vhdl_obj_in.data, x[0],x[1] ]) # filen name, assigned to, line number
                    temp = [find_str]
                    find_str = temp
                    find_str.append(x[0])
                    break
    for y in vhdl_obj_in.process: #find asignments in processes
        for x in y[2]:
            if (find_str in x[0] or find_str in x[1] ):       
                    if (x[1] == find_str):   # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                        
                        assignments.append([vhdl_obj_in.data, x[0],x[1] ]) # filen name, assigned to, line number
                        temp = [find_str]
                        find_str = temp
                        find_str.append(x[0])
                        break
    if type(find_str) == list:
        for string in find_str:  
        # string = find_str
            for x in vhdl_obj_in.children_name: # search for assignments in sub modules that have our search term going into them
                for y in x.port:
                    if (string in y[1]):
                        # string_out = y[0] + " => " + y[1]
                        if (y[1] == string):
                            find_str_sub = y[0]
                            new_node = TreeNode(x.mod,y[0],"module", x.name, find_str_sub)
                            
                            curent_node.add_child(new_node)
                            if x.vhdl_obj != None:
                                create_path(x.vhdl_obj,find_str_sub, new_node)
    else:
        string = find_str
        for x in vhdl_obj_in.children_name: # search for assignments in sub modules that have our search term going into them
            for y in x.port:
                if (string in y[1]):
                    # string_out = y[0] + " => " + y[1]
                    if (y[1] == string):
                        find_str_sub = y[0]
                        new_node = TreeNode(x.mod,y[0],"module", x.name, find_str_sub)
                        
                        curent_node.add_child(new_node)
                        if x.vhdl_obj != None:
                            create_path(x.vhdl_obj,find_str_sub, new_node)





    return 

treetop = None
for entity in vhdl_file_as_obj:
    if entity.data == target_vhdl.data:
        treetop = entity
path_unsorted = create_path(treetop,find_str,nodes[0])

# aditional assignments:
# for ass in assignments:
#     assigned_path_unsorted = create_path(treetop,ass[1],nodes[0])

path_tree = nodes[0].paths()

print("---------------------------------------------------")
print ("Searching for " + find_str + " in " + target_vhdl.data)

for path in path_tree:
    for step in path:
        print( " --> ",end='')
        if len(step)==2:
            if verbose == False:
                print(f"{step[0].if_mod_name} = '{step[1]}' " ,end='')
            else:
                print(f"{step[0].if_mod_name} : {step[0].filename} = '{step[1]}' " ,end='')
        else:
            print(f"{step} = '{find_str}' " ,end='')
    print("")
print("")
print("---------------------------------------------------")


def create_tree(data):
    tree = graphviz.Digraph(format='png')
    parent_node = None
    existing_edges = set()
    
    for path in data:
        for item in path:
            if isinstance(item, str):
                parent_node = item
                tree.node(parent_node, shape='note', label= f"{item}\\n{find_str}")
            elif isinstance(item, list):
                if len(item) == 1:  
                    node_label = item[0]
                    child_node = f"{node_label}_Self"
                    tree.node(child_node, label=node_label)
                    if parent_node is not None:
                        edge = (parent_node, child_node)
                        if edge not in existing_edges:
                            tree.edge(parent_node, child_node)
                            existing_edges.add(edge)
                elif len(item) == 2:  
                    node_label, edge_label = item
                    node_label_mod_name = node_label.if_mod_name
                    node_label_fine_name = node_label.filename
                    child_node = f"{node_label}_{edge_label}"
                    if verbose == False:
                        tree.node(child_node, label=f"{node_label_mod_name}\\n{edge_label}")
                    else:
                        tree.node(child_node, label=f"{node_label_mod_name} : {node_label_fine_name}\\n{edge_label}")
                    if parent_node is not None:
                        edge = (parent_node, child_node)
                        if edge not in existing_edges:
                            tree.edge(parent_node, child_node)
                            existing_edges.add(edge)
                    parent_node = child_node
                else:
                    raise ValueError("Invalid data format")
    return tree


data = path_tree

tree_map = create_tree(data)
tree_map.render('tree', format='png', view=True)


print("")
