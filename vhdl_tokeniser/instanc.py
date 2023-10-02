from token_test import *
import os

decoded = parse_vhdl('fan_control.vhd')


f = open("instance_out.vhdl", "a")
f.write(f"{decoded.data}_i : entity work.{decoded.data} \n")
if len(decoded.generic) > 0:
    f.write(f"generic map (\n")
    for gen in decoded.generic[:-1]:
        f.write(f"{gen[0]} => {gen[0]}, --{gen[1]} width = {gen[2]}\n")
    gen = decoded.generic[-1]
    f.write(f"{gen[0]} => {gen[0]} --{gen[1]} width =  {gen[2]}\n")
    f.write(f");\n")
if len(decoded.port) > 0:
    f.write(f"port map (\n")
    for port in decoded.port[:-1]:
        f.write(f"{port[0]} => {port[0]}, --{port[1]} width =  {port[2]}\n")
    port = decoded.port[-1]
    f.write(f"{port[0]} => {port[0]} --{port[1]} width = {port[2]}\n")
    f.write(f");\n")
    f.write(f"\n")

f.close()