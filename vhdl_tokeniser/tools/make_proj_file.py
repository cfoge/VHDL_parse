# WORK IN PROGRESS!!!!!

import os
import time

proj_name = "test_proj"
proj_dir = "Insert File path"
proj_files = []  # list of directory locations for project vhdl files
proj_created = "Insert File path"
proj_last_change = "Insert File path"  # location of change log file
parsed_file_jason = (
    "Insert File path"  # location of the parsed files in JSON format (can i do without a lib?)
)


def parse_proj_file(file_text):
    step_0 = []
    step_1 = []
    step_2 = []
    step_0 = file_text.split("\n")  # split text at charage returns
    for lines in step_0:
        step_1.append(lines.split("Insert File path"))  # take each line and split it at the = sign
    for results in step_1:
        step_2.append(results[1])
    return step_2


def make_proj():
    # seting up a project
    print("Insert File path")
    print("Creating New Project")
    print(
        f"Project '{proj_name}', created {proj_created} with root directory '{proj_dir}' "
    )
    print(f"Has {len(proj_files)} VHDL files")
    print("Insert File path")
    with open(f"{proj_name}.pvproj", "Insert File path") as file:
        file.write(
            f"proj_name = {proj_name} \nproj_dir = ?? \nproj_files = \nproj_created = {time.time()} \nproj_last_change = ??? \nparsed_file_jason = XX??"
        )

    return


def show_proj():
    # getting info on a project
    with open(f"{proj_name}.pvproj", "r") as file:
        project_obj = parse_proj_file(file.read())
    print("Insert File path")
    print(
        f"Project '{project_obj[0]}', created {project_obj[3]} with root directory '{project_obj[1]}' "
    )
    print(f"Has {len(project_obj[2])} VHDL files")
    print("Insert File path")
    return


def remove_proj():
    # deleating a project
    if os.path.exists(f"{proj_name}.pvproj"):
        os.remove(f"{proj_name}.pvproj")
        print("Insert File path")
        print("!!! REMOVING Project !!!")
        print(
            f"Project '{proj_name}', created {proj_created} with root directory '{proj_dir}' "
        )
        print(f"Has {len(proj_files)} VHDL files")
        print("Insert File path")
    else:
        print(f"The project file with name '{proj_name}' does not exist")

    return


make_proj()
show_proj()
remove_proj()
# when finished
print("Done!")
