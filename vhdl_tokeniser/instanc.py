## Parse_VHDL 2023 CFOGE
## instanc.py
## A Script to instantiate a VHDL module from its VHDL file

import argparse
import sys
from token_test import *

# Add argparse for command-line arguments
parser = argparse.ArgumentParser(
    description="VHDL instance generator", formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("file", type=str, help="Input file")
parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
parser.add_argument("-s", "--save", action="store_true", help="Save output to file")
parser.add_argument(
    "--h",
    action="help",
    default=argparse.SUPPRESS,
    help="Show this help message and exit\n"
    "Example usage:\n"
    "python script.py input.vhdl --verbose --save\n",
)

# Check if the correct number of arguments is provided
if len(sys.argv) < 2:
    print("Error: Missing required arguments. Use --h for more information.")
    sys.exit(1)

args = parser.parse_args()

# Parse VHDL file
decoded = parse_vhdl(args.file, False)

# Initialize save_to_file based on command-line argument
save_to_file = False  # args.s

# add arg parser
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

# Print to terminal
print(f"{decoded.data}_i : entity work.{decoded.data}")

# Print generic map if generics are present
if len(decoded.generic) > 0:
    print("generic map (")
    last_gen = decoded.generic[-1]
    for gen in decoded.generic:
        spaces = " " * (genspacing - len(gen[0]))
        vb = f"--{gen[1]} width = {gen[2]}" if True else ""
        if gen != last_gen:
            print(f"   {gen[0]}{spaces}=> {gen[0]}, {vb}")
        else:
            print(f"   {gen[0]}{spaces}=> {gen[0]}  {vb}")
    print(");")

# Print port map if ports are present
if len(decoded.port) > 0:
    print("port map (")
    last_port = decoded.port[-1]
    for port in decoded.port:
        spaces = " " * (portspacing - len(port[0]))
        vb = f"{spaces}--{port[1]} width = {port[2]}" if True else ""   
        if port != last_port:
            print(f"   {port[0]}{spaces}=> {port[0]}, {vb}")
        else:
             print(f"   {port[0]}{spaces}=> {port[0]}  {vb}")
    print(");")
    print()

# Save to file if save_to_file is True
if save_to_file:
    with open("instance_out.vhdl", "a") as f:
        f.write(f"{decoded.data}_i : entity work.{decoded.data}\n")
        if len(decoded.generic) > 0:
            f.write("generic map (\n")
            for gen in decoded.generic[:-1]:
                spaces = " " * (genspacing - len(gen[0]))
                vb = f"{spaces}--{gen[1]} width = {gen[2]}" if True else ""
                
                f.write(f"   {gen[0]}{spaces}=> {gen[0]}, {vb}\n")
            gen = decoded.generic[-1]
            vb = f"{spaces}--{gen[1]} width = {gen[2]}" if True else ""
            spaces = " " * (genspacing - len(gen[0]))
            f.write(f"   {gen[0]}{spaces}=> {gen[0]} {vb}\n")
            f.write(");\n")
        if len(decoded.port) > 0:
            f.write("port map (\n")
            for port in decoded.port[:-1]:
                vb = f"{spaces}--{port[1]} width = {port[2]}" if True else ""
                spaces = " " * (portspacing - len(port[0]))
                f.write(f"   {port[0]}{spaces}=> {port[0]}, {vb}\n")
            port = decoded.port[-1]
            vb = f"--{spaces}{port[1]} width = {port[2]}" if True else ""
            spaces = " " * (portspacing - len(port[0]))
            f.write(f"   {port[0]}{spaces}=> {port[0]} {vb}\n")
            f.write(");\n\n")
