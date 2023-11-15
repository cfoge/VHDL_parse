import argparse

def extract_module_content(file_path, verbose=False, save_to_file=False):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()

            # Find the starting and ending indices of each module
            start_indices = [i for i, line in enumerate(content) if line.startswith("entity")]
            end_indices = [i for i, line in enumerate(content) if line.startswith("end")]

            # Extract content between "entity" and "end entity"
            extracted_content = ""
            for start_index in start_indices:
                end_index = min(end_index for end_index in end_indices if end_index > start_index)
                module_content_lines = content[start_index:end_index]

                # Remove comments from each line
                module_content = ""
                for line in module_content_lines:
                    if "--" in line and not verbose:
                        no_comments = line.split("--")
                        module_content += no_comments[0] + '\n'
                    else:
                        module_content += line

                # Join the lines to form the module content
                module_content_out = ''.join(module_content).replace("entity", "module").replace("end entity", "end module").strip()

                # Extract the name of the entity
                entity_name = module_content_out.split()[1] if module_content_out else "unknown_entity"

                # Append the extracted content to the result
                extracted_content += f"{module_content_out}\nend module {entity_name};\n"

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Print the extracted content to the terminal
    print(extracted_content)

    # Save to file if save_to_file is True
    if save_to_file:
        with open("component_out.txt", "w") as output_file:
            output_file.write(extracted_content)

if __name__ == "__main__":
    # Add argparse for command-line arguments
    parser = argparse.ArgumentParser(description='VHDL module content extractor')
    parser.add_argument('file_path', type=str, help='Path to the VHDL file')
    parser.add_argument('-v','--verbose', action='store_true', help='Print comments in the VHDL file')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to "component_out.txt" file')

    # Parse command-line arguments
    args = parser.parse_args()

    # Extract module content
    extract_module_content(args.file_path, verbose=args.verbose, save_to_file=args.save)
