import sys
import re
import os
import argparse

def parse_vhdl_arg_parse():
  # Create the parser
  parser = argparse.ArgumentParser()
  # Add an argument
  parser.add_argument('-i', '--input', type=str, required=True)
  # Parse the argument
  args = parser.parse_args()
  return args


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def find_type(input_line):
    type_found = "null"
    if "std_logic_vector" in input_line:
        type_found = "std_logic_vector"
    elif "std_logic" in input_line:
        type_found = "std_logic"
    elif "bit_vector" in input_line:
        type_found = "bit_vector"
    elif "bit" in input_line:
        type_found = "bit"
    elif "boolean" in input_line:
        type_found = "boolean"
    elif "interger" in input_line:
        type_found = "interger"
    elif "unsigned" in input_line:
        type_found = "unsigned"
    elif "signed" in input_line:
        type_found = "signed"
    # add more types
    if "std_ulogic_vector" in input_line:
        type_found = "std_ulogic_vector"
    elif "std_ulogic" in input_line:
        type_found = "std_ulogic"
    return type_found


def find_width(input_line, type_in):
    size_found = "null"
    if type_in == "std_logic_vector":
        size_found = extract_bit_len(input_line)
    elif type_in == "std_logic":
        size_found = 1
    elif "bit_vector" in input_line:
        type_found = "bit_vector"
    elif "bit" in input_line:
        size_found = 1
        # add for more types
    elif type_in == "std_ulogic_vector":
        size_found = extract_bit_len(input_line)
    elif type_in == "std_ulogic":
        size_found = 1
    return size_found


def extract_bit_len(str_in):
    port_width = re.findall(r"\d+", str_in)
    if len(port_width) < 2:
        bit_len = 1
    else:
        bit_len = (int(port_width[0]) + 1) - int(port_width[1])
    return bit_len


class instanc(object):
    def __init__(self, mod, name, line_num):
        self.mod = mod  # is module name
        self.name = name  # is module name
        self.line_num = line_num
        self.generic = []
        self.port = []


class vhdl_obj(object):
    def __init__(self):
        self.type = []
        self.data = []
        self.line_num = []
        self.lib = []
        self.work = []
        self.generic = []
        self.port = []
        self.children_name = []
        self.children = []
        self.component = []
        self.attribute = []
        self.constant = []
        self.process = []
        self.signal = []
        self.search = []
        self.paths = []
        self.assign = []

    def who_is(self):
        print(self.data[0])
        print(self.type)
        print(color.UNDERLINE + "Generic" + color.END)
        for i in range(len(self.generic)):
            print("   --" + str(self.generic[i][0]))
        print(color.UNDERLINE + "Port" + color.END)
        for i in range(len(self.port)):
            print("   --" + str(self.port[i]))
        print("  Children")
        for i in range(len(self.children_name)):
            print(
                "   --"
                + str(self.children_name[i].name)
                + "  --> "
                + str(self.children_name[i].mod)
            )
        print("  Component")
        for i in range(len(self.component)):
            print("   --" + str(self.component[i].mod))
        print(color.UNDERLINE + "Attribute" + color.END)
        for i in range(len(self.attribute)):
            print("   --" + str(self.attribute[i][0]))
        print(color.UNDERLINE + "Constant" + color.END)
        for i in range(len(self.constant)):
            print("   --" + str(self.constant[i][0]))
        print(color.UNDERLINE + "Process" + color.END)
        for i in range(len(self.process)):
            print("   --" + str(self.process[i][0]))
        print(color.UNDERLINE + "Signal" + color.END)
        for i in range(len(self.signal)):
            print("   --" + str(self.signal[i]))
            # add the rest of the stuff


def parse_vhdl(file_name):
    # with open(file_name) as f:
    #     file_in = f.readlines()

    with open(file_name) as f:
        vhd = f.readlines()
        

    generic_found = False
    port_found = False
    port_final_line = False
    entity_found = False
    entity_port_found = False
    component_found = False
    component_port_found = False
    entity_counter = -1
    component_count = -1
    entity_vhdl = []
    vhdl_line = -1
    vhdl_line_str = ""

    # Initialize the VHDL object
    entity_vhdl = vhdl_obj()
    for i in vhd:
        vhdl_line = vhdl_line + 1  # increment line number
        # if vhdl_line == 556: # use to debug specific lines of the vhdl file
        #     print("BREAK")
        vhdl_line_str = ""  # "#" + str(vhdl_line)
        # Strip leading and trailing whitespace from the line
        i = i.strip()
        i = i.lower()
        # remove coments from end of lines
        if (not i.startswith("--")  and "--" in i):
            i = i.split("--", 1)[0]
        # Skip commented lines
        if i.startswith("--"):
            continue
        elif (("library" in i) & (";" in i)) or (
            (("use " in i) or ("USE " in i)) & ((";" in i) or ("," in i))
        ):
            entity_vhdl.lib.append(i)  # basic, not finished
        elif ("entity" in i) & ("is" in i):
            tmp1 = re.findall("entity (.*) is", i)
            if len(tmp1) > 0:
                entity_vhdl.data.append(tmp1[0].strip())
                entity_vhdl.type.append("file")
        elif ("entity" in i) & (":" in i) & (entity_found == False):
            entity_found = True
            tmp1 = i.strip()
            if (":" in tmp1) & ("entity" in tmp1) & ("work." in tmp1):
                tmp2 = tmp1.split("work.", 1)
            elif (":" in tmp1) & ("entity" in tmp1):
                tmp2 = tmp1.split("entity", 1)
            else:
                tmp2 = tmp1.split(":", 1)
            if " " in tmp2[1]:
                tmp2[1] = tmp2[1].split(" ", 1)[0]
            if "--" in tmp2[1]:
                tmp2[1] = tmp2[1].split("--", 1)[0]
            tmp2[0] = tmp2[0].split(":", 1)[0]

            entity_vhdl.children_name.append(
                instanc(tmp2[1].strip(), tmp2[0].strip(), vhdl_line_str)
            )
            entity_counter = entity_counter + 1

        elif (
            (":" in i)
            & (";" not in i)
            & ("," not in i)
            & (")" not in i)
            & ("process" not in i)
            & (entity_found == False)
            & (port_found == False)
            & (component_found == False)
            & (generic_found == False)
        ):
            entity_found = True
            tmp1 = i.strip()
            if (":" in tmp1) & ("entity" in tmp1) & ("work." in tmp1):
                tmp2 = tmp1.split("work.", 1)
            elif (":" in tmp1) & ("entity" in tmp1):
                tmp2 = tmp1.split("entity", 1)
            else:
                tmp2 = tmp1.split(":", 1)
            if " " in tmp2[1]:
                tmp2[1] = tmp2[1].split(" ", 1)[0]
            if "--" in tmp2[1]:
                tmp2[1] = tmp2[1].split("--", 1)[0]
            tmp2[0] = tmp2[0].split(":", 1)[0]

            entity_vhdl.children_name.append(
                instanc(tmp2[1].strip(), tmp2[0].strip(), vhdl_line_str)
            )
            entity_counter = entity_counter + 1
            if "port map" in i:
                entity_port_found = True

        elif (entity_found == True) & ("port map" in i):
            entity_port_found = True
        elif (entity_found == True) & (entity_port_found == True) & ("=>" in i):
            tmp1 = i.strip()
            tmp2 = tmp1.split("=>")
            if "," in tmp2[1]:
                tmp2[1] = tmp2[1].split(",")
                tmp2[1] = tmp2[1][0]
            entity_vhdl.children_name[entity_counter].port.append(
                [tmp2[0].strip(), tmp2[1].strip()]
            )

        elif (entity_found == True) & (entity_port_found == True) & (");" in i):
            entity_port_found = False
            entity_found = False

        elif ("component" in i) & ("is" in i) or ("component" in i) & (
            not ("is" in i)
        ) & (not (";" in i)):
            tmp1 = re.findall("component (.*) is", i)
            if len(tmp1) == 0:
                tmp1 = i.split("component")
                tmp1 = tmp1[1].strip()
            # entity_vhdl[0].component.append(tmp1)
            component_found = True
            entity_vhdl.component.append(instanc(tmp1, "", vhdl_line_str))
            component_count = component_count + 1
        elif (component_found == True) & (("port " in i) or ("port(" in i)):
            component_port_found = True
        elif (component_port_found == True) & ("end component" in i) & (";" in i):
            component_port_found = False
            component_found = False

        elif (
            ("component" not in i)
            & ("map" not in i)
            & (component_port_found == True)
            & (component_found == True)
        ):
            if ":" in i:
                tmp1 = i.strip()
                tmp2 = tmp1.split(":")  # port name
                tmp2[0] = tmp2[0].strip()
                tmp2[1] = tmp2[1].strip()
                tmp3 = tmp2[1].split(" ")
                port_type = find_type(tmp2[1])
                port_width = find_width(tmp2[1], port_type)
                if "," in tmp2[0]:
                    tmp4 = tmp2[0].split(",")
                    for port in tmp4:
                        entity_vhdl.component[component_count].port.append(
                            [port.strip(), tmp3[0].strip(), port_type, port_width]
                        )
                else:
                    entity_vhdl.component[component_count].port.append(
                        [tmp2[0].strip(), tmp3[0].strip(), port_type, port_width]
                    )
                    # tmp1 = i.strip()
                    # tmp2 =  tmp1.split(":")    #port name
                    # tmp2[0] = tmp2[0].strip()
                    # tmp2[1] = tmp2[1].strip()
                    # tmp3 = tmp2[1].split(" ")
                    # entity_vhdl.component[component_count].port.append([tmp2[0].strip(), tmp3[0].strip(),  tmp3[len(tmp3)-1].strip()])

        elif ("process" in i) & ("(" in i) & (")" in i):
            if ":" in i:
                tmp1 = i.strip()
                tmp2 = tmp1.split(":")
                tmp3 = tmp2[1].strip()
                tmp3 = tmp3[7:].split(")")
                tmp4 = tmp3[0].strip()
                tmp4 = tmp4[1:]
                if "," in tmp1:
                    tmp4 = tmp4.split(",")

                entity_vhdl.process.append([tmp2[0], tmp4])

            else:
                tmp1 = i.strip()
                tmp1 = tmp1[7:]
                tmp1 = tmp1.strip()
                tmp1 = tmp1[1:-1]
                if "," in tmp1:
                    tmp2 = tmp1.split(",")
                else:
                    tmp2 = tmp1
                entity_vhdl.process.append(["no name", tmp2])
                
        elif ("process" in i) & (":" in i) & ("(" not in i):
            tmp1 = i.strip()
            tmp2 = tmp1.split(":")
            tmp3 = tmp2[1].strip()
            tmp3 = tmp3[7:].split(")")
            tmp4 = tmp3[0].strip()
            tmp4 = tmp4[1:]
            if "," in tmp1:
                tmp4 = tmp4.split(",")

            entity_vhdl.process.append([tmp2[0], tmp4])

        elif ("constant" in i) & (":=" in i) & (";" in i):
            tmp1 = i.strip()
            tmp1 = tmp1[8:-1]
            tmp2 = tmp1.split(":")
            tmp2[0] = tmp2[0].strip()
            tmp2[1] = tmp2[1].strip()
            tmp3 = tmp2[2].split(";")
            tmp2[2] = tmp3[0][1:].strip()
            entity_vhdl.constant.append([tmp2, vhdl_line_str])
        elif ("Variable" in i) & (":" in i) & (";" in i):
            tmp1 = i.strip()
            tmp1 = tmp1[8:-1]
            entity_vhdl.variable.append([tmp1, vhdl_line_str])
        elif ("attribute" in i) & (":" in i) & (";" in i):
            tmp1 = i.strip()
            tmp1 = tmp1[9:-1]
            if ":" in tmp1:
                tmp2 = tmp1.split(":")
            else:
                tmp2 = tmp1.split("is")
            tmp3 = tmp2[1].split("is")
            if "of" in tmp2[0]:
                tmp4 = tmp2[0].split("of")
                tmp2[0] = tmp4[1].strip()
            if len(tmp3) > 1:
                entity_vhdl.attribute.append(
                    [tmp2[0].strip(), tmp3[0].strip(), tmp3[1].strip(), vhdl_line_str]
                )
            else:
                entity_vhdl.attribute.append(
                    [tmp2[0].strip(), tmp3[0].strip(), vhdl_line_str]
                )
        elif (("signal" in i) & (":" in i) & (";" in i)) & ("attribute" not in i):
            port_found = False
            tmp1 = i.strip()
            tmp1 = tmp1[6:-1]
            tmp2 = tmp1.split(":")
            tmp2[0] = tmp2[0].strip()
            tmp2[1] = tmp2[1].strip()
            tmp3 = tmp2[1].split(" ")
            port_type = find_type(tmp2[1])
            port_width = find_width(tmp2[1], port_type)
            if "," in tmp2[0]:
                tmp4 = tmp2[0].split(",")
                for signal in tmp4:
                    entity_vhdl.signal.append([signal.strip(), port_type, port_width])
            else:
                entity_vhdl.signal.append([tmp2[0].strip(), port_type, port_width])
            # if(len(tmp2)>2):
            #     tmp2[2] = tmp2[2][1:].strip()
            # entity_vhdl.signal.append(tmp2)

        elif ("generic" in i) & ("(" in i) & ("map" not in i):
            if (")" in i) & (";" in i):
                tmp1 = i.strip()
                tmp2 = tmp1.split("(")
                tmp3 = tmp2[1].split(":")
                tmp3[0] = tmp3[0].strip()
                tmp3[1] = tmp3[1].strip()
                tmp3[2] = tmp3[2][1:].strip()
                tmp_fix = tmp3[2].split(")")
                tmp3[2] = tmp_fix[0]
                entity_vhdl.generic.append([tmp3, vhdl_line_str])

            else:
                generic_found = True
        elif (generic_found == True) & (");" in i) & ("port" not in i):
            generic_found = False
        elif (generic_found == True) & (");" in i) & ("port" in i):
            generic_found = False
            port_found = True

        elif (
            ("generic" not in i)
            & ("map" not in i)
            & (generic_found == True)
            # & (";" in i)
        ):
            tmp1 = i.strip()
            tmp2 = tmp1.split(":")
            tmp2[0] = tmp2[0].strip()
            if len(tmp2) > 1:
                tmp2[1] = tmp2[1].strip()
            if len(tmp2) > 2:
                tmp2[2] = tmp2[2][1:].strip()

            entity_vhdl.generic.append([tmp2, vhdl_line_str])
        elif (("port " in i) & (("(" in i))) or (("port(" in i)) and ("map" not in i) and ("=" not in i):
            port_found = True
        elif (port_found == True) & (");" in i)& (":"not in i) & (not ("(" in i)):
            port_found = False

        elif ("port " not in i) & ("map " not in i) & (port_found == True) & (":" in i):
            tmp1 = i.strip()
            tmp2 = tmp1.split(":")  # port name
            tmp2[0] = tmp2[0].strip()
            tmp2[1] = tmp2[1].strip()
            tmp3 = tmp2[1].split(" ")
            port_type = find_type(tmp2[1])
            port_width = find_width(tmp2[1], port_type)
            if "," in tmp2[0]:
                tmp4 = tmp2[0].split(",")
                for port in tmp4:
                    entity_vhdl.port.append(
                        [port.strip(), tmp3[0].strip(), port_type, port_width]
                    )
            else:
                entity_vhdl.port.append(
                    [tmp2[0].strip(), tmp3[0].strip(), port_type, port_width]
                )
        elif ("<=" in i) & (";" in i): # assignment detector
            tmp1 = i.strip()
            if "--" in tmp1:
                tmp_comment = tmp1.split("--")
                tmp2 = tmp_comment[0].split("<=")
            else:
                tmp2 = tmp1.split("<=")
            tmp2[0] = tmp2[0].strip()
            tmp2[1] = tmp2[1][:-1].strip()
            entity_vhdl.assign.append([tmp2, vhdl_line])
        # elif(sys.argv[2]  in i):
        #     tmp1 = i.strip()
        #     entity_vhdl[0].search.append([i,vhd.index(i)])

    entity_vhdl.children_name = list(dict.fromkeys(entity_vhdl.children_name))
    return entity_vhdl

# args = parse_vhdl_arg_parse()
# inp_fname = args.input

# vhdl_as_obj = parse_vhdl(inp_fname)
# vhdl_as_obj.who_is()
# print("xx")
