this folder has command line scripts to help work with:
- creating top level vhdl files from scematic netlists
- creating contraints files from vhdl files and linking the pin name/number to the schematic netlist
- checking a top level vhld file to see if all top level ports are connected to pins in the contraints file

  ## new_project.py (This script is great for automating the creation of ports and contraints on a new FPGA design)
  - Creates VHDL top level design from Mentore Graphics NETLIST by matching net names with pin locations (now works with series resistors between the target net and the fpga)
  - Creates .XDC constraints file from VHDL
  - extracts pin location from SCH (eg. J5, AD14..... the pin names that Xilinx uses)
  - Updates the .XDC file with any found pin locations
