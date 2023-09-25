import unittest

# Import the function to be tested
from token_test import tokenize_vhdl_code , replace_end_process_tokens, extract_bit_len, find_type, find_width

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


# Create a test suite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestTokenizeVHDLCode))
test_suite.addTest(unittest.makeSuite(TestReplaceEndProcessTokens))

# Run the test suite
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite)