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
- [Insight](#1.4) into the contents of files and the overall structure of the design


## Search<a id='1.1'></a>:
#### Search within VHDL (found in the "vhdl_tokeniser/tools" folder )
##### Search functions: 
- Constant = fconst.py
- Package = fpack.py
- Architecture = farch.py
- Type = ftype.py
#### Search for Type Name
>**Example ftype.py:**
>*Searches all VHDL files in a directory for VHDL FEATURES matching string. arg 1 = search string, arg 2 = -d directory*
>```bash
>python .\ftype.py MY_TYPE -d test
>```
>Returns:
>```
>Searching for type with 'MY_TYPE' in directory: test...
>test\my_package.vhd  : line 10: type MY_TYPE is record    
>Info: 2 files checked.
>```
#### Search for Two strings in the Same Line
>**Example pfind.py:**
>*Searches all VHDL files in a directory for VHDL FEATURES matching string.*
>```bash
>python .\pfind.py clk in -d test
>```
>*Searches for 2 words on the same line, useful for doing things like finding all the VHDL modules with specific input names or libraries. arg 1 = search string A, arg 2 = search string B, arg 3 = -d directory*
>
>Returns:
>```
>test\my_entity.vhd  : line 7: clk : in  std_logic;
>Info: 2 files checked.
>```
>---

## Show<a id='1.2'></a>:
#### Compare File Names in One Directroy vs. Another 
>**Example sdiffile.py:** 
>```bash
>python .\sdiffile.py test/folderA test/folderB 
>```
>*Compares two directorys and returns the files found in one but not the other, and vise versa.*
>
>Returns:
>```
>Files in test/folderA but not in test/folderB :
>test1.vhdl
>
>Files in test/folderB but not in test/folderA :
>test5.vhdl
>```
#### Compare File Contents in One Directroy vs. Another
>**Example sdifcont.py:** 
>```bash
>python .\sdifcont.py test/folderA test/folderB -e vhdl
>```
>*Compares contents of two files with the same name in two different directorys and returns the files that are not >identical.*
>
>Returns:
>```
>test/folderA\test2.vhdl and test/folderB\test2.vhdl have different contents
>```

>**Example sdir.py:** 
>```bash
>python sdir.py  . -f package 
>```
>*Searches directory for VHDL files with keyword 'package' in filename, shows in file tree with files matching your >search tearm highlighted in red.*
>
>Returns:
>```
>Directory tree structure for '.':
>⤷ test
>    - my_entity.vhd
>      - my_package.vhd
>⤷ __pycache__
>```
---
## Automate<a id='1.3'></a>:
#### Create Bus and Assignments from signals:
>**bundle_sig.py:**
>```bash
>python bundle_sig.py tests\test2.vhdl new_bus a AB Result b
>```
>*Creates a signal definition as well as the assignements needted to explicitly asssign a group of signals to a new bus. Args are 1. vhdl file with the signals to be bundled, 2. the name of the new signal, 3. any signals from the VHDL file to be bundled*
>
>Returns:
>```
>signal new_bus : std_logic_vector(24 downto 0);
>
>new_bus(7 downto 0) <= a;
>new_bus(15 downto 8) <= ab;
>new_bus(16)           <= result;
>new_bus(24 downto 17) <= b;
>```
#### Make Constraints File from Top-Level VHDL
>**make_xdc.py:** (in the PINS Folder)
>```bash
>python make_xdc.py gen_file test\proj1.vhd
>```
>*Creates an .xdc constraints file from a top-level VHDL file named "gen_file"*
>
>Returns:
>```
>Running with default settings (Xilinx .xdc)
>gen_file.xdc created from test\proj1.vhd  
>```
#### Check XDC vs. Top-level VHDL
>**check_xdc.py:** (in the PINS Folder)
>```bash
>python check_xdc.py test\proj2.xdc test\proj1.vhd 
>```
>*Compares a .xdc constraints file with the ports of a top-level VHDL file and reports the differences.*
>
>Returns:
>```
>Comparing Ports in .\proj2.xdc and .\proj1.vhd
>In XDC but NOT in Vhd:
>
>In Vhd but NOT in XDC:
>in_vcxo_0_ctrl
>```
#### Make Constraints and Top-Level VHDL from Schematic Netlist
> WIP
#### Find Unused Signals in VHDL File
>**find_unused_sig.py:**
>```bash
>python find_unused_sig.py .\tests\unused_sig.vhdl
>```
>*Checks for signals declared in a VHDL file, that are not ever used. Good for cleaning up files.*
>
>Returns:
>```
>Searching for signals declared but never used in .\tests\unused_sig.vhdl...
>counter_2s found in file 1 time(s). line 21
>unused_delay found in file 1 time(s). line 23
>```
#### Create Testbench from VHDL File
>**testbench.py:**
>```bash
>python testbench.py tests/test3.vhdl
>```
>*Generates a VHDL test bench for a VHDL file. Detects clocks and resets, extracts signals form UUT and sets them to '0'*
>
>Returns:
>```
>Generating test bench for tests/test3.vhdl...
>Clocks found:  ['clk']
>Resets found:  ['rst_n']
>```
#### Create Wrapper for Multiple VHDL Files
>**wrapper.py:**
>```bash
>python wrapper.py tests\test1.vhdl tests\test2.vhdl -sig
>```
>*Generates a VHDL file consisting of instances of any VHDL files passed to it. "-sig" will create signals for each VHDL modules I/O signals,check the script help for renaming and saving to disk*
>
>Returns:
>```
>--Auto generated VHDL Wrapper  
>LIBRARY ieee;
>USE ieee.std_logic_1164.all;   
>
>entity wrapper is
>port();
>end wrapper;
>
>architecture rtl of wrapper is 
>
>signal x1 : std_logic;   
>signal x2 : std_logic;   
>..... (Other signals omitted here to save space in this readme)
>begin
>
>full_adder_structural_vhdl_i : entity work.full_adder_structural_vhdl
>port map (
>x1      => x1,
>x2      => x2,
>cin     => cin,
>s       => s,
>cout    => cout
>);
>
>comparator_i : entity work.comparator
>port map (
>clock     => clock,
>a         => a,
>b         => b,
>iab       => iab,
>output    => output
>);
>end rtl;
>```
## Insight<a id='1.4'></a>:
#### Get Summery of VHDL file Contents
>**get_info.py:**
>```bash
>python get_info.py tests\test8.vhdl
>```
>*Sumerises the contents of a VHDL file with colour coding. Some VHDL features are currently not shown.*
>
>Returns:
>```
>Getting Info For .\tests\test8.vhdl
>Name: adder_tree  -  Arch: str
>   Generics:
>        -->['width', '', 'positive', 'null', 8]
>        -->['topwidth', '', 'positive', 'null', 4]
>   Port:
>        -->['rst', 'in', 'std_logic', 1, None]
>        -->['clk', 'in', 'std_logic', 1, None]
>        -->['input', 'in', 'std_logic_vector', 'topwidth * width - 1 downto 0', None]
>        -->['output', 'out', 'std_logic_vector', 'width - 1 downto 0', None]
>        -->['valid_in', 'in', 'std_logic', 1, None]
>        -->['valid_out', 'out', 'std_logic', 1, None]
>   Components:
>   Entities:
>   Process:
>   Constants:
>        -->['treeheight', '', 'integer', 'null', 'integerceillog2realtopwidth']
>   Attributes:
>   Signals:
>        -->['valid', '', 'std_logic', 1, None]
>        -->['register_input', '', 'std_logic_vector', 'width - 1 downto 0', None]
>        -->['register_input', '', 'std_logic_vector', 'topwidth / 2 * width - 1 downto 0', None]
>        -->['register_output', '', 'std_logic_vector', 'topwidth / 2 * width - 1 downto 0', None]
>        -->['base_case', '', 'std_logic_vector', 'width * 2 - 1 downto 0', None]
>        -->['delay_chain', '', 'std_logic_vector', 'treeheight + 1 * width - 1 downto 0', None]
>        -->['valid2', '', 'std_logic', 1, None]
>```


#### I hope these scripts make your FPGA and VHDL work a bit smoother! I use them all the time and they have saved me countless hrs already. 🎉

