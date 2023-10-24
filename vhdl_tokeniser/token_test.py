import re

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
        self.modname = ''
        self.url = ''


# Define regular expressions for VHDL tokens
token_patterns = [
    (r'^\s+', 'SpaceToken'),  # Match whitespace characters
    (r'^--.*', 'SingleLineCommentToken'),  # Match single-line comments
    (r'^\b--.*\n', 'SingleLineCommentToken'),  # Match single-line comments ending with newline
    (r'^/\*.*?\*/', 'MultiLineCommentToken'),  # Match multi-line comments
    (r'^:|;|\(|\)|,', 'DelimiterToken'),  # Match delimiters like :, ;, (, ), and ,
    # (r'^:=', 'AssignmentOperatorToken'),  # Match assignment operator :=
    (r'^\b(library|use|if|entity|architecture|begin|end|process|generic|generate|port|process|signal|constant|function|package|type|subtype)\b', 'KeywordToken'),  # Match keywords
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
    'type'    : 'TypeKeyword'     #needs beter decoding
}


# Define a function to tokenize VHDL code
def tokenize_vhdl_code(code):
    tokens = []
    code_length = len(code)
    current_position = 0
    in_multi_line_comment = False

    while current_position < code_length:
        if in_multi_line_comment:
            multi_line_comment_end = code.find('*/', current_position)
            if multi_line_comment_end != -1:

                tokens.append(('MultiLineCommentToken', code[current_position:multi_line_comment_end]))
                current_position = multi_line_comment_end + 2
                in_multi_line_comment = False
            else:
                tokens.append(('MultiLineCommentToken', code[current_position:]))
                break
        else:
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
        next_prev_pop = 2
        if token_text == '=':
             try:
                token_type_next, token_text_next = tokens[i+1]
                next_prev_pop = 1
             except:
                  token_text_next = None
             try:
                token_type_prev, token_text_prev = tokens[i-1]
                next_prev_pop = 0
             except:
                  token_text_prev = None
             
             if token_text_next == '>':
                tokens[i] = ('AssignKeyword', '=>')
                tokens.pop(i+1)
                # elif next_prev_pop == 0: 
                #     tokens.pop(i-1)
             if token_text_prev == ':':
                tokens[i] = ('AssignKeyword', ':=')
                # if next_prev_pop == 1:
                #     tokens.pop(i+1)
                # elif next_prev_pop == 0: 
                tokens.pop(i-1)
             if token_text_prev == '<':
                tokens[i] = ('AssignKeyword', '<=')
                # if next_prev_pop == 1:
                #     tokens.pop(i+1)
                # elif next_prev_pop == 0: 
                tokens.pop(i-1)
                

        if token_type == 'EndKeyword':
            # Search for the next keyword token
            next_keyword_index = i + 1
            while next_keyword_index < len(tokens) and not tokens[next_keyword_index][0].endswith('Keyword'):
                next_keyword_index += 1

            if next_keyword_index < len(tokens):
                next_keyword_type = tokens[next_keyword_index][0]

                if next_keyword_type == 'ProcessKeyword':
                    # Replace tokens between 'EndKeyword' and 'ProcessKeyword' with 'EndProcessKeyword'

                        tokens[i] = ('EndProcessKeyword', tokens[i][1])
                        tokens.pop(next_keyword_index)

                if next_keyword_type == 'IfKeyword':
                    # Replace tokens between 'EndKeyword' and 'ProcessKeyword' with 'EndProcessKeyword'

                        tokens[i] = ('EndIfKeyword', tokens[i][1])
                        tokens.pop(next_keyword_index)

                if next_keyword_type == 'FunctionKeyword':
                    # Replace tokens between 'EndKeyword' and 'ProcessKeyword' with 'EndProcessKeyword'

                        tokens[i] = ('EndFunctionKeyword', tokens[i][1])
                        tokens.pop(next_keyword_index)

                if next_keyword_type == 'GenerateKeyword':
                    # Replace tokens between 'EndKeyword' and 'ProcessKeyword' with 'EndProcessKeyword'

                        tokens[i] = ('EndGenerateKeyword', tokens[i][1])
                        tokens.pop(next_keyword_index)

                if next_keyword_type == 'EntityKeyword':
                    # Replace tokens between 'EndKeyword' and 'ProcessKeyword' with 'EndProcessKeyword'

                        tokens[i] = ('EndEntityKeyword', tokens[i][1])
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


def make_block(token_type,current_position,end_token, sirch_dir=1, search_limit=0, add_space = 0):
        start_pos = current_position
        search_position = current_position
        token_list = []
        if sirch_dir == 1:
            start = search_position
            end = len(tokens)
        else:
            start = search_position
            end = len(tokens) - search_position
        for i in range(start, end):
            if(abs(start_pos - current_position)> search_limit) and search_limit != 0:
                return -1
            this_token_type = token_type
            token_type, token_text = tokens[i]
            if token_text == end_token:
                if len(token_list)==1:
                    return token_list[0][1]
                else:
                    out_str = ''
                    for token_type, token_text in token_list:
                        if add_space == 1:
                            out_str = out_str + " " + token_text
                        else:
                            out_str = out_str + token_text
                    return out_str

            if token_type != 'SpaceToken' and token_type != this_token_type:
                token_list.append((token_type, token_text))
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        if sirch_dir == 1:
            current_position = current_position + 1
        else: 
            current_position = current_position - 1
        return -1

def find_name(token_type,current_position, search_limit, dir = 0, sperator = ':'):
        if dir == 0:
            end = 0
            step = -1
        else:
            end = len(tokens)
            step = 1
        start_pos = current_position
        search_position = current_position
        token_list = []
        start = search_position
        for i in range(start, end, step):
            if(abs(start_pos - current_position)> search_limit) and search_limit != 0:
                return "Unnammed"
            this_token_type = token_type
            token_type, token_text = tokens[i]
            if token_text == sperator:
                global gen_trigger
                gen_trigger = tokens[i:current_position]
                for j in range(i, current_position-search_limit,-1):
                    this_token_type = token_type
                    token_type, token_text = tokens[j]
                    if token_type == 'IdentifierToken' and token_text != 'downto':
                        return token_text
                    if token_type == 'EndKeyword' or token_text == 'port' or token_text == ';':
                        return "end"
                return "Unnammed"
            if token_type != 'SpaceToken' and token_type != this_token_type:
                token_list.append((token_type, token_text))

        return -1

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

            if token_type in end_token.values() and token_type != port_token:
                return token_list[0:-1]
            if token_text == splitter:
                port_num = port_num + 1
                token_list.append('')

            if token_type != 'SpaceToken' and token_type != this_token_type:

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
                return token_list[0:-1]
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
    type_found = "null"
    input_line = input_line.lower()
    if "array" in input_line:
        array_type = find_type(input_line.replace("array",''))
        type_found = "array: " + array_type  
    elif "std_logic_vector" in input_line:
        type_found = "std_logic_vector"
    elif "std_logic" in input_line:
        type_found = "std_logic"
    elif "bit_vector" in input_line:
        type_found = "bit_vector"
    elif "bit" in input_line:
        type_found = "bit"
    elif "boolean" in input_line:
        type_found = "boolean"
    elif "integer" in input_line:
        type_found = "interger"
    elif "unsigned" in input_line:
        type_found = "unsigned"
    elif "signed" in input_line:
        type_found = "signed"
    # add more types
    elif "std_ulogic_vector" in input_line:
        type_found = "std_ulogic_vector"
    elif "std_ulogic" in input_line:
        type_found = "std_ulogic"
    elif "positive" in input_line:
        type_found = "positive"
    elif "natural" in input_line:
        type_found = "natural"
    elif "real" in input_line:
        type_found = "real"
    return type_found

def find_width(input_line, type_in):
    size_found = "null"
    if type_in == "std_logic_vector":
        size_found = extract_bit_len(input_line)
    elif type_in == "std_logic":
        size_found = 1
    elif "bit_vector" in input_line:
        size_found = "bit_vector"
    elif "bit" in input_line:
        size_found = 1
        # add for more types
    elif type_in == "std_ulogic_vector":
        size_found = extract_bit_len(input_line)
    elif type_in == "std_ulogic":
        size_found = 1
    return size_found

def extract_bit_len_not_numbers(str_in):
        match = re.search(r'(\d+)\s+downto\s+(\d+)', str_in)
        
        if match:
            first_part = match.group(1)
            # Extract the numbers
            before_downto = int(match.group(1))
            after_downto = int(match.group(2))
            bit_len = (before_downto + 1 - after_downto)
            return bit_len
        else:
            return None

def extract_bit_len(str_in):
           # Find the number before and after 'downto'
    if ('-' in str_in or '/' in str_in or '+' in str_in or '*' in str_in) and 'downto' in str_in:
        a_num = False
        b_num = False
        split_str = str_in.split('downto')
        if validate_list_elements_equations(split_str[0]):
            msb = calculate_equations(split_str[0])
            a_num = True
        else:
            msb = extract_bit_len_not_numbers(split_str[0])
        if validate_list_elements_equations(split_str[1]):
            lsb = calculate_equations(split_str[1])
            b_num = True
        else:
            msb = extract_bit_len_not_numbers(split_str[1])
        if a_num == True and b_num == True:
            bit_len = (int(msb) + 1 - int(lsb))
        else:
            bit_len = None
        return bit_len

    else:    
        return_len = extract_bit_len_not_numbers(str_in)
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

def format_port(decoded_gen, generic = False):
        result = [] 
        for i in decoded_gen:
                type_found = False
                in_out_inout = ''
                if generic == False:
                    
                    if " in " in i:
                        in_out_inout = ' in'
                    elif " out " in i:
                        in_out_inout = ' out'
                    elif " inout " in i:
                        in_out_inout = ' inout'


                if " subtype " in i:
                    i = i.replace("subtype" , "")
                    i = i.strip()
                if " type " in i:
                    i = i.replace("type" , "")
                    i = i.strip()
                    type_found = True
                    type_val = i.split(" of ")
                    if ";" in type_val[1]:
                        type_val[1] = type_val[1].replace(";", "")

                if "," in i and ":" in i :
                    split_sig = i.split(": ")
                    sig_names = split_sig[0]
                    sig_dec = split_sig[1]
                    i = sig_dec
                    split = i.split(" ")
                    name = sig_names.split(",")
                    if name[0] == "":
                        continue
                    port_type = find_type(i)
                    if port_type == "null":
                        port_type = is_port_type_dec(i, entity_vhdl)
                    port_width = find_width(i, port_type)
                    port_val = None
                    if type_found == True:
                        port_val = type_val[1].strip()
                    if "=" in i:
                        equal_sign_index = i.find('=')
                        if equal_sign_index != -1:
                            # Extract the text after '=' with no spaces
                            port_temp = i[equal_sign_index + 1:].replace(' ', '')
                            port_temp = port_temp.replace("'", '')
                                # Check if the result is a number and convert it if it is
                            try:
                                if port_type in ["real", "natural"]:
                                    port_val = float(port_temp) 
                                else:
                                    port_val = int(port_temp)  # Convert to float (or int if it's an integer)
                            except ValueError:
                                port_val = port_temp
                    for sig_name in name:
                        if in_out_inout != "":
                            result.append(
                                [sig_name.strip(),in_out_inout, port_type, port_width, port_val]
                                )
                        else:
                            result.append(
                                [sig_name.strip(), port_type, port_width, port_val]
                                )

                else:
## dont repeat this break it oput into a func
                    split = i.split(" ")
                    name = split[0]
                    if name == "":
                        continue
                    port_type = find_type(i)
                    if port_type == "null":
                        port_type = is_port_type_dec(i, entity_vhdl)
                    port_width = find_width(i, port_type)
                    port_val = None
                    if type_found == True:
                        port_val = type_val[1].strip()
                    if "=" in i:
                        equal_sign_index = i.find('=')
                        if equal_sign_index != -1:
                            # Extract the text after '=' with no spaces
                            port_temp = i[equal_sign_index + 1:].replace(' ', '')
                            port_temp = port_temp.replace("'", '')
                                # Check if the result is a number and convert it if it is
                            try:
                                if port_type in ["real", "natural"]:
                                    port_val = float(port_temp) 
                                else:
                                    port_val = int(port_temp)  # Convert to float (or int if it's an integer)
                            except ValueError:
                                port_val = port_temp
                    if in_out_inout != "":
                        result.append(
                            [name,in_out_inout, port_type, port_width, port_val]
                            )
                    else:
                        result.append(
                            [name, port_type, port_width, port_val]
                            )
        for found_port in result:
            if found_port[0] == entity_vhdl.data and found_port[1] == 'null':
                result.pop(result.index(found_port))
        return result

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

def parse_vhdl(file_name):
    global entity_vhdl
    file_path = file_name
    # file_path = "fan_control.vhd"  # Replace with the path to your VHDL file
    vhdl_code = read_vhdl_file(file_path).lower()
    tokens_raw = tokenize_vhdl_code(vhdl_code)
    global tokens
    tokens = replace_end_process_tokens(tokens_raw)


    proces_ranges = extract_process_lines(tokens, "ProcessKeyword", "EndProcessKeyword")
    generate_ranges = extract_process_lines(tokens, "GenerateKeyword", "EndGenerateKeyword")
    func_ranges = extract_process_lines(tokens, "FunctionKeyword", "EndFunctionKeyword")

    entity_vhdl = vhdl_obj()
    entity_vhdl.url = file_path

    current_position = 0  # Initialize the current position
    search_position = 0 
    global_entity = 0
    global_arch = 0
    global_sig = 0


    for token_type, token_text in tokens:
        if token_type == 'LibraryKeyword':
            entity_vhdl.lib.append(make_block(token_type,current_position,";"))
        if token_type == 'UseKeyword':
            entity_vhdl.lib.append(make_block(token_type,current_position,";"))


        if token_type == 'EntityKeyword' and global_entity == 1:
                ent_name = find_name("IdentifierToken", current_position, 6)
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

        if token_type == 'EntityKeyword':
            if global_entity == 0: # detect first entity decleration which is module
                ent_name_found =   make_block(token_type,current_position,"is")
                if isinstance(ent_name_found,str):
                    entity_vhdl.data = ent_name_found
                else: 
                    entity_vhdl.data = "None"
                global_entity = 1
        
        if token_type == 'PackageKeyword':
            if global_entity == 0: # detect first entity decleration which is module
                ent_name_found =   make_block(token_type,current_position,"is")
                if isinstance(ent_name_found,str):
                    entity_vhdl.data = ent_name_found
                else: 
                    entity_vhdl.data = "None"
                global_entity = 1
                entity_vhdl.type = "package"


        if token_type == 'GenericKeyword' and len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
            decoded_gen = (decode_port(token_type,current_position,keyword_mapping, 'GenericKeyword'))
            entity_vhdl.generic = format_port(decoded_gen, True) # second arg tells the function that it is a generic and that it can ignore in/outs that appear in the line such as names 
            

        if token_type == 'PortKeyword' and len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
            decoded_por = (decode_port(token_type,current_position,keyword_mapping, 'PortKeyword'))
            entity_vhdl.port = format_port(decoded_por)

        if token_type == 'ArchitectureKeyword':
            if global_arch == 0: # detect first arch decleration which is module arch
                entity_vhdl.arch=(make_block(token_type,current_position,"of"))
                global_arch = 1

        if token_type == 'SignalKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            format_sig_tmp = format_port(decoded_por)
            if len(format_sig_tmp) == 1:
                entity_vhdl.signal.append(format_sig_tmp[0])
            else:
                for i in format_sig_tmp:
                    entity_vhdl.signal.append(i)

        if token_type == 'ConstantKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            entity_vhdl.constant.append(format_port(decoded_por, True)[0])

        if token_type == 'SubtypeKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            entity_vhdl.subtype.append(format_port(decoded_por)[0])

        if token_type == 'TypeKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            entity_vhdl.type_dec.append(format_port(decoded_por)[0])

        if token_type == 'GenerateKeyword' : 
            
            generate_name = find_name("IdentifierToken", current_position, 26)
            gen_triger_str = decode_block(gen_trigger,';')
            entity_vhdl.generate.append([generate_name,gen_triger_str[0].strip()])
        
        if token_type == 'ProcessKeyword':
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

        if token_text == '<=': # detect assignements
            ignore = 0
            #find out if the assign is inside of a func, generate or process and if so ignore for now
            for start, end in func_ranges:
                if start <= current_position <= end:
                    ignore = 1
                    break
            for start, end in proces_ranges:
                if start <= current_position <= end:
                    ignore = 1
                    break
            for start, end in generate_ranges:
                if start <= current_position <= end:
                    ignore = 1
                    break
            if ignore == 0:
                assign_from = make_block("<=",current_position+1,";",1, 0, 1) 
                assign_to  = find_name("IdentifierToken", current_position, 20, 0, " ") #using " " as a seperator could make issues in the future
                entity_vhdl.assign.append([assign_to, assign_from])

        if token_type == 'FunctionKeyword':
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
        


        #     # test = make_block(token_type,current_position,"end", 0, 5)
        #     # if make_block(token_type,current_position,"end", 0, 6) == -1 : # search back wards for an end that precedes the process so we only detect the start of processes
        #         prcess_name = find_name("IdentifierToken", current_position, 4)
        #         process_dep = make_block(token_type,current_position,")")
        #         entity_vhdl.process.append([prcess_name, process_dep])
        current_position = current_position + 1

    return entity_vhdl






# print("")
