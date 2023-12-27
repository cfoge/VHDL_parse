import unittest

# Import the function to be tested
from token_test import *

class Test_Parse_VHDL_interface(unittest.TestCase):
    def test_no_input(self):
        file_name = ''
        returned = parse_vhdl(file_name)
        expected_returned = "Error: Failed to read file"
        self.assertEqual(returned, expected_returned)

    def test_input_not_file(self):
        file_name = '../'
        returned = parse_vhdl(file_name)
        expected_returned = "Error: Failed to read file"
        self.assertEqual(returned, expected_returned)
    
    def test_input_not_correct_type_file(self):
        file_name = 'token_test.py'
        returned = parse_vhdl(file_name)
        expected_returned = "Error: file not of type .vhd or .vhdl"
        self.assertEqual(returned, expected_returned)

    def test_correct_input_retruns_object(self):
        file_name = 'tests/test1.vhdl'
        returned = type(parse_vhdl(file_name, just_port = False))
        expected_returned = type(vhdl_obj())
        self.assertEqual(returned, expected_returned)

    def test_correct_input_retruns_object_just_port(self):
        file_name = 'tests/test1.vhdl'
        returned = type(parse_vhdl(file_name, just_port = True))
        expected_returned = type(vhdl_obj())
        self.assertEqual(returned, expected_returned)

    def Test_lib_decode(self):
        file_name = 'tests/test1.vhdl'
        returned = (parse_vhdl(file_name)).lib
        expected_returned = type(vhdl_obj())
        self.assertEqual(returned, expected_returned)

######

# Create a test suite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(Test_Parse_VHDL_interface))

# Run the test suite
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite)