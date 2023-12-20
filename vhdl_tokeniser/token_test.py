import re
from bisect import bisect_left

class instanc(object):
    def __init__(self, mod, name, line_num):
        self.mod = mod  # is module name
        self.name = name  # is module name
        self.line_num = line_num
        self.generic = []
        self.port = []
        self.vhdl_obj = None

class vhdl_obj(object):
    def __init__(self):
        self.type = []
        self.data = []
        self.line_num = []
        self.lib = []
        self.work = []
        self.arch = []
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
        self.subtype = []
        self.type_dec = []
        self.nonSynth = []
        self.func = []
        self.generate = []
        self.primitives = []
        self.modname = ''
        self.url = ''


primitives_list = [ # list of built in primitives (xilinx), should have anoption to pass in a list
    'oddr', 'bufg', 'xadc_wrapper', 'srlc32e', 'mmcme2_base', 'ibufds_gte2', 'bufgce', 'iobuf', 'ibufg', 'bufgmux_ctrl'
]

# Define regular expressions for VHDL tokens
token_patterns = [
    (r'^\s+', 'SpaceToken'),  # Match whitespace characters
    (r'^--.*', 'SingleLineCommentToken'),  # Match single-line comments
    (r'^\b--.*\n', 'SingleLineCommentToken'),  # Match single-line comments ending with newline
    (r'^/\*.*?\*/', 'MultiLineCommentToken'),  # Match multi-line comments
    (r'^:|;|\(|\)|,', 'DelimiterToken'),  # Match delimiters like :, ;, (, ), and ,
    # (r'^:=', 'AssignmentOperatorToken'),  # Match assignment operator :=
    (r'^\b(library|use|if|entity|architecture|begin|end|process|generic|generate|port|process|signal|constant|function|package|type|subtype|component)\b', 'KeywordToken'),  # Match keywords
    (r'^[A-Za-z][A-Za-z0-9_]*', 'IdentifierToken'),  # Match identifiers
    (r'^[0-9]+', 'NumberToken'),  # Match numbers
    (r'^.?', 'CharacterToken'),  # Match any other character
]

# Create a list of token types
token_types = [
    'StartOfDocumentToken', 'SpaceToken', 'DelimiterToken', 'AssignmentOperatorToken',
    'KeywordToken', 'IdentifierToken', 'NumberToken', 'CharacterToken',
    'FusedCharacterToken', 'CommentToken', 'SingleLineCommentToken', 'MultiLineCommentToken',
    'EndOfDocumentToken'
]

# Define a mapping of VHDL keywords to their specific types
keyword_mapping = {
    'library': 'LibraryKeyword',
    'use': 'UseKeyword',
    'entity': 'EntityKeyword',
    'architecture': 'ArchitectureKeyword',
    'begin': 'BeginKeyword',
    'end': 'EndKeyword',
    'process': 'ProcessKeyword',
    'generic': 'GenericKeyword',
    'port': 'PortKeyword',
    'signal' : 'SignalKeyword',
    'constant' : 'ConstantKeyword',
    'if' : 'IfKeyword',
    'function' : 'FunctionKeyword',
    'generate' : 'GenerateKeyword',
    'work'    : 'WorkKeyword',
    'package' : 'PackageKeyword',
    'subtype' : 'SubtypeKeyword', #needs beter decoding
    'type'    : 'TypeKeyword'  ,   #needs beter decoding
    'component' : 'ComponentKeyword'
}


# Define a function to tokenize VHDL code
def tokenize_vhdl_code(code):
    tokens = []
    code_length = len(code)
    current_position = 0
    in_multi_line_comment = False

    while current_position < code_length:
        # if in_multi_line_comment:
        #     multi_line_comment_end = code.find('*/', current_position)
        #     if multi_line_comment_end != -1:

        #         tokens.append(('MultiLineCommentToken', code[current_position:multi_line_comment_end]))
        #         current_position = multi_line_comment_end + 2
        #         in_multi_line_comment = False
        #     else:
        #         tokens.append(('MultiLineCommentToken', code[current_position:]))
        #         break
        # else:
            for pattern, token_type in token_patterns:
                match = re.match(pattern, code[current_position:])
                if match:
                    matched_text = match.group(0)
                    # if "/" in matched_text:
                    #     # if code[current_position+1] == '*':
                    #     #     in_multi_line_comment = True
                    #     #     current_position += 2
                    #         current_position += 1

                    if token_type == 'SingleLineCommentToken' and '--' in matched_text:
                        single_line_comment_end = matched_text.find('\n')
                        if single_line_comment_end != -1:
                            tokens.append(('SingleLineCommentToken', matched_text[:single_line_comment_end]))
                            current_position += single_line_comment_end
                        else:
                            tokens.append(('SingleLineCommentToken', matched_text))
                            current_position += len(matched_text)
                        break
                    elif token_type == 'CharacterToken':
                        tokens.append(('CharacterToken', matched_text[0]))
                        current_position += 1
                    elif token_type == 'KeywordToken':
                        keyword = matched_text.lower()
                        vhdl_type = keyword_mapping.get(keyword)
                        if vhdl_type:
                            tokens.append((vhdl_type, matched_text))
                        else:
                            tokens.append(('KeywordToken', matched_text))
                        current_position += len(matched_text)
                    # elif token_type == 'SpaceToken': ##############################skip spaces
                    #     current_position += len(matched_text)
                    else:
                        tokens.append((token_type, matched_text))
                        current_position += len(matched_text)
                    break
            else:
                # If no pattern matches, consider it a character token
                tokens.append(('CharacterToken', code[current_position]))
                current_position += 1

    return tokens

def replace_end_process_tokens(tokens):
    i = 0
    while i < len(tokens):
        token_type, token_text = tokens[i]

        if token_text == '=':
            try:
                token_type_next, token_text_next = tokens[i + 1]
            except IndexError:
                token_text_next = None

            try:
                token_type_prev, token_text_prev = tokens[i - 1]
            except IndexError:
                token_text_prev = None

            if token_text_next == '>':
                tokens[i] = ('AssignKeyword', '=>')
                tokens.pop(i + 1)

            elif token_text_prev == ':':
                tokens[i] = ('AssignKeyword', ':=')
                tokens.pop(i - 1)

            elif token_text_prev == '<':
                tokens[i] = ('AssignKeyword', '<=')
                tokens.pop(i - 1)

        elif token_text in primitives_list:
            tokens[i] = ('PrimitiveKeyword', token_text)

        elif token_type == 'EndKeyword':
            # Search for the next keyword token
            next_keyword_index = i + 1
            while next_keyword_index < len(tokens) and not tokens[next_keyword_index][0].endswith('Keyword'):
                next_keyword_index += 1

            if next_keyword_index < len(tokens):
                next_keyword_type = tokens[next_keyword_index][0]

                if next_keyword_type in ('ProcessKeyword', 'IfKeyword', 'FunctionKeyword',
                                         'GenerateKeyword', 'EntityKeyword', 'ComponentKeyword'):
                    # Replace tokens between 'EndKeyword' and next keyword with corresponding 'End...Keyword'
                    end_keyword_mapping = {
                        'ProcessKeyword': 'EndProcessKeyword',
                        'IfKeyword': 'EndIfKeyword',
                        'FunctionKeyword': 'EndFunctionKeyword',
                        'GenerateKeyword': 'EndGenerateKeyword',
                        'EntityKeyword': 'EndEntityKeyword',
                        'ComponentKeyword': 'EndComponentKeyword'
                    }
                    tokens[i] = (end_keyword_mapping[next_keyword_type], tokens[i][1])
                    tokens.pop(next_keyword_index)

        i += 1

    return tokens


def extract_process_lines(tokens, start_keyword, end_keyword):
    process_lines = []
    inside_process = False
    process_start = None

    for i, (token_type, _) in enumerate(tokens):
        if token_type == start_keyword and not inside_process:
            inside_process = True
            process_start = i
        elif token_type == end_keyword and inside_process:
            inside_process = False
            process_lines.append((process_start, i))
    
    return process_lines

# Example usage:
# tokens = [...]  # Your list of tokens
# keyword_mapping = {...}  # Your keyword mapping
# keyword_ranges = find_keyword_pairs(tokens, keyword_mapping)
# for keyword_type, ranges in keyword_ranges.items():
#     for start_index, end_index in ranges:
#         print(f'{keyword_type}: Line {start_index +
def find_next_ident(current_position, token_in = []):
    if len(token_in) == 0:
        tokens_to_parse = tokens
    else:
        tokens_to_parse = token_in
    end = len(tokens_to_parse)
    start = current_position
    for i in range(start, end):
        token_type, token_text = tokens_to_parse[i]
        if token_type == 'IdentifierToken':
            return token_text

    return -1

def find_prev_ident(current_position , token_in = []):
    if len(token_in) == 0:
        tokens_to_parse = tokens
    else:
        tokens_to_parse = token_in
    end = 0
    start = current_position
    for i in range(start, end, -1):
        token_type, token_text = tokens_to_parse[i]
        if token_type == 'IdentifierToken':
            return token_text

    return -1

def find_prev_till(current_position, end_tokens, token_in = []):
    if len(token_in) == 0:
        tokens_to_parse = tokens
    else:
        tokens_to_parse = token_in
    tokens_list = []
    end = current_position - 20
    if end < 0:
        end = 0
    start = current_position - 1
    for i in range(start, end, -1):
        token_type, token_text = tokens_to_parse[i]
        if token_text in end_tokens:
            token_str = ''
            for token_found in tokens_list:
                token_str = token_found + token_str
            return token_str
        else:
            if '\n' not in token_text and '--' not in token_text:
                tokens_list.append(token_text)
    return -1

def make_block(token_type, current_position, end_token, search_dir=1, search_limit=0, add_space=0, token_in=None):
    tokens_to_parse = token_in if token_in else tokens
    start_pos = current_position
    token_list = []

    start, end, step = (current_position, len(tokens_to_parse), 1) if search_dir == 1 else (current_position, 0, -1)

    for i in range(start, end, step):
        if abs(start_pos - current_position) > search_limit and search_limit != 0:
            return -1

        this_token_type, token_text = tokens_to_parse[i]

        if token_text == end_token:
            return token_list[0][1] if len(token_list) == 1 else ''.join(token_text for _, token_text in token_list)

        if token_type not in ('SpaceToken', this_token_type):
            token_list.append((this_token_type, token_text))

        if search_dir == 1:
            current_position += 1
        else:
            current_position -= 1

    return -1


def find_name(token_type,current_position, search_limit, dir = 0, sperator = ':'):
        if dir == 0:
            end = current_position - search_limit
            step = -1

        else:
            end = current_position + search_limit
            step = 1
        search_position = current_position
        token_list = []
        start = search_position
        for i in range(start, end, step):

            this_token_type = token_type
            token_type, token_text = tokens[i]
            if token_text.strip() == sperator:
                global gen_trigger
                gen_trigger = tokens[i:current_position]
                for j in token_list:
                    this_token_type = token_type
                    token_type, token_text = j
                    if token_type == 'IdentifierToken' and token_text != 'downto':
                        return token_text
                    if token_type == 'EndKeyword' or token_text == 'port' or token_text == ';':
                        return "end"
                return "Unnammed"
            if token_type != 'SpaceToken' and token_type != this_token_type:
                token_list.append((token_type, token_text))

        return "Unnammed"

def decode_port(token_type,current_position,end_token,port_token, token_in = 0, splitter = ';'): #decodes lines with the strcutre of a port such as generics/assignements ect
        if token_in != 0:
            tokens_int = token_in
            search_position = 0
        else:
            tokens_int = tokens
            search_position = current_position
        token_list = ['']
        port_num = 0
        for i in range(search_position, len(tokens_int)):
            this_token_type = token_type

            token_type, token_text = tokens_int[i]

            if token_type in end_token.values() and token_type not in port_token:
                return token_list
            if token_text == splitter:
                port_num = port_num + 1
                token_list.append('')

            if token_type != 'SpaceToken' and token_type != this_token_type and (token_text not in port_token):

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken' or token_type == 'AssignKeyword' or token_text == "," or token_text == ":":
                        token_list[port_num] = token_list[port_num] + token_text + " "
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        current_position = current_position + 1
        return -1

def decode_ent_port(token_in): #decodes lines with the strcutre of a port such as generics/assignements ect

        tokens_int = token_in
        search_position = 0

        token_list = ['']
        port_num = 0
        found_function = 0

        for i in range(search_position, len(tokens_int)):
            
            token_type, token_text = tokens_int[i]

            

            if "to_" in token_text:
                 found_function = 1
            if token_text == ';':
                return token_list
            if token_text == ',' and found_function == 0:
                port_num = port_num + 1
                token_list.append('')
            if token_text == ',' and found_function == 1:
                token_text = '/' #replace , with / to avoid parser confusion
                found_function = 0
            if token_type != 'SpaceToken':

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken':
                        if token_text != "," and token_text != 'map':
                            token_list[port_num] = token_list[port_num] + token_text + " "
                if token_text == "=>":
                        token_list[port_num] = token_list[port_num] + token_text + " "


            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        return -1

def decode_block(block,endLine): #decodes lines with the strcutre of a port such as generics/assignements ect
        token_list = ['']
        block_num = 0
        for i in range(len(block)):
            token_type, token_text = block[i]
            if token_text == endLine:
                block_num = block_num + 1
                token_list.append('')

            if token_type != 'SpaceToken' and token_text != endLine:

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken' or token_type == 'AssignKeyword':
                        token_list[block_num] = token_list[block_num] + token_text + " "
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        if token_list[-1] == '':
            token_list.remove('')                  
        return token_list

def decode_sig(token_type,current_position,end_token): #decodes lines with the strcutre of a port such as generics/assignements ect
        search_position = current_position
        token_list = ['']
        port_num = 0
        for i in range(search_position, len(tokens)):
            this_token_type = token_type
            token_type, token_text = tokens[i]

            if token_text == end_token:
                return token_list

            if token_type != 'SpaceToken' and token_type != this_token_type:

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken' or token_type == 'AssignKeyword' or token_text == "," or token_text == ":":
                        token_list[port_num] = token_list[port_num] + token_text + " "
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        current_position = current_position + 1
        return -1

def find_type(input_line):
    type_mapping = {
        "array": "array",
        "std_logic_vector": "std_logic_vector",
        "std_logic": "std_logic",
        "bit_vector": "bit_vector",
        "bit": "bit",
        "boolean": "boolean",
        "integer": "integer",
        "unsigned": "unsigned",
        "signed": "signed",
        "std_ulogic_vector": "std_ulogic_vector",
        "std_ulogic": "std_ulogic",
        "positive": "positive",
        "natural": "natural",
        "real": "real"
        # Add more types as needed
    }

    input_line = input_line
    
    for keyword, type_found in type_mapping.items():
        if keyword in input_line:
            return type_found

    return "null"

def find_width(input_line, type_in):
    width_functions = {
        "std_logic_vector": extract_bit_len,
        "std_logic": lambda line, type_str: 1,
        "bit_vector": lambda line, type_str: "bit_vector",
        "bit": lambda line, type_str: 1,
        "interger": extract_bit_len,
        "std_ulogic_vector": extract_bit_len,
        "signed": extract_bit_len,
        "unsigned": extract_bit_len,
        "std_ulogic": lambda line, type_str: 1
        # Add more types as needed
    }

    if type_in in width_functions:
        return width_functions[type_in](input_line, type_in)
    else:
        return "null"

def extract_bit_len_not_numbers(str_in, type_in):
        match = re.search(r'(\d+)\s+downto\s+(\d+)', str_in)
        
        if match:
            first_part = match.group(1)
            # Extract the numbers
            before_downto = int(match.group(1))
            after_downto = int(match.group(2))
            bit_len = (before_downto + 1 - after_downto)
            return bit_len
        else:
            if type_in in str_in:
                length = str_in.split(type_in)[1]
            else:
                length = str_in
            return length

def extract_bit_len(str_in, type_in = "std_logic_vector"):
           # Find the number before and after 'downto'
    if type_in == "interger":
        if "range" in str_in and "to" in str_in:
                split_str_tmp = str_in.split('range')
                split_str = split_str_tmp[1].strip()
                return split_str_tmp[1]       
        else:
            return_len = str_in
            return return_len
               
    elif ('-' in str_in or '/' in str_in or '+' in str_in or '*' in str_in) and 'downto' in str_in:
        a_num = False
        b_num = False
        split_str = str_in.split('downto')
        if validate_list_elements_equations(split_str[0]):
            msb = calculate_equations(split_str[0])
            a_num = True
        else:
            msb = extract_bit_len_not_numbers(split_str[0], type_in)
        if validate_list_elements_equations(split_str[1]):
            lsb = calculate_equations(split_str[1])
            b_num = True
        else:
            lsb = extract_bit_len_not_numbers(split_str[1], type_in)
        if a_num == True and b_num == True:
            bit_len = (int(msb) + 1 - int(lsb))
        else:
            bit_len = msb.strip() + " downto " + lsb.strip()
        return bit_len

    else:    
        return_len = extract_bit_len_not_numbers(str_in, type_in)
        return return_len
        
def is_port_type_dec(i, entity_vhdl):
    type_found = "null"
    for types in entity_vhdl.type_dec:
        if types[0] in i:
            type_found = types[0]
    return type_found

def validate_list_elements_equations(lst):
    for element in lst:
        # Check if the element is a string
        if not isinstance(element, str):
            return False
        
        # Check if the string represents a valid operation
        if element not in {'=', '-', '+', '/', '*'} and not element.replace('.', '', 1).isdigit():
            return False

    # All elements are either strings representing valid operations or numbers
    return True
    
def calculate_equations(string):
    # Regular expression to find more complex mathematical equations
    pattern = r'([-+]?\d*\.\d+|\d+|\w+)\s*([-+*/])\s*([-+]?\d*\.\d+|\d+|\w+)'

    equations = re.findall(pattern, string)

    results = []
    for equation in equations:
        try:
            result = eval(''.join(equation))
            # results.append((equation, result))
            results =  result
        except (ZeroDivisionError, SyntaxError, TypeError) as e:
            results.append((equation, f"Error: {e}"))
    if results == []:
        results = string
    return results

def format_port(decoded_gen, generic=False):
    result = []

    for i in decoded_gen:
        in_out_inout = ''
        type_found = False

        if not generic:
            if " in " in i:
                in_out_inout = 'in'
            elif " out " in i:
                in_out_inout = 'out'
            elif " inout " in i:
                in_out_inout = 'inout'

        if " subtype " in i:
            i = i.replace("subtype", "").strip()
        if " type " in i:
            i = i.replace("type", "").strip()
            type_found = True
            type_val = i.split(" of ")
            if ";" in type_val[1]:
                type_val[1] = type_val[1].replace(";", "")

        if "," in i and ":" in i:
            sig_names, sig_dec = i.split(": ")
            i = sig_dec
            split = i.split(" ")
            name = [n.strip() for n in sig_names.split(",") if n.strip()]
            port_type = find_type(i) if not type_found else type_val[1].strip()
            port_width = find_width(i, port_type)
            port_val = extract_port_val(i)

            for sig_name in name:
                result.append([sig_name, in_out_inout, port_type, port_width, port_val])

        else:
            split = i.split(" ")
            name = split[0]
            if name:
                port_type = find_type(i) if not type_found else type_val[1].strip()
                port_width = find_width(i, port_type)
                port_val = extract_port_val(i)

                result.append([name, in_out_inout, port_type, port_width, port_val])

    result = [found_port for found_port in result if found_port[0] != entity_vhdl.data or found_port[1] != 'null']

    return result


def extract_port_val(i):
    port_val = None
    if "=" in i:
        equal_sign_index = i.find('=')
        if equal_sign_index != -1:
            # Extract the text after '=' with no spaces
            port_temp = i[equal_sign_index + 1:].replace(' ', '').replace("'", '')
            try:
                if find_type(i) in ["real", "natural"]:
                    port_val = float(port_temp)
                else:
                    port_val = int(port_temp)
            except ValueError:
                port_val = port_temp
    return port_val

def extract_process_blocks(start):
    blocks = []
    block = []
    i = start

    token_type, token_text = tokens[i]

    if token_type == 'ProcessKeyword':
        block = []
        while i < len(tokens) and not (token_type == 'EndProcessKeyword'):
            block.append((token_type, token_text))
            i += 1
            if i < len(tokens):
                token_type, token_text = tokens[i]

        if i < len(tokens):
            # Skip the "end" keyword
            i += 1

    return block

def extract_tokens_between(tokens, start_token_text, end_token_text, current_index=0):
    extracted_tokens = []
    found_start = False

    for i in range(current_index, len(tokens)):
        token_type, token_text = tokens[i]

        if token_text == start_token_text:
            found_start = True
            extracted_tokens = []

        if found_start:
            if token_type != 'SpaceToken' and token_text != start_token_text and token_text != end_token_text:
                extracted_tokens.append((token_type, token_text))

        if token_text == end_token_text:
            found_start = False
            return extracted_tokens

# Read VHDL code from a file
def read_vhdl_file(file_path):
    with open(file_path, 'r') as file:
        try:
            vhdl_code = file.read()
        except:
             return ""
    return vhdl_code

def extract_text_until_keywords(file_path):
    with open(file_path, 'r') as file:
        extracted_text = ''
        for line in file:
            extracted_text += line
            if all(keyword in line.lower() for keyword in ["architecture", "of", "is"]):
                break
    return extracted_text

def is_in_ranges(ranges, current_position):
    index = bisect_left(ranges, (current_position,))
    return index % 2 == 1

def parse_vhdl(file_name, just_port = False):
    global entity_vhdl
    file_path = file_name
    # file_path = "fan_control.vhd"  # Replace with the path to your VHDL file
    if just_port == True:
        vhdl_code = extract_text_until_keywords(file_path)
    else:
        vhdl_code = read_vhdl_file(file_path).lower()
    tokens_raw = tokenize_vhdl_code(vhdl_code)
    global tokens
    tokens = replace_end_process_tokens(tokens_raw)

    if just_port == False:
        proces_ranges = extract_process_lines(tokens, "ProcessKeyword", "EndProcessKeyword")
        generate_ranges = extract_process_lines(tokens, "GenerateKeyword", "EndGenerateKeyword")
        func_ranges = extract_process_lines(tokens, "FunctionKeyword", "EndFunctionKeyword")
        component_ranges = extract_process_lines(tokens, "ComponentKeyword", "EndComponentKeyword")

    entity_vhdl = vhdl_obj()
    entity_vhdl.url = file_path
    component_list = []

    current_position = 0  # Initialize the current position
    global_entity = 0
    global_arch = 0
    first_begin_found = False

    token_actions = {
    'LibraryKeyword': 'lib',
    'UseKeyword': 'lib',
    'PrimitiveKeyword': 'primitives',
    # Add more token types as needed
}

    for token_type, token_text in tokens:
        if token_type in token_actions:
            entity_vhdl_list = getattr(entity_vhdl, token_actions[token_type])
            entity_vhdl_list.append(make_block(token_type, current_position, ";"))


        if ((token_type == 'EntityKeyword') or (token_text in component_list and first_begin_found == True) or (token_type == 'PrimitiveKeyword' and first_begin_found == True)) and global_entity == 1: # if we have found the global entity and we come across another entity
                if (token_text in component_list) or token_type == 'PrimitiveKeyword': # if we find a component instanciated inside the global module it will be called differently so we need to decode it differently to a regular entity decleration
                    ent_name = find_prev_ident(current_position)
                    # ent_name = find_name("IdentifierToken", current_position, 6)
                    entity = extract_tokens_between(tokens, token_text, ";",current_position)
                    mod_name = token_text
                else:
                    ent_name = find_prev_ident(current_position)
                    # ent_name = find_name("IdentifierToken", current_position, 6)
                    if ent_name == "generate":
                        ent_name = 'unnamed'
                    entity = extract_tokens_between(tokens, "entity", ";",current_position)
                    if entity[0][1] == 'work':
                        mod_name =  entity[0][1] + entity[1][1] + entity[2][1]
                    else: 
                        mod_name =  entity[0][1]
                    if 'work.' in mod_name:
                        tmp1 = mod_name.replace("work.", "")
                        mod_name = tmp1
                generic = []
                port = []
                if any(token_type == 'GenericKeyword' for token_type, _ in entity):
                    generic = extract_tokens_between(tokens, "generic", ";",current_position)
                if any(token_type == 'PortKeyword' for token_type, _ in entity):
                    port = extract_tokens_between(tokens, "port", ";",current_position)
                    port.append(('DelimiterToken',';'))
                    port.append(('EndKeyword','end'))

                mod = instanc(mod_name, ent_name, 0)

                if len(generic) > 0:
                    gen_dec = decode_ent_port(generic)
                    if gen_dec != -1:
                        for generic in gen_dec:
                            mod.gen.append(generic.split("=>"))
                if len(port) > 0:
                    port_dec = decode_ent_port(port)
                    for ports in port_dec:
                        temp1 = ports.split("=>")
                        if len(temp1)>1:
                            mod.port.append([temp1[0].strip(), temp1[1].strip()])
                #decode the port and genric if it exists

                entity_vhdl.children_name.append(mod)

        elif token_type == 'EntityKeyword':
            if global_entity == 0: # detect first entity decleration which is module
                ent_name_found =   make_block(token_type,current_position,"is")
                if isinstance(ent_name_found,str):
                    entity_vhdl.data = ent_name_found
                else: 
                    entity_vhdl.data = "None"
                global_entity = 1
        
        elif token_type == 'PackageKeyword':
            if global_entity == 0: # detect first entity decleration which is module
                ent_name_found =   make_block(token_type,current_position,"is")
                if isinstance(ent_name_found,str):
                    entity_vhdl.data = ent_name_found
                else: 
                    entity_vhdl.data = "None"
                global_entity = 1
                entity_vhdl.type = "package"

        try:
            if token_type == 'GenericKeyword' and len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
                decoded_gen = (decode_port(token_type,current_position,keyword_mapping, 'GenericKeyword'))
                entity_vhdl.generic = format_port(decoded_gen, True) # second arg tells the function that it is a generic and that it can ignore in/outs that appear in the line such as names 
        except:
            print()  

        if token_type == 'PortKeyword': 
            if len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
                port_belongs_to_component = False
                for range in component_ranges:
                    if current_position > range[0] and current_position < range[1]:
                        port_belongs_to_component = True
                        break
                if port_belongs_to_component == False:     
                    decoded_por = (decode_port(token_type,current_position,keyword_mapping, 'PortKeyword'))
                    entity_vhdl.port = format_port(decoded_por)



        elif token_type == 'ComponentKeyword': # there is no 'map' following the generic keyword
            compoent_name = find_next_ident(current_position)
            component_list.append(compoent_name)
            decoded_por = (decode_port(token_type,current_position,keyword_mapping, ['PortKeyword','ComponentKeyword',compoent_name, "is"]))
            entity_vhdl.component.append([compoent_name, format_port(decoded_por)])

        elif token_type == 'ArchitectureKeyword':
            if global_arch == 0: # detect first arch decleration which is module arch
                entity_vhdl.arch=(make_block(token_type,current_position,"of"))
                global_arch = 1
        if just_port == False:
            if token_type == 'SignalKeyword' : 
                decoded_por = (decode_sig(token_type,current_position,";"))
                format_sig_tmp = format_port(decoded_por)
                if len(format_sig_tmp) == 1:
                    entity_vhdl.signal.append(format_sig_tmp[0])
                else:
                    for i in format_sig_tmp:
                        entity_vhdl.signal.append(i)

            elif token_type == 'ConstantKeyword' : 
                decoded_por = (decode_sig(token_type,current_position,";"))
                entity_vhdl.constant.append(format_port(decoded_por, True)[0])

            elif token_type == 'SubtypeKeyword' : 
                decoded_por = (decode_sig(token_type,current_position,";"))
                entity_vhdl.subtype.append(format_port(decoded_por)[0])

            elif token_type == 'TypeKeyword' : 
                decoded_por = (decode_sig(token_type,current_position,";"))
                entity_vhdl.type_dec.append(format_port(decoded_por)[0])

            elif token_type == 'GenerateKeyword' : 
                generate_name = find_name("IdentifierToken", current_position, 26)
                gen_triger_str = decode_block(gen_trigger,';')
                try:
                    entity_vhdl.generate.append([generate_name,gen_triger_str[0].strip()])
                except:
                    print('')
            
            elif token_type == 'ProcessKeyword':
                    prcess_name = find_name("IdentifierToken", current_position, 9)
                    if prcess_name == "generate" or prcess_name == "end":
                        prcess_name = 'unnamed'
                    process_dep = make_block(token_type,current_position,")")
                    if process_dep != -1:
                        process_dep = process_dep[1:]
                    
                    process_def = [prcess_name, process_dep]
                    # process_contents = extract_process_blocks(current_position)
                    #need to handle contents in process block now like ifs and assignements, cases ect
                    entity_vhdl.process.append([prcess_name, process_dep] )

                    #search inside process for contents
            if token_text == 'assert':
                assert_tok = make_block("",current_position,";",1, 0, 1) 
                entity_vhdl.nonSynth.append(assert_tok)

            elif token_text == '<=': # detect assignements
                ignore = 0
                #find out if the assign is inside of a func, generate or process and if so ignore for now
                if is_in_ranges(func_ranges, current_position) or \
                    is_in_ranges(proces_ranges, current_position) or \
                    is_in_ranges(generate_ranges, current_position):
                        ignore = 1
                if ignore == 0:
                    # assign_from = find_prev_ident(current_position)
                    assign_from = make_block("<=",current_position+1,";",1, 0, 1) 
                    assign_to  = find_prev_till(current_position, [';','begin','\n','\n\n'])
                    # assign_to  = find_name("IdentifierToken", current_position, 10, 0, ";") #using " " as a seperator could make issues in the future
                    if assign_to == -1:
                        assign_to = "error"
                    entity_vhdl.assign.append([assign_to.strip(), assign_from.strip()])

            elif token_type == 'FunctionKeyword':
                    funct_name =  make_block(token_type,current_position,"(")
                    func_inputs_tmp = extract_tokens_between(tokens, "(", ")",current_position)
                    func_inputs_tmp2 = decode_block(func_inputs_tmp,';')
                    func_inputs = format_port(func_inputs_tmp2)

                    return_type_tmp = extract_tokens_between(tokens, "return", "is",current_position)
                    if return_type_tmp != None:
                        return_type = ("returnType", return_type_tmp[0][1])
                    else:
                        return_type = ("returnType", "None")
                    entity_vhdl.func.append([funct_name,func_inputs, return_type] )
            
            elif token_text == "begin" and first_begin_found == False:
                first_begin_found = True

            


            #     # test = make_block(token_type,current_position,"end", 0, 5)
            #     # if make_block(token_type,current_position,"end", 0, 6) == -1 : # search back wards for an end that precedes the process so we only detect the start of processes
            #         prcess_name = find_name("IdentifierToken", current_position, 4)
            #         process_dep = make_block(token_type,current_position,")")
            #         entity_vhdl.process.append([prcess_name, process_dep])
        current_position = current_position + 1

    return entity_vhdl






# print("")
