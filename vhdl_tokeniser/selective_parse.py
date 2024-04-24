import os
from token_test import *

def attach_dependent_objects(parent_vhdl_obj, entity_texts_with_path): # this function creates a vhdl object hieracy of only instanciated vhdl entitys
    try:
        for child in parent_vhdl_obj.children_name:
            for vhdl_found_entities in entity_texts_with_path:
                if len(vhdl_found_entities[0]) > 0:
                    if vhdl_found_entities[0] == child.mod:
                        new_child = parse_vhdl(vhdl_found_entities[1])
                        child.vhdl_obj = new_child
                        attach_dependent_objects(new_child, entity_texts_with_path)  # Recursive call
                        break
    except Exception as e:
        error_log.append(["file_path_error", e])

root_dir = 'C:/BMD_builds/audio_a_release/oceanus/src/'
find_str = 'voip_rx_anc_vpid_array'
verbose = True

vhdl_files = []

# Traverse through directories and find VHDL files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".vhd"):
            vhdl_files.append(os.path.join(root, file))

entity_texts_with_path = []

# Read each VHDL file, extract text between 'entity' and 'is', and store it with file path
for file_path in vhdl_files:
    with open(file_path, 'r') as f:
        file_text = f.read()
        # Extract text between 'entity' and 'is'
        start_index = file_text.find('entity') + len('entity')
        end_index = file_text.find('is', start_index)
        if start_index != -1 and end_index != -1:
            entity_text = file_text[start_index:end_index].strip()
            # Exclude if the text contains "\n" unless it's at the very end
            if '\n' not in entity_text[:-1]:
                entity_texts_with_path.append([entity_text, file_path])

print(f"{len(vhdl_files)} VHDL files found")
print(f"{len(entity_texts_with_path)} entities extracted")

target_vhdl = parse_vhdl('C:/BMD_builds/audio_a_release/oceanus/src/Oceanus.vhd')

# search list and and attach dependent objects as childerenfor vhdl_o in target_vhdl:
# try:
#     for child in target_vhdl.children_name:
#         for vhdl_found_entities in entity_texts_with_path:
#                 if len(vhdl_found_entities[0])>0:

#                     if vhdl_found_entities[0] == child.mod:
#                         new_child = parse_vhdl(vhdl_found_entities[1])
#                         child.vhdl_obj = new_child
#                         #vhdl_o.children_name.remove(child)
#                         break
# except Exception as e:
#     error_log.append(["file_path_error",e])
attach_dependent_objects(target_vhdl, entity_texts_with_path)
print("")
