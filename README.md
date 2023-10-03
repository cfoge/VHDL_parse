# VHLD_parse
A collection of Python scripts to make working with VHDL easier

## Purpose: 
These scripts are designed to run in the command line without needing any libraries other then those included with Python3

## Scripts:
### parse_vhdl.py:
Rewritern from scratch to use a tokenizer, work in progress. Tokeniser makes it much better at files with different formatting.
Parse VHDL is a script that parses VHDL and creates an object with all the VHDL files ports, signals, components... ect.

At the moment it can do things like, show VHDL module hierarchies, trace signal paths through multiple files (even as signal name changes), and auto-generate entity and module instantiations. 

Designed to eventually be used to allow automated component declaration, automated test bench creation, signal tracing/search through multiple files ect...

### what_in.py:
Lists VHDL files: entities, constants, attributes, signals, and processes in a simple color-coded list
> This script needs one or two inputs, the first is a vhdl file, the second (optional) a parameter
> 2nd arg "f" shows all, "a" shows attributes, "v" shows variables, "c" shows constants, "p" shows processes, "s" shows signals
>
> example: what_in.py input.vhd a

### make_xdc.py:
Takes the ports on your top-level VHDL file and turns them into a constraints file in either Xilinx or Quartus format.
> This script needs two inputs,XDC output file name and the input Top level.vhd file.
> 
> example: check_xdc.py output input.vhd (opt 3rd argument "q" generates Quartus output
