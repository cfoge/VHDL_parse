from parse_vhdl import *
import plotly.express as px

#dependency search
root_dir = 'C:/BMD_builds/nios_timer/atemtvs3d1/src'
tld = 'C:/BMD_builds/nios_timer/atemtvs3d1/src/atemtvs3d1.vhd'
vhdl_files = []
#print("VHDL Files Found:")
for root, dirs, files in os.walk(root_dir):
    for file in files: 
        if file.endswith(".vhd"):
             #print(os.path.join(root, file))
             vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []

# make list of VHDL files as parsed objects
for files in vhdl_files:
    vhdl_file_as_obj.append(parse_vhdl(files))

target_vhdl = parse_vhdl(tld)

# search list and and attach dependent objects as childeren
for vhdl_o in vhdl_file_as_obj:
    for child in vhdl_o.children_name:
        for vhdl_objsB in vhdl_file_as_obj:
            if len(vhdl_objsB.data)>0:
                if vhdl_objsB.data[0] == child.mod:
                    child.vhdl_obj = (vhdl_objsB)
                    #vhdl_o.children_name.remove(child)
                    break

def print_child(object,depth,parent):
    if depth == 0:
        spacing =  ""
    if depth > 1:
        spacing =  "    " * (depth - 1) + "│   "
    else: 
        spacing = "    "
    if isinstance(object,vhdl_obj): 
        obj_type = "obj"
        child_var = object.children_name
        if (len(child_var) > 0):
            spacing = "    " * (depth)
            if obj_type == "obj":
                print (spacing + "├─ " + object.data[0])

                for child in range(len(child_var)):
                    hierachy_vis.append([object.data[0],child_var[child].name])
                    print_child(object.children_name[child], (depth + 1),object.data[0])


    if isinstance(object,instanc): 
        obj_type = "inst"
        temp1 = object.vhdl_obj
        if temp1 != None:
            if object.mod == "":
                print(spacing +"├─ " + object.name)
            else:
                print(spacing +"├─ " + object.mod + " : " + object.name)
            hierachy_vis.append([parent,object.name])
            print_child(object.vhdl_obj, (depth + 1), object.name)
        else:
            if object.mod == "":
                print(spacing +"├─ " + object.name)
            else:
                print(spacing +"├─ " + object.mod + " : " + object.name)
    return 

def extract(lst,addr):
    return [item[addr] for item in lst]


print("---------------------------------------------------")
hierachy_vis = [['',target_vhdl.data[0]]]
for vhdl_objs in vhdl_file_as_obj:
    if len(vhdl_objs.data) > 0 :
        if (target_vhdl.data[0] in vhdl_objs.data[0] ):
            # print(vhdl_objs.data[0])
            print_child(vhdl_objs,0,"")
print("---------------------------------------------------")

names_val = extract(hierachy_vis,1)
parents_val = extract(hierachy_vis,0)

fig = px.treemap(
    names = names_val[0:20], # there cant be a perent referenced that hasnt been listed in the names yet!!
    parents = parents_val[0:20]
    #     names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    # parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()

print("")