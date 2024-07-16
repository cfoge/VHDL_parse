# This script creates a hiracical representation of your VHDL project.
# It will print to the console which VHDL modules are instanciated by which other module

from token_test import *
import os
import argparse

# ANSI escape codes for colors
COLORS = [
    "\033[97m",  # WHITE
    "\033[92m",  # GREEN
    "\033[94m",  # BLUE
    "\033[93m",  # YELLOW
    "\033[96m",  # CYAN
    "\033[95m",  # MAGENTA
    "\033[0m",  # RESET
]

hierarchy_vis = []


def create_tree(parents, children):
    tree = {}
    for parent, child in zip(parents, children):
        if parent not in tree:
            tree[parent] = []
        if child not in tree:
            tree[child] = []
        tree[parent].append(child)
    return tree


def attach_dependent_objects(
    parent_vhdl_obj, entity_texts_with_path
):  # this function creates a vhdl object hieracy of only instanciated vhdl entitys
    # for modules in entity_texts_with_path:
        # if "am_audio" in modules[1]:
        #     print()
    try:
        for child in parent_vhdl_obj.children_name:
            for vhdl_found_entities in entity_texts_with_path:
                if len(vhdl_found_entities[0]) > 0:
                    # if "am_audio_" in vhdl_found_entities[0]:
                    #     print("")
                    if vhdl_found_entities[0] == child.mod:
                        # Add a "." with no return to the terminal to show that it is still allive when parsing huge numbers of files
                        new_child = parse_vhdl(vhdl_found_entities[1])
                        child.vhdl_obj = new_child
                        attach_dependent_objects(
                            new_child, entity_texts_with_path
                        )  # Recursive call
                        break
    except Exception as e:
        error_log.append(["file_path_error", e])


# dependency search
def cl_depend(root_dir, tld, print_url, exclude_dirs = []):
    vhdl_files = []
    for root, dirs, files in os.walk(root_dir):
        # Check if the current directory is in the list of directories to exclude
        if any(excluded_dir in root for excluded_dir in exclude_dirs):
            continue
        for file in files:
            if file.endswith(".vhd") or file.endswith(".vhdl"):
                # print(os.path.join(root, file))
                vhdl_files.append(os.path.join(root, file))

    vhdl_file_as_obj = []
    print(f"Printing VHDL Module Hierachy")
    print(f"{len(vhdl_files)} vhdl files found")
    if len(vhdl_files) == 0:
        exit()

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
            unreadible_files += 1
    print(f"{unreadible_files} vhdl files unreadable")

    ###### FIND AND REMOVE DUPLICTES, VHDL files with the same name that contain the same named modules can cause issues
    # Dictionary to store encountered filenames and their corresponding paths
    filename_to_path = {}

    # List to store duplicate filenames
    duplicate_filenames = []

    # Iterate over entity_texts_with_path
    for entity_text, file_path in entity_texts_with_path:
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
    for entity_text, file_path in entity_texts_with_path:
        filename = os.path.basename(file_path)
        if filename in duplicate_filenames:
            # Skip duplicates
            continue

        # Remove file format from name
        if "." in filename:
            filename = filename.split(".")[0]
        # Add non-duplicates to the unique list
        entity_texts_with_path_unique.append([entity_text, file_path])
        # if "am_audio" in entity_text:
        #     print()

    # Update entity_texts_with_path to contain only unique filenames
    vhdl_files = entity_texts_with_path_unique

    # Print the number of duplicate files found
    print(f"{len(duplicate_filenames)} duplicate files found")
    if len(duplicate_filenames) > 0:
        print(
            "Duplicate files with the same name can create issues when searching through VHDL hierarchies, so duplicates have been removed\n"
        )

    target_vhdl = parse_vhdl(tld)

    # Attach dependent objects
    attach_dependent_objects(target_vhdl, vhdl_files)


    def print_child(object, depth, parent, print_url):
        url = ""
        if depth == 0:
            spacing = ""
            object.modname = object.data
            if print_url == True:
                url = object.url
            print(object.data + " " + url)
        if depth > 1:
            spacing = "    " * (depth - 1) + "   "
        else:
            spacing = "    "
        if isinstance(object, vhdl_obj):
            obj_type = "obj"
            child_var = object.children_name
            if len(child_var) > 0:
                spacing = "    " * (depth)
                if obj_type == "obj":
                    # print (spacing + "├─ " + object.data[0])

                    for child in range(len(child_var)):
                        # hierachy_vis.append([object.modname,child_var[child].name,depth,child_var[child].mod])
                        print_child(
                            object.children_name[child],
                            (depth + 1),
                            object.data,
                            print_url,
                        )

        elif isinstance(object, instanc):
            if (print_url == True) and (object.vhdl_obj != None):
                url = object.vhdl_obj.url
            obj_type = "inst"
            temp1 = object.vhdl_obj
            if temp1 != None:
                object.vhdl_obj.modname = object.name
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "":
                    print(color + spacing + "├─ " + object.name + " " + url)
                else:
                    print(
                        color
                        + spacing
                        + "├─ "
                        + object.mod
                        + " : "
                        + object.name
                        + " "
                        + url
                    )
                hierachy_vis.append([parent, object.name, depth, object.mod])
                print_child(object.vhdl_obj, (depth + 1), object.name, print_url)
            else:
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "":
                    print(color + spacing + "├─ " + object.name + " " + COLORS[6] + url)
                else:
                    print(
                        color
                        + spacing
                        + "├─ "
                        + object.mod
                        + " : "
                        + object.name
                        + " "
                        + url
                    )
        return

    print("---------------------------------------------------")
    print(f"Hierarchy of {target_vhdl.data} is: \n")
    global hierachy_vis
    hierachy_vis = []

    def print_child_with_name(
        vhdl_obj_in, indent_level, indent_str, print_url, hierachy_vis
    ):
        # try:
        if isinstance(vhdl_obj_in, instanc):
            vhdl_obj = vhdl_obj_in.vhdl_obj
            modname = vhdl_obj_in.name
        else:
            vhdl_obj = vhdl_obj_in
            modname = ""

        color_index = indent_level % (len(COLORS) - 1)  # Exclude RESET color
        color = COLORS[color_index]
        if print_url == True:
            url = vhdl_obj.url
        else:
            url = ""
        if indent_level != 0:
            arrow = "├─"
        else:
            arrow = ""

        if vhdl_obj.data is not None and len(vhdl_obj.data) > 0:
            if modname == "":
                print(f"{color}{indent_str}{arrow} {vhdl_obj.data} {url}")
            else:
                print(f"{color}{indent_str}{arrow} {modname} : {vhdl_obj.data} {COLORS[6]}{url}")
                # hierachy_vis.append([parent,vhdl_obj.name,vhdl_obj,object.mod])
        for child in vhdl_obj.children_name:
            if child.vhdl_obj is not None:
                print_child_with_name(
                    child, indent_level + 1, indent_str + "  ", print_url, hierachy_vis
                )
            else:
                color_index_tmp = (indent_level+1) % (len(COLORS) - 1)  # if the child has no VHDL object attched to it, we didnt find the vhdl file for it just print the module name.
                color_tmp = COLORS[color_index_tmp]
                if indent_level == 0:
                    arrow = "├─"
                indent_str_tmp = indent_str + "  "
                print(f"{color_tmp}{indent_str_tmp}{arrow} {child.mod} : {child.name}  {COLORS[6]}{url}")
        # except Exception as e:
        #     print('error')
        #     error_log.append(["print Hierarchy error", e])
        return hierachy_vis

    try:
        if target_vhdl.data is not None and len(target_vhdl.data) > 0:
            print_child_with_name(target_vhdl, 0, "", print_url, hierachy_vis)
    except Exception as e:
        error_log.append(["print Hierarchy error", e])

    print(COLORS[-1])
    print("---------------------------------------------------")
    # #################################
    # # for error in error_log:
    # #     print(error)
    # # Create Plotly tree map
    # fig = go.Figure(
    #     go.Treemap(
    #         labels=[lab for _, _, _, lab in hierachy_vis],
    #         parents=[parent for parent, _, _, _ in hierachy_vis],
    #         customdata=[mod for _, _, mod, _ in hierachy_vis],
    #         # hoverinfo=customdata,
    #         marker=dict(
    #             # colors=[COLORS[depth % (len(COLORS) - 1)] for _, _, depth, _ in hierachy_vis],
    #             line=dict(width=1, color="black")
    #         ),
    #     )
    # )

    # fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()


    return


if __name__ == "__main__":
    # Add argparse for command-line arguments
    parser = argparse.ArgumentParser(description="VHDL wrapper generator")
    parser.add_argument("tld", type=str, help="Input VHDL file (Your top level design)")
    parser.add_argument(
        "-d", "--directory", type=str, help="root directory for vhdl project"
    )
    parser.add_argument(
        "-ex", "--exclude", type=str, help="directory names to exclude form search"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print verbose output"
    )

    # # Check if the correct number of arguments is provided
    args = parser.parse_args()


    tld = args.tld
    ROOT_DIR = os.path.dirname(tld)
    root_dir = args.directory if args.directory is not None else ROOT_DIR

    print("---------------------------------------------")
    print(f"Running Show VHDL Hieracy of TLD '{tld}'")

    cl_depend(root_dir, tld, args.verbose)


    print("")
