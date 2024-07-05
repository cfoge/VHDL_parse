import sys
import os
import argparse
from token_test import parse_vhdl

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Test Bench Generator: Generates a test bench for a VHDL file.')
    parser.add_argument('vhdl_file', type=str, help='The VHDL file to generate the test bench for.')
    args = parser.parse_args()

    # Extract argument
    files_to_tb = args.vhdl_file

    # Parse the VHDL file
    decoded = parse_vhdl(files_to_tb, True)
    tb_name = f"TB_{decoded.data}"

    verbose = True
    all_generics_2_toplevel = True
    all_ports_2_toplevel = True

    lib_list = []
    generic_list = []
    port_list = []

    for lib in decoded.lib:
        lib_list.append(lib.lower())
    genlen = 0
    for gen in decoded.generic:
        generic_list.append(gen)
        x = len(gen[0])
        if x > genlen:
            genlen = x
    portlen = 0
    for port in decoded.port:
        port_list.append(port)
        x = len(port[0])
        if x > portlen:
            portlen = x

    genspacing = genlen + 4
    portspacing = portlen + 4

    print(f"Generating test bench for {files_to_tb}...")
    
    f = open(f"{tb_name}.vhdl", "a")
    f.write(f"UUT : entity work.{decoded.data} \n")
    if len(decoded.generic) > 0:
        f.write(f"generic map (\n")
        for gen in decoded.generic[:-1]:
            if verbose:
                vb = f"--{gen[1]}, {gen[2]} "
            spaces = " " * (genspacing - len(gen[0]))
            f.write(f"{gen[0]}{spaces}=> {gen[0]}, {vb}\n")
        gen = decoded.generic[-1]
        if verbose:
            vb = f"--{gen[1]}, {gen[2]}"
        spaces = " " * (genspacing - len(gen[0]))
        f.write(f"{gen[0]}{spaces}=> {gen[0]} {vb}\n")
        f.write(f");\n")
    if len(decoded.port) > 0:
        f.write(f"port map (\n")
        for port in decoded.port[:-1]:
            if verbose:
                vb = f"--{port[1]}, {port[2]}"
            spaces = " " * (portspacing - len(port[0]))
            f.write(f"{port[0]}{spaces}=> {port[0]}, {vb}\n")
        port = decoded.port[-1]
        if verbose:
            vb = f"--{port[1]}, {port[2]}"
        spaces = " " * (portspacing - len(port[0]))
        f.write(f"{port[0]}{spaces}=> {port[0]} {vb}\n")
        f.write(f");\n")
        f.write(f"\n")
    f.close()

    # Remove duplicates from the library list
    temp = [idx for idx, val in enumerate(lib_list) if val in lib_list[:idx]]

    # Excluding duplicate indices from other list
    clean_lib_list = [ele for idx, ele in enumerate(lib_list) if idx not in temp]

    contents = None
    header = "--Auto generated Test Bench\n"
    footer = ""

    with open(f"{tb_name}.vhdl", "r") as contents:
        save = contents.read()

    # Generate header
    for lib in clean_lib_list:
        if "." not in lib:
            header = header + f"LIBRARY {lib}; \n"
        else:
            header = header + f"USE {lib}; \n"

    header = (
        header
        + f"\nentity {tb_name} is \n\nend {tb_name};\n\narchitecture rtl of {tb_name} is \n \n"
    )

    found_clk = False
    found_rst = False
    clk_list = []
    reset_list = []

    if all_ports_2_toplevel == True:
        # Detect ports and generics
        header = header + "constant clk_period : time := 1 ns;\n" # add in clock period constant
        for generic in generic_list:
            end_of_gen = ""
            if generic[3] != 1:
                if isinstance(generic[3], int):
                    gen_msb = generic[3] - 1
                    end_of_gen = end_of_gen + f"({gen_msb} downto 0)"
            if generic[4] is not None:
                end_of_gen = end_of_gen + f" := {generic[4]}"
            header = header + f"constant {generic[0]} : {generic[2]}{end_of_gen}; \n"

        # Detect CLOCKS and resets
        for port in port_list:
            if 'clk' in port[0] or 'clock' in port[0]: # if the port name include CLK or clock and has length of one add it to a list of signals that could be clocks
                if port[2] == 'std_ulogic' or port[2] == 'std_logic':
                    found_clk = True
                    clk_list.append(port[0] )
            if 'rst' in port[0] or 'reset' in port[0]: # if the port name include CLK or clock and has length of one add it to a list of signals that could be clocks
                if port[2] == 'std_ulogic' or port[2] == 'std_logic':
                    found_rst = True
                    reset_list.append(port[0] )
            end_of_port = ""
            if port[3] != 1:
                if isinstance(port[3], int):
                    port_msb = port[3] - 1
                    end_of_port = end_of_port + f"({port_msb} downto 0)"
            if port[4] is not None:
                end_of_port = end_of_port + f" := {port[4]}"
            else:
                if port[3] != 1:
                    end_of_port = end_of_port + f" := (others => '0')"
                else:
                    end_of_port = end_of_port + f" := '0'"
            header = header + f"signal {port[0]} : {port[2]}{end_of_port}; \n"

    header = header + "\nbegin\n\n"

    # Create clocking process
    if len(clk_list) != 0:
        header = header + "-- Test Bench Clocks\n"
        print("Clocks found: ", clk_list)
    for clk in clk_list:
        header = header + f"""{clk}_process : process
       begin
        {clk} <= '0';
        wait for clk_period/2;  --for 0.5 ns signal is '0'.
        {clk} <= '1';
        wait for clk_period/2;  --for next 0.5 ns signal is '1'. 
end process;"""

    # Create reset process, detect negative reset as active
    if len(reset_list) != 0:
        header = header + "\n\n-- Test Bench Resets\n"
        print("Resets found: ", reset_list)
    for reset in reset_list:
        if '_n' in reset:
            header = header + f"{reset} <= '0', '1' after 25 ns, '0' after 35 ns ; \n"
        else:
            header = header + f"{reset} <= '1', '0' after 25 ns, '1' after 35 ns ; \n"

    header = header + "\n\n"

    with open(f"{tb_name}.vhdl", "w") as contents:
        contents.write(header)

    save_out = (
        save + footer + "\n--Add Test cases here...\nend rtl;\n"
    )  # add the file contents and the footer/end of the file back in.

    with open(f"{tb_name}.vhdl", "a") as contents:
        contents.write(save_out)

    f.close()

if __name__ == '__main__':
    main()
