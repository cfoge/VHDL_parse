# A command line program for tracing signals through hieracys of of vhdl docs
# Robert D Jordan 2022

import sys
import re
import os
from parse_vhdl import *


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

def get_data(node):
    path_list = ""
    if (node.type == "file"):
        path_list = str("file: " + node.filename[0])
    if (node.type == "port"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "signal"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "component port"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "module"):
        path_list = str(node.type + ": "+ node.if_mod_name + ": "+ node.assigned_to +" <= "+ node.search_term)
    return path_list

def get_data_slim(node):
    path_list = ""
    if (node.type == "file"):
        path_list = node.filename[0]
    if (node.type == "port"):
        path_list = node.search_term
    if (node.type == "signal"):
        path_list = node.search_term
    if (node.type == "component port"):
        path_list = node.search_term
    if (node.type == "module"):
        path_list = [node.if_mod_name , node.assigned_to]
    return path_list
    



vhdl_files = []
#print("VHDL Files Found:")
for root, dirs, files in os.walk('C:/BMD_builds/time_code_in/atemtvs3d1/src'):
    for file in files: 
        if file.endswith(".vhd"):
             #print(os.path.join(root, file))
             vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []

# make list of VHDL files as parsed objects
for files in vhdl_files:
    vhdl_file_as_obj.append(parse_vhdl(files))

target_vhdl = parse_vhdl('C:/BMD_builds/time_code_in/atemtvs3d1/src/atemtvs3d1.vhd')

# search list and and attach dependent objects as childeren
# for vhdl_o in vhdl_file_as_obj:
#     if(not(vhdl_o.data == target_vhdl.data)):
#        # for child in vhdl_o.children_name:
#             for vhdl_objsB in target_vhdl.children_name:
#                 if len(vhdl_objsB.mod)>0:
#                     if vhdl_objsB.mod == vhdl_o.data:
#                         target_vhdl.children.append(vhdl_o) #this needs a way to signal a file change?
#                     # target_vhdl.children_name.remove(child)
#                         break
for vhdl_o in vhdl_file_as_obj:
    for child in vhdl_o.children_name:
        for vhdl_objsB in vhdl_file_as_obj:
            if len(vhdl_objsB.data)>0:
                if vhdl_objsB.data[0] == child.mod:
                    # vhdl_o.children.append(vhdl_objsB)
                    child.vhdl_obj.append(vhdl_objsB)

                    #vhdl_o.children_name.remove(child)
                    break


# search for arg 2 in each each part of the top level file
# search for other lines involving this signal
#search each child for 
find_str = 'clk_25'




####################when you find somthing crate a node and link it together
# create dependency graph from results 
# tr = Tree()
# n1 = tr.root
nodes = []
search_list_modules = []
# for i in range(len(instance_final_nodup)):
#     nodes.append(TreeNode(instance_final_nodup[i]))
# for i in nodes:
#     n2.add_child(i)
# for i in nodes:
#     n2.add_depth(n2)
nodes.append(TreeNode(target_vhdl.data,find_str,"file", "", ""))
#  fname,find_str,hdl_type, if_mod_name, assigned_to):

###################################


def create_path(vhdl_obj_in, find_str, curent_node):
    port_search = False
    sig_search = False
    comp_search = False
    find_str_sub = ''
    # if(vhdl_obj_in.type == "file"): # because im not storing it corectly 
       # nodes.append(TreeNode(vhdl_obj_in.data,find_str,"file", "", ""))
    # else:
        # for x in vhdl_obj_in.port:
        #     if (find_str in x): 
        #         tmp1 = x.split(":")
        #         tmp1[0] = tmp1[0].strip()
        #         tmp1[1] = tmp1[1].strip()
        #         if (tmp1[0] == find_str):
        #             nodes.append(TreeNode(vhdl_obj_in.data,find_str,"port", "", ""))
        #             port_search = True
        #             break

        # if (port_search == False):
        #     for x in vhdl_obj_in.signal:
        #         if (find_str in x[0]):          
        #                 nodes.append(TreeNode(vhdl_obj_in.data,find_str,"signal", "", ""))
        #                 sig_search = True
        #                 break

        # if (sig_search == False)&(port_search == False) :
        #     for y in vhdl_obj_in.component:
        #         for x in y.port:
        #             if (find_str in x): 
        #                 tmp1 = x.split(":")
        #                 tmp1[0] = tmp1[0].strip()
        #                 tmp1[1] = tmp1[1].strip()
        #                 if (tmp1[0] == find_str):
        #                     nodes.append(TreeNode(vhdl_obj_in.data,find_str,"component port", "", ""))
        #                     comp_search = True
        #                     break

    for x in vhdl_obj_in.children_name:
        for y in x.port:
            if (find_str in y[1]):
                string_out = y[0] + " => " + y[1]
                if (y[1] == find_str):
                    find_str_sub = y[0]
                    if len(x.mod)==0:
                        new_node = TreeNode(x.name,y[0],"module", x.name, find_str_sub)
                    else:
                        new_node = TreeNode(x.mod,y[0],"module", x.name, find_str_sub)
                    
                    curent_node.add_child(new_node)
                    if len(x.vhdl_obj)>0:
                        create_path(x.vhdl_obj[0],find_str_sub, new_node)


    # for node in nodes:
    #     if (node.type == "port")or(node.type == "signal")or(node.type == "component port") :
    #             previous_node = nodes.index(node)-1
    #             nodes[previous_node].add_child(node)
    #     if (node.type == "module"):
            
    #         for sub_mod in node.children:
    #             if (node.find_str == sub_mod.data):
                    
    #                 create_path(sub_mod,find_str_sub,curent_node)
    #                 break
            
    #         # nodes[1].add_child(node)
    #         nodes[0].add_child(node)


    return 


# path_unsorted = create_path(target_vhdl,find_str)
path_unsorted = create_path(vhdl_file_as_obj[0],find_str,nodes[0])



path_tree = nodes[0].paths()



print("---------------------------------------------------")
print ("Searching for " + find_str + " in " + target_vhdl.data[0])

for path in path_tree:
    for step in path:
        print( " --> ",end='')
        if len(step)==2:
            print(step[0] + " : " + step[1] ,end='')
        else:
            print(step ,end='')
    print("")
print("")
print("---------------------------------------------------")

