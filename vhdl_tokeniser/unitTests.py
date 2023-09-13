import unittest

# Import the function to be tested
from token_test import tokenize_vhdl_code , replace_end_process_tokens

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
        expected_tokens = [('IdentifierToken', 'a'), ('EndProcessKeyword', 'end'), ('IdentifierToken', 'b'), ('ProcessKeyword', 'process')]
        replace_end_process_tokens(tokens)
        self.assertEqual(tokens, expected_tokens)

# Create a test suite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(TestTokenizeVHDLCode))
test_suite.addTest(unittest.makeSuite(TestReplaceEndProcessTokens))

# Run the test suite
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite)