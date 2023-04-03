# VHLD_parse
A collection of Python scripts to make working with VHDL easier

## Purpose: 
These scripts are designed to run in the command line without needing an libaries other then those included with python 3

## Scripts:
### what_in.py:
Lists a VHDL files: entitys, constants, atributes, signals and processes in a simple colour coded list
> This script needs one or two inputs, the first is a vhdl file, the second (optional) a paramiter
> 2nd arg "f" show all, "a" show attributes, "v" show variables, "c" show constants, "p" show processes, "s" show signals
>
> example: what_in.py input.vhd a
