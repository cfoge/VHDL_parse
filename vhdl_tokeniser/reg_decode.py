import os
import re
import argparse
from token_test import *


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def convert_vhdl_reg_to_code(input_file, vhdl_obj, cpp_out=False):
    cpp_header = []
    if cpp_out:
        print("// Auto Generated C/C++ header file for register file")
    else:
        print("-- Auto Generated VHDL header file for register file")
    
    lower = input_file.lower()
    lines = lower.split(";")
    for line in lines:
        if "regs" in line and "<=" in line:
            packed = []
            from_to = line.split("<=")
            if "&" in from_to[1]:
                packed_reg = from_to[1].split("&")
                for reg in packed_reg:
                    if '"' in reg or "'" in reg:
                        if "x" in reg:
                            zeros = find_between(reg, '"', '"')
                            constant = False
                            for dig in zeros:
                                if dig != "0":
                                    constant = True
                            if not constant:
                                packed.append(int(len(zeros)) * 4)
                            else:
                                packed.append(zeros)
                        else:
                            zeros = find_between(reg, '"', '"')
                            packed.append(int(len(zeros)))
                    else:
                        if "(" in reg and ")" in reg:
                            reg = find_between(reg, "(", ")")
                        packed.append(reg.replace(";", ""))
            else:
                if "(" in from_to[1] and ")" in from_to[1]:
                    from_to[1] = find_between(from_to[1], "(", ")")
                packed.append(from_to[1].strip())
            
            match = re.search(r'x"([^"]*)"', from_to[0])
            if match:
                regnum = match.group(1).strip()
                str_out = ""
                start_bit = 0

                for pack in reversed(packed):  # go from end to beginning
                    if isinstance(pack, int):
                        start_bit += pack
                    else:
                        found_sig = False
                        for signal in vhdl_obj.signal:
                            if signal[0] == pack.strip():
                                found_sig = True
                                str_out = f"{pack.strip()}({int(signal[3])-1+start_bit}:{start_bit})  " + str_out
                                cpp_shift = start_bit
                                start_bit += signal[3]
                                if cpp_out:
                                    print(f"#define {pack.strip()}     0x{regnum}")
                                    print(f"#define {pack.strip()}_shift     {cpp_shift}")
                                    print(f"#define {pack.strip()}_size      {signal[2]}")

                        if not found_sig:  # if the assignment wasn't a signal, check if it was a port
                            for signal in vhdl_obj.port:
                                if signal[0] == pack.strip():
                                    found_sig = True
                                    try:
                                        str_out = f"{pack.strip()}({int(signal[3])-1+start_bit}:{start_bit})  " + str_out
                                        cpp_shift = start_bit
                                        start_bit += signal[3]
                                        if cpp_out:
                                            print(f"#define {pack.strip()}     0x{regnum}")
                                            print(f"#define {pack.strip()}_shift     {cpp_shift}")
                                            print(f"#define {pack.strip()}_size      {signal[3]}")
                                    except:
                                        print("decode_error")

                if not cpp_out:
                    print(f"-- 0x{regnum}   R    {str_out}")
    
    if cpp_out:
        print("// Macros for extracting and setting values based on the given specifications")
        print("#define EXTRACT_BITS(value, shift, size) (((value) >> (shift)) & ((1 << (size)) - 1))")
        print("#define SET_BITS(value, shift, size, data) ((value) = ((value) & ~(((1 << (size)) - 1) << (shift))) | (((data) & ((1 << (size)) - 1)) << (shift)))")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert VHDL register definitions to code.")
    parser.add_argument("input_file", type=str, help="Input VHDL register file.")
    parser.add_argument("-c", "--cpp_out", action="store_true", help="Output as C/C++ header instead of VHDL.")
    args = parser.parse_args()

    reg_file = read_vhdl_file(args.input_file)
    parsed_vhdl_obj = parse_vhdl(args.input_file)  # Replace this with actual loading or definition of parsed_vhdl_obj


    # print(reg_file)

    if parsed_vhdl_obj is None:
        print("Error: parsed_vhdl_obj is not defined.")
        exit(1)

    convert_vhdl_reg_to_code(reg_file, parsed_vhdl_obj, args.cpp_out)
