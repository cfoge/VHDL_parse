# a test program designed to check how long it takes to run functions


import os
from token_test import *
# from trace_sign import *
# from reg_decode import *

import time

start = time.time()


# primitives = get_filenames_without_extension("C:/Xilinx/2022_2_new/Vivado/2022.2/data/vhdl/src/unisims/primitive")
# print (primitives)
# file = "C:/BMD_builds/ava_final/atemava1/src/cpu_regs.vhd"
# file = "c:/Users/robertjo/Downloads/ems_latest/src/digital_side/control/digital_reg_file.vhd"
file = "tests/lifo.vhdl"
# reg_file = read_vhdl_file(file)
target_vhdl = parse_vhdl(file)

# convert_vhdl_reg_to_code(reg_file, target_vhdl,False)

end = time.time()
print(end - start)
print("")