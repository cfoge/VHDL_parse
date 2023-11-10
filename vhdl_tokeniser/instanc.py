from token_test import *
import os

decoded = parse_vhdl('c:/BMD_builds/tvs3d_issue_multi_build/atemtvs3dcpu/src/atemtvs3dcpu.vhd', True)

#add arg parser
# add function to allign => based on gen/port lenghth

verbose = True
genlen = 0
for gen in decoded.generic:
    x = len(gen[0])
    if x > genlen:
        genlen = x
portlen = 0
for port in decoded.port:
    x = len(port[0])
    if x > portlen:
        portlen = x

genspacing = genlen + 4
portspacing = portlen + 4

f = open("instance_out.vhdl", "a")
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

