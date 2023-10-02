def extract_module_content(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()

            # Find the starting and ending indices of each module
            start_indices = [i for i, line in enumerate(content) if line.startswith("entity")]
            end_indices = [i for i, line in enumerate(content) if line.startswith("end entity")]

            # Extract content between "entity" and "end entity"
            for start_index in start_indices:
                end_index = min(end_index for end_index in end_indices if end_index > start_index)
                module_content_lines = content[start_index:end_index]

                # Remove comments from each line
                module_content = ""
                for line in module_content_lines:
                    if "--" in line:
                        no_coments = line.split("--")
                        module_content = module_content + no_coments[0] +'\n'
                    else:
                        module_content = module_content + line
                # Join the lines to form the module content

                module_content_out = ''.join(module_content).replace("entity", "module").replace("end entity", "end module").strip()

                # Extract the name of the entity
                entity_name = module_content_out.split()[1] if module_content_out else "unknown_entity"


                # Print the extracted content and append the entity name to the end
                print(f"Module Content:\n{module_content_out}\nend module {entity_name};\n")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.txt' with the path to your text file
# Set verbose to True if you want to print comments
extract_module_content('fan_control.vhd', verbose=False)
