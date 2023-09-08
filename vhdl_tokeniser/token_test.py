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
        self.modname = ''
        self.url = ''


# Define regular expressions for VHDL tokens
token_patterns = [
    (r'^\s+', 'SpaceToken'),  # Match whitespace characters
    (r'^--.*', 'SingleLineCommentToken'),  # Match single-line comments
    (r'^\b--.*\n', 'SingleLineCommentToken'),  # Match single-line comments ending with newline
    (r'^/\*.*?\*/', 'MultiLineCommentToken'),  # Match multi-line comments
    (r'^:|;|\(|\)|,', 'DelimiterToken'),  # Match delimiters like :, ;, (, ), and ,
    (r'^:=', 'AssignmentOperatorToken'),  # Match assignment operator :=
    (r'^\b(library|use|entity|architecture|begin|end|process|generic|port|process|signal|constant)\b', 'KeywordToken'),  # Match keywords
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
    'process' : 'ProcessKeyword',
    'signal' : 'SignalKeyword',
    'constant' : 'ConstantKeyword'
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
                tokens.append(('MultiLineCommentToken', code[current_position:multi_line_comment_end + 2]))
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
                    if token_type == 'MultiLineCommentToken' and '/*' in matched_text:
                        in_multi_line_comment = True
                    elif token_type == 'SingleLineCommentToken' and '--' in matched_text:
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

def make_block(token_type,current_position,end_token, sirch_dir=1, search_limit=0):
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

def find_name(token_type,current_position, search_limit):
        start_pos = current_position
        search_position = current_position
        token_list = []
        start = search_position
        end = len(tokens) - search_position
        for i in range(start, end):
            if(abs(start_pos - current_position)> search_limit) and search_limit != 0:
                return "Unnammed"
            this_token_type = token_type
            token_type, token_text = tokens[i]
            if token_text == ':':
                for j in range(current_position, search_limit):
                    this_token_type = token_type
                    token_type, token_text = tokens[i]
                    if token_type == 'IdentifierToken':
                        return token_text
                    current_position = current_position - 1
                return "Unnammed"
            if token_type != 'SpaceToken' and token_type != this_token_type:
                token_list.append((token_type, token_text))
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
            current_position = current_position - 1
        return -1

def decode_port(token_type,current_position,end_token,port_token): #decodes lines with the strcutre of a port such as generics/assignements ect
        search_position = current_position
        token_list = ['']
        port_num = 0
        for i in range(search_position, len(tokens)):
            this_token_type = token_type
            token_type, token_text = tokens[i]

            if token_type in end_token.values() and token_type != port_token:
                return token_list[0:-1]
            if token_text == ';':
                port_num = port_num + 1
                token_list.append('')

            if token_type != 'SpaceToken' and token_type != this_token_type:

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken':
                        token_list[port_num] = token_list[port_num] + token_text + " "
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        current_position = current_position + 1
        return -1

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

                if token_type == 'IdentifierToken' or token_type == 'NumberToken' or token_type == 'CharacterToken':
                        token_list[port_num] = token_list[port_num] + token_text + " "
            # Check if the token is a delimiter token (adjust the condition as needed)

            # Update the current position for future searches
        current_position = current_position + 1
        return -1

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


def extract_bit_len(str_in):
           # Find the number before and after 'downto'
    match = re.search(r'(\d+)\s+downto\s+(\d+)', str_in)
    
    if match:
        # Extract the numbers
        before_downto = int(match.group(1))
        after_downto = int(match.group(2))
        bit_len = (before_downto + 1 - after_downto)
        return bit_len
    else:
        return None

def format_port(decoded_gen):
            result = []
            for i in decoded_gen:
                split = i.split(" ")
                name = split[0]
                port_type = find_type(i)
                port_width = find_width(i, port_type)
                port_val = None
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
                if "," in i:

                    tmp4 = i.split(",")
                    for port in tmp4:
                        result.append(
                            [port.strip(), tmp3[0].strip(), port_type, port_width, port_val]
                        )
                else:
                    result.append(
                        [name, port_type, port_width, port_val]
                    )
            return result



# Read VHDL code from a file
def read_vhdl_file(file_path):
    with open(file_path, 'r') as file:
        vhdl_code = file.read()
    return vhdl_code

if __name__ == "__main__":
    file_path = "fan_control.vhd"  # Replace with the path to your VHDL file
    vhdl_code = read_vhdl_file(file_path)
    tokens = tokenize_vhdl_code(vhdl_code)

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
        if token_type == 'EntityKeyword':
            if global_entity == 0: # detect first entity decleration which is module
                entity_vhdl.data = make_block(token_type,current_position,"is")
                global_entity = 1
        if token_type == 'GenericKeyword' and len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
            
            decoded_gen = (decode_port(token_type,current_position,keyword_mapping, 'GenericKeyword'))
            entity_vhdl.generic = format_port(decoded_gen)
            

        if token_type == 'PortKeyword' and len(make_block(token_type,current_position,"(")) == 0: # there is no 'map' following the generic keyword
            decoded_por = (decode_port(token_type,current_position,keyword_mapping, 'PortKeyword'))
            entity_vhdl.port = format_port(decoded_por)

        if token_type == 'ArchitectureKeyword':
            if global_arch == 0: # detect first arch decleration which is module arch
                entity_vhdl.arch=(make_block(token_type,current_position,"of"))
                global_arch = 1

        if token_type == 'SignalKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            entity_vhdl.signal.append(format_port(decoded_por)[0])

        if token_type == 'ConstantKeyword' : 
            decoded_por = (decode_sig(token_type,current_position,";"))
            entity_vhdl.constant.append(format_port(decoded_por)[0])
        # if token_type == 'ProcessKeyword':
        #     # test = make_block(token_type,current_position,"end", 0, 5)
        #     # if make_block(token_type,current_position,"end", 0, 6) == -1 : # search back wards for an end that precedes the process so we only detect the start of processes
        #         prcess_name = find_name("IdentifierToken", current_position, 4)
        #         process_dep = make_block(token_type,current_position,")")
        #         entity_vhdl.process.append([prcess_name, process_dep])
        current_position = current_position + 1








print("")
