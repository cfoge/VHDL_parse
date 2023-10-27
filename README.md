# VHDL_parse 🚀
Welcome to VHDL_parse, a collection of Python tools crafted to simplify your VHDL workflow without the fuss of heavyweight IDEs like Vivado or Quartus. Dive into efficient VHDL development with these lightweight scripts!
---

## Purpose
Designed to seamlessly run in the command line, VHDL_parse empowers you to navigate and manipulate VHDL projects effortlessly. No additional libraries required—just the magic of Python3.

## Scripts
### parse_vhdl.py 🕵️‍♂️
Revamped from scratch, parse_vhdl.py now utilizes a sophisticated tokenizer, enhancing compatibility with differently formatted files. This script parses VHDL, creating an object containing ports, signals, components, and more.

##### Current features:
- Display VHDL module hierarchies
- Trace signal paths across multiple files
- Auto-generate entity and module instantiations
Future potential:
- Automated component declaration
- Test bench creation automation
- Signal tracing/search through multiple files

###what_in.py 📜
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

