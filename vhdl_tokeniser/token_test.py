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
    (r'^\b(library|use|entity|architecture|begin|end|process)\b', 'KeywordToken'),  # Match keywords
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
    'process': 'ProcessKeyword'
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

def make_block(token_type,current_position,end_token):
        search_position = current_position
        token_list = []
        for i in range(search_position, len(tokens)):
            this_token_type = token_type
            token_type, token_text = tokens[i]
            if token_type == 'DelimiterToken' and token_text == end_token:
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
        current_position = current_position + 1
        return -1


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
    for token_type, token_text in tokens:
        if token_type == 'LibraryKeyword':
            entity_vhdl.lib.append(make_block(token_type,current_position,";"))
        if token_type == 'UseKeyword':
            entity_vhdl.lib.append(make_block(token_type,current_position,";"))

        current_position = current_position + 1








print("")
