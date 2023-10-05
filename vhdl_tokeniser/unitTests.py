import unittest

# Import the function to be tested
from token_test import tokenize_vhdl_code , replace_end_process_tokens, extract_bit_len, find_type, find_width, extract_tokens_between, decode_block, extract_process_lines, format_port

class TestTokenizeVHDLCode(unittest.TestCase):
    def test_empty_input(self):
        code = ''
        tokens = tokenize_vhdl_code(code)
        self.assertEqual(tokens, [])

    def test_single_line_comment(self):
        code = '-- This is a single-line comment'
        tokens = tokenize_vhdl_code(code)
        expected_tokens = [('SingleLineCommentToken', '-- This is a single-line comment')]
        self.assertEqual(tokens, expected_tokens)

    def test_keywords_and_identifiers(self):
        code = 'entity example is\nend entity;'
        tokens = tokenize_vhdl_code(code)
        expected_tokens = [
            ('EntityKeyword', 'entity'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'example'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'is'),
            ('SpaceToken', '\n'),
            ('EndKeyword', 'end'),
            ('SpaceToken', ' '),
            ('EntityKeyword', 'entity'),
            ('DelimiterToken', ';')
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_character_tokens(self):
        code = ':, >, <'
        tokens = tokenize_vhdl_code(code)
        expected_tokens = [
            ('DelimiterToken', ':'),
            ('DelimiterToken', ','),
            ('SpaceToken', ' '),
            ('CharacterToken', '>'),
            ('DelimiterToken', ','),
            ('SpaceToken', ' '),
            ('CharacterToken', '<'),
        ]
        self.assertEqual(tokens, expected_tokens)
    


class TestReplaceEndProcessTokens(unittest.TestCase):
    def test_replace_assignment_operator(self):
        tokens = [('DelimiterToken', ':'), ('AssignKeyword', '=')]
        expected_tokens = [('AssignKeyword', ':=')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_replace_association_operator(self):
        tokens = [('AssignKeyword', '='), ('CharacterToken', '>')]
        expected_tokens = [('AssignKeyword', '=>')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_replace_association_operator_with_other_tokens(self):
        tokens = [('CharacterToken', 'a'), ('CharacterToken', '<'), ('AssignKeyword', '='), ('CharacterToken', 'b')]
        expected_tokens = [('CharacterToken', 'a'), ('AssignKeyword', '<='), ('CharacterToken', 'b')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_replace_end_process_keywords(self):
        tokens = [('EndKeyword', 'end'), ('ProcessKeyword', 'process')]
        expected_tokens = [('EndProcessKeyword', 'end')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_replace_end_process_keywords_with_other_tokens(self):
        tokens = [('IdentifierToken', 'a'), ('EndKeyword', 'end'), ('IdentifierToken', 'b'), ('ProcessKeyword', 'process')]
        expected_tokens = [('IdentifierToken', 'a'), ('EndProcessKeyword', 'end'), ('IdentifierToken', 'b')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

    def test_extract_bit_len_with_valid_input(self):
        input_string = "7 downto 3"
        expected_result = 5
        result = extract_bit_len(input_string)
        self.assertEqual(result, expected_result)

    def test_extract_bit_len_with_invalid_input(self):
        input_string = "no_downto_here"
        expected_result = None
        result = extract_bit_len(input_string)
        self.assertEqual(result, expected_result)

    def test_extract_bit_len_with_invalid_input(self):
        input_string = "x downto y"
        expected_result = None
        result = extract_bit_len(input_string)
        self.assertEqual(result, expected_result)

    def test_find_type_with_valid_input(self):
        input_line = "signal my_signal: std_logic_vector(7 downto 0);"
        expected_result = "std_logic_vector"
        result = find_type(input_line)
        self.assertEqual(result, expected_result)

    def test_find_type_with_invalid_input(self):
        input_line = "signal my_signal: int(7 downto 0);"
        expected_result = "null"
        result = find_type(input_line)
        self.assertEqual(result, expected_result)

    def test_find_width_with_std_logic_vector(self):
        input_line = "signal my_signal: std_logic_vector(7 downto 0);"
        type_in = "std_logic_vector"
        expected_result = 8
        result = find_width(input_line, type_in)
        self.assertEqual(result, expected_result)

    def test_find_width_with_std_logic(self):
        input_line = "signal my_signal: std_logic;"
        type_in = "std_logic"
        expected_result = 1
        result = find_width(input_line, type_in)
        self.assertEqual(result, expected_result)

    def test_find_width_with_invalid_input(self):
        input_line = "signal my_signal: int(7 downto 0);"
        type_in = "int"  # Invalid type
        expected_result = "null"
        result = find_width(input_line, type_in)
        self.assertEqual(result, expected_result)

    def test_tokenize_vhdl_code_with_single_line_comment(self):
        code = "entity Test is\n-- This is a single-line comment\nend entity;"
        expected_tokens = [
            ('EntityKeyword', 'entity'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'Test'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'is'),
            ('SpaceToken', '\n'),
            ('SingleLineCommentToken', '-- This is a single-line comment'),
            ('SpaceToken', '\n'),
            ('EndKeyword', 'end'),
            ('SpaceToken', ' '),
            ('EntityKeyword', 'entity'),
            ('DelimiterToken', ';')
        ]
        tokens = tokenize_vhdl_code(code)
        self.assertEqual(tokens, expected_tokens)

    # def test_tokenize_vhdl_code_with_multi_line_comment(self):
    #     code = "/* This is\na multi-line\ncomment */"
    #     expected_tokens = [('MultiLineCommentToken', ' This is\na multi-line\ncomment ')]
    #     tokens = tokenize_vhdl_code(code)
    #     self.assertEqual(tokens, expected_tokens)

    def test_tokenize_vhdl_code_with_identifiers(self):
        code = "signal my_signal: std_logic;"
        expected_tokens = [
            ('SignalKeyword', 'signal'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'my_signal'),
            ('DelimiterToken', ':'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'std_logic'),
            ('DelimiterToken', ';')
        ]
        tokens = tokenize_vhdl_code(code)
        self.assertEqual(tokens, expected_tokens)

    def test_extract_tokens_between_with_valid_tokens(self):
        # Sample tokens for testing
        sample_tokens = [
            ('KeywordToken', 'entity'),
            ('IdentifierToken', 'my_entity'),
            ('KeywordToken', 'is'),
            ('KeywordToken', 'port'),
            ('IdentifierToken', 'input_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'in'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';'),
            ('IdentifierToken', 'output_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'out'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';'),
            ('KeywordToken', 'end'),
            ('KeywordToken', 'entity'),
            ('CharacterToken', ';')
        ]
        # Assuming you want to extract tokens between 'port' and 'end entity'
        start_token_text = 'port'
        end_token_text = 'end'
        expected_tokens = [
            ('IdentifierToken', 'input_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'in'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';'),
            ('IdentifierToken', 'output_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'out'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';')
        ]
        
        result = extract_tokens_between(sample_tokens, start_token_text, end_token_text)
        
        # Assert that the result is a list of extracted tokens
        self.assertIsInstance(result, list)
        # Assert that the result contains the expected tokens
        self.assertEqual(result, expected_tokens)

    def test_extract_tokens_between_with_missing_end_token(self):
        # Sample tokens for testing
        sample_tokens = [
            ('KeywordToken', 'entity'),
            ('IdentifierToken', 'my_entity'),
            ('KeywordToken', 'is'),
            ('KeywordToken', 'port'),
            ('IdentifierToken', 'input_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'in'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';'),
            ('IdentifierToken', 'output_signal'),
            ('CharacterToken', ':'),
            ('KeywordToken', 'out'),
            ('KeywordToken', 'std_logic'),
            ('CharacterToken', ';'),
            ('KeywordToken', 'end'),
            ('KeywordToken', 'entity'),
            ('CharacterToken', ';')
        ]
        # Test when the end token is not found
        start_token_text = 'port'
        end_token_text = 'missing_token'
        
        result = extract_tokens_between(sample_tokens, start_token_text, end_token_text)
        
        # Assert that the result is an empty list when the end token is missing
        self.assertEqual(result, None)

    def test_decode_block(self):
        # Test input data
        block = [
            ('IdentifierToken', 'foo'),
            ('SpaceToken', ' '),
            ('CharacterToken', '='),
            ('SpaceToken', ' '),
            ('NumberToken', '42'),
            ('CharacterToken', ';'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'bar'),
            ('SpaceToken', ' '),
            ('CharacterToken', '='),
            ('SpaceToken', ' '),
            ('NumberToken', '123'),
            ('CharacterToken', ';'),
        ]

        endLine = ';'

        # Expected output
        expected_result = ['foo = 42 ', 'bar = 123 ']

        # Call the function being tested
        result = decode_block(block, endLine)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_result)

    def test_extract_process_lines(self):
        # Test input data
        tokens = [
            ('ProcessKeyword', 'PROCESS'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'Process1'),
            ('SpaceToken', ' '),
            ('KeywordToken', 'BEGIN'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'A'),
            ('SpaceToken', ' '),
            ('CharacterToken', '='),
            ('SpaceToken', ' '),
            ('NumberToken', '1'),
            ('SpaceToken', ' '),
            ('EndKeyword', 'END'),
            ('SpaceToken', ' '),
            ('ProcessKeyword', 'PROCESS'),
            ('SpaceToken', ' '),
            ('ProcessKeyword', 'PROCESS'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'Process2'),
            ('SpaceToken', ' '),
            ('KeywordToken', 'BEGIN'),
            ('SpaceToken', ' '),
            ('IdentifierToken', 'B'),
            ('SpaceToken', ' '),
            ('CharacterToken', '='),
            ('SpaceToken', ' '),
            ('NumberToken', '2'),
            ('SpaceToken', ' '),
            ('EndKeyword', 'END'),
            ('SpaceToken', ' '),
            ('ProcessKeyword', 'PROCESS'),
        ]

        start_keyword = 'ProcessKeyword'
        end_keyword = 'EndProcessKeyword'

        test_toekens = replace_end_process_tokens(tokens)
        # Expected output
        expected_result = [(0, 12), (15, 27)]

        # Call the function being tested
        result = extract_process_lines(test_toekens, start_keyword, end_keyword)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_result)

    ###### FORMAT PORT FUNCTION TESTS
    def test_format_port_single_port(self):
        decoded_gen = ["data real := 3.14"]
        expected_result = [["data", "real", 'null', 3.14]]
        self.assertEqual(format_port(decoded_gen), expected_result)

    def test_format_port_multiple_ports(self):
        decoded_gen = ["data real := 3.14", "clk : in std_logic"]
        expected_result = [
            ["data", "real", 'null', 3.14],
            ["clk","in", "std_logic", 1, None]
        ]
        self.assertEqual(format_port(decoded_gen), expected_result)

    def test_format_port_multiple_signals_same_value(self):
        decoded_gen = ["valid, Test2: out std_logic := '1'"]
        expected_result = [
            ["valid","out", "std_logic", 1, 1],
            ["Test2","out", "std_logic", 1, 1]
        ]
        self.assertEqual(format_port(decoded_gen), expected_result)

    def test_format_port_invalid_value(self):
        decoded_gen = ["data real := abc"]
        expected_result = [["data", "real", 'null', "abc"]]
        self.assertEqual(format_port(decoded_gen), expected_result)
    
    # def test_format_port_subtype(self):
    #     decoded_gen = ["subtype data is unsigned(12 downto 0);"]
    #     expected_result = [["data", "unsigned", 'null', None]]
    #     self.assertEqual(format_port(decoded_gen), expected_result)
    
    # def test_format_port_type(self):
    #     decoded_gen = ["type data is array (natural range<>) of dataType;"]
    #     expected_result = [["data", "array: natural", 'dataType', None]]
    #     self.assertEqual(format_port(decoded_gen), expected_result)

######

# Create a test suite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestTokenizeVHDLCode))
test_suite.addTest(unittest.makeSuite(TestReplaceEndProcessTokens))

# Run the test suite
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite)