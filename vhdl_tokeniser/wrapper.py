import argparse
from token_test import parse_vhdl
import os

def generate_vhdl_wrapper(file_paths, wrapper_name, verbose=False, save_to_file=False, make_signals=False):
    decoded_list = []

    for file_path in file_paths:
        decoded_list.append(parse_vhdl(file_path, verbose))

    lib_list = []
    generic_list = []
    port_list = []
    signals_list = ''

    for decoded in decoded_list:
        for lib in decoded.lib:
            lib_list.append(lib.lower())
        try:
            genlen = max(len(gen[0]) for gen in decoded.generic)
        except:
            # print("no generics found")
            genlen = 0
        try:
            portlen = max(len(port[0]) for port in decoded.port)
        except:
            # print("no port found")
            portlen = 0

        genspacing = genlen + 4
        portspacing = portlen + 4
        vb = ""
        with open("wrapper_out.vhdl", "a") as f:
            f.write(f"{decoded.data}_i : entity work.{decoded.data} \n")
            if len(decoded.generic) > 0:
                f.write(f"generic map (\n")
                for gen in decoded.generic[:-1]:
                    if verbose:
                        vb = f"--{gen[1]} width = {gen[2]}"
                    spaces = " " * (genspacing - len(gen[0]))
                    f.write(f"{gen[0]}{spaces}=> {gen[0]}, {vb}\n")
                gen = decoded.generic[-1]
                if verbose:
                    vb = f"--{gen[1]} width = {gen[2]}"
                spaces = " " * (genspacing - len(gen[0]))
                f.write(f"{gen[0]}{spaces}=> {gen[0]} {vb}\n")
                f.write(f");\n")
            if len(decoded.port) > 0:
                f.write(f"port map (\n")
                for port in decoded.port[:-1]:
                    if verbose:
                        vb = f"--{port[1]} width = {port[2]}"
                    spaces = " " * (portspacing - len(port[0]))
                    f.write(f"{port[0]}{spaces}=> {port[0]}, {vb}\n")
                port = decoded.port[-1]
                if verbose:
                    vb = f"--{port[1]} width = {port[2]}"
                spaces = " " * (portspacing - len(port[0]))
                f.write(f"{port[0]}{spaces}=> {port[0]} {vb}\n")
                f.write(f");\n")
                f.write(f"\n")

        signals = ''
        if make_signals == True:
            for port in decoded.port:
                end_of_port = ""
                if port[3] != 1:
                    port_msb = port[3] -1
                    end_of_port = end_of_port + f"({port_msb} downto 0)"
                if port[4] != None:
                    end_of_port = end_of_port + f" := {port[4]}"
                signals = signals + f"signal {port[0]} : {port[2]}{end_of_port}; \n"
        signals_list = signals_list + signals
  
    # Remove duplicates from the Library list
    temp = [idx for idx, val in enumerate(lib_list) if val in lib_list[:idx]]
    clean_lib_list = [ele for idx, ele in enumerate(lib_list) if idx not in temp]

    contents = None
    header = "--Auto generated VHDL Wrapper\n"
    footer = ""

    with open("wrapper_out.vhdl", 'r') as contents:
        save = contents.read()

    # Generate header
    for lib in clean_lib_list:
        if "." not in lib:
            header = header + f"LIBRARY {lib}; \n"
        else:
            header = header + f"USE {lib}; \n"

    header = header + f"\nentity {wrapper_name} is \n"


    # for port in port_list:
    #     end_of_port = ""
    #     if port[3] != 1:
    #         port_msb = port[3] - 1
    #         end_of_port = end_of_port + f"({port_msb} downto 0)"
    #     if port[4] is not None:
    #         end_of_port = end_of_port + f" := {port[4]}"
    #     header = header + f"{port[0]} : {port[1]} {port[2]}{end_of_port}; \n"

    header = header + f"end {wrapper_name}; \n\narchitecture rtl of {wrapper_name} is \n"

    header = header + f"begin \n"

    with open("wrapper_out.vhdl", 'w') as contents:
        contents.write(header)

    if make_signals == True:
        save_out = signals_list + "\n" + save + footer + "\nend rtl;\n"  # add the file contents and the footer/end of the file back in.
    else:
        save_out = save + footer + "\nend rtl;\n"  # add the file contents and the footer/end of the file back in.


    with open("wrapper_out.vhdl", 'a') as contents:
        contents.write(save_out)
    print(header)
    print(save_out)
    if save_to_file != True:
        os.remove("wrapper_out.vhdl")


if __name__ == "__main__":
    # Add argparse for command-line arguments
    parser = argparse.ArgumentParser(description='VHDL wrapper generator')
    parser.add_argument('files', type=str, nargs='+', help='Input VHDL files')
    parser.add_argument('-n', '--name', type=str,default='wrapper', help='Wrapper entity name')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    parser.add_argument('-sig', '--signal', action='store_true', help='create signals from the ports of modules beign wrapped')
    parser.add_argument('-s', '--save', action='store_true', help='Save output to file')

    # # Check if the correct number of arguments is provided
    args = parser.parse_args()

    # # Initialize save_to_file based on command-line argument
    save_to_file = args.save

    # Generate VHDL wrapper
    generate_vhdl_wrapper(args.files, args.name, verbose=args.verbose, save_to_file=save_to_file, make_signals=args.signal)
    # files = ["tests/test2.vhdl", "tests/test1.vhdl"]
    # generate_vhdl_wrapper(files, "wraper_wth_sig", verbose=False, save_to_file=False, make_signals=True)