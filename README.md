# VHDL_parse 🚀

#### VHDL_parse is for Automating VHDL creation, creating top-level and constraint files from schematics, searching large projects, and visualising module hierarchy and signal flow.
---
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=LSMYWSM7M7EEA)
Open to donations and contributors with VHDL or Python experience. 😀 

> [!IMPORTANT]
> Designed to run in the command line, VHDL_parse lets you explore, navigate and manipulate VHDL files effortlessly. No additional libraries are required, just the magic of Python3. If you want to run these scripts from anywhere check [here](Global_setup.md).

## Functions
- [Search](#1.1) for somthing inside your VHDL files.
- [Show](#1.2) differences in vhdl files and folder structure.
- [Automate](#1.3) the creation and checking of VHDL files.  



## Tools 🕵️‍♂️
found in the "vhdl_tokeniser/tools" folder 
### Search<a id='1.1'></a>:
*Searches all VHDL files in a directory for VHDL FEATURES matching string. Eg. fconst.py searches for constants, ftype.py searches for types ect...*
arg 1 = search string, arg 2 = -d directory

>**Example farch.py:** 
>```bash
>python .\farch.py Behavioral -d test
>```
>Returns:
>```
>Searching for architecture with 'Behavioral' in directory: test...
>test\my_entity.vhd  : line 14: architecture Behavioral of my_entity is
>Info: 2 files checked.
>```

>**Example ftype.py:** 
>```bash
>python .\ftype.py MY_TYPE -d test
>```
>Returns:
>```
>Searching for type with 'MY_TYPE' in directory: test...
>test\my_package.vhd  : line 10: type MY_TYPE is record    
>Info: 2 files checked.
>```

>**Example pfind.py:** 
>```bash
>python .\pfind.py clk in -d test
>```
>*Searches for 2 words on the same line, useful for doing things like finding all the VHDL modules with specific input names or >libraries.*
>Returns:
>```
>test\my_entity.vhd  : line 7: clk : in  std_logic;
>Info: 2 files checked.
>```
>---

### Show<a id='1.2'></a>:
>**Example sdiffile.py:** 
>```bash
>python .\sdiffile.py test/folderA test/folderB 
>```
>*Compares two directorys and returns the files found in one but not the other, and vise versa.*
>Returns:
>```
>Files in test/folderA but not in test/folderB :
>test1.vhdl
>
>Files in test/folderB but not in test/folderA :
>test5.vhdl
>```

>**Example sdifcont.py:** 
>```bash
>python .\sdifcont.py test/folderA test/folderB -e vhdl
>```
>*Compares contents of two files with the same name in two different directorys and returns the files that are not >identical.* 
>Returns:
>```
>test/folderA\test2.vhdl and test/folderB\test2.vhdl have different contents
>```

>**Example sdir.py:** 
>```bash
>python sdir.py  . -f package 
>```
>*Searches directory for VHDL files with keyword 'package' in filename, shows in file tree with files matching your >search tearm highlighted in red.*
>Returns:
>```
>Directory tree structure for '.':
>⤷ test
>    - my_entity.vhd
>      - my_package.vhd
>⤷ __pycache__
>```
---
### Automate<a id='1.3'></a>:
>**check_xdc.py:** (in the PINS Folder)
>```bash
>python check_xdc.py test\proj2.xdc test\proj1.vhd 
>```
>*Compares a .xdc constraints file with the ports of a top-level VHDL file and reports the differences*
>Returns:
>```
>Comparing Ports in .\proj2.xdc and .\proj1.vhd
>In XDC but NOT in Vhd:
>
>In Vhd but NOT in XDC:
>in_vcxo_0_ctrl
>```

#### Working Python Comand Line Scripts
- **instanc.py** = creates a template instantiation from a VHDL file in the terminal or as a .txt file
- **component.py** = creates a template component declaration from a VHDL file in the terminal or as a .txt file
- **wrapper.py** = create a wrapper that declares an entity, instantiates the VHDL files passed to it and optionally creates signals with matching port names connected to each instance.

##### Current features:
- Display VHDL module hierarchies from a directory
- Auto-generate entity and module instantiations
- Auto-generate VHDL wrappers for multiple entities
##### Future potential:
- Test bench creation automation
- Signal tracing/search through multiple files
- Diff two vhdl files by port,generics,contants ect.. rather than line by line like a regular diff would

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


#### I hope these scripts make your FPGA and VHDL work a bit smoother! I use them all the time and they have saved me countless hrs already. 🎉

