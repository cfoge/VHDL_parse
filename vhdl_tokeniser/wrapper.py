from token_test import *
import os

files_to_wrap = ["tests/test1.vhdl", "tests/test2.vhdl"]
wrapper_name = "wrapper_test"
decoded_list = []
for files in files_to_wrap:
    decoded_list.append(parse_vhdl(files))

#add arg parser
# add function to allign => based on gen/port lenghth

verbose = True
all_generics_2_toplevel = True
all_ports_2_toplevel = True


lib_list = []
generic_list = []
port_list = []
for decoded in decoded_list:


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

    f = open("wraper_out.vhdl", "a")
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
f.close()

#remove duplicates form the Liberary list
temp = [idx for idx, val in enumerate(lib_list) if val in lib_list[:idx]]
 
# excluding duplicate indices from other list
clean_lib_list = [ele for idx, ele in enumerate(lib_list) if idx not in temp]


contents = None
header = "--Auto generated VHDL Wrapper\n"
footer = ""

with open("wraper_out.vhdl",'r') as contents:
      save = contents.read()

# generate header
for lib in clean_lib_list:
    if "." not in lib:
        header = header + f"LIBRARY {lib}; \n"
    else:
        header = header + f"USE {lib}; \n"     

header = header + f"\nentity {wrapper_name} is \n"

if all_ports_2_toplevel == True:
    for port in port_list:
        end_of_port = ""
        if port[3] != 1:
            port_msb = port[3] -1
            end_of_port = end_of_port + f"({port_msb} downto 0)"
        if port[4] != None:
            end_of_port = end_of_port + f" := {port[4]}"
        header = header + f"{port[0]} : {port[1]} {port[2]}{end_of_port}; \n"


header = header + f"end {wrapper_name}; \n\narchitecture rtl of {wrapper_name} is \nbegin \n"

with open("wraper_out.vhdl",'w') as contents:
      contents.write(header)

save_out = save + footer + "\nend rtl;\n" # add the file contents and the footer/end of the file back in.

with open("wraper_out.vhdl",'a') as contents:
      contents.write(save_out)

f.close()