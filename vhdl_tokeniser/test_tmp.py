
import os
from token_test import *
from reg_decode import *

import time

start = time.time()
file = "C:/BMD_builds/ava_final/atemava1/src/cpu_regs.vhd"
reg_file = read_vhdl_file(file)
target_vhdl = parse_vhdl(file)

convert_vhdl_reg_to_comment(reg_file, target_vhdl)

end = time.time()
print(end - start)
print("")