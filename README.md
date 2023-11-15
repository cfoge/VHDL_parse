# VHDL_parse 🚀
Welcome to VHDL_parse, a collection of Python tools crafted to simplify your VHDL workflow without the fuss of heavyweight IDEs like Vivado or Quartus. Dive into efficient VHDL development with these lightweight scripts!
---
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=LSMYWSM7M7EEA)
Open to donations and contributors with VHDL/Python experience. 😀 

## Purpose
Designed to seamlessly run in the command line, VHDL_parse empowers you to navigate and manipulate VHDL projects effortlessly. No additional libraries required—just the magic of Python3.

## Scripts
### parse_vhdl.py (in the "vhdl_tokeniser" folder) 🕵️‍♂️
Revamped from scratch, parse_vhdl.py now utilizes a tokenizer and enhancing compatibility with differently formatted files. This script parses VHDL, creating a python object containing ports, signals, components, and more. Then this python object can be used to simplify VHDL development.

#### Working Python Comand Line Scripts
- **instanc.py** = creates a template instantiation from a VHDL file in the terminal or as a .txt file
- **component.py **= creates a template component decleration from a VHDL file in the terminal or as a .txt file
- **wrapper.py** = create a wrapper that declares an entity, instantiates the VHDL files passed to it annd optionally creates signals with matching port names connected to each instance.

##### Current features:
- Display VHDL module hierarchies from directory
- Auto-generate entity and module instantiations
- Auto generate VHDL wrappers for multiple entitys
##### Future potential:
- Test bench creation automation
- Signal tracing/search through multiple files
- Diff two vhdl files by port,generics,contants ect.. rather then line by line like a regular diff would

### what_in.py 📜
List VHDL entities, constants, attributes, signals, and processes:

| Arg 1        | Arg 2           |
| ------------- |:-------------:| 
| vhdl file     | param (optional)|

The second (optional) is a parameter to filter the results:
"f" shows all
"a" shows attributes
"v" shows variables
"c" shows constants
"p" shows processes
"s" shows signals

Example: 
```bash
what_in.py input.vhd a
```


### make_xdc.py 🧩
Transform the ports on your top-level VHDL file into a constraints file in either Xilinx or Quartus format with make_xdc.py. Just two inputs needed:

| Arg 1        | Arg 2           | Arg 3 (optional)|
| ------------- |:-------------:| ------------- |
| XDC output file name    | Input Top level.vhd file| q (quartus mode)|

Example: 
```bash
check_xdc.py output input.vhd 
```
(optional 3rd argument "q" generates Quartus output)


#### Explore the efficiency, simplicity, and joy of VHDL development with VHDL_parse. Your VHDL projects just got a whole lot more enjoyable! 🎉

