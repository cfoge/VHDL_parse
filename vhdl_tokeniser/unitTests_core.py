import unittest

# Import the function to be tested
from token_test import *

# THese unit tests check that the correct type is returned and that no errors are encountered from different file types
class Test_Parse_VHDL_interface(unittest.TestCase):
    def test_no_input(self):
        file_name = "Insert File path"
        returned = parse_vhdl(file_name)
        expected_returned = "Error: Failed to read file"
        self.assertEqual(returned, expected_returned)

    def test_input_not_file(self):
        file_name = "Insert File path"
        returned = parse_vhdl(file_name)
        expected_returned = "Error: Failed to read file"
        self.assertEqual(returned, expected_returned)

    def test_input_not_correct_type_file(self):
        file_name = "token_test.py"
        returned = parse_vhdl(file_name)
        expected_returned = "Error: file not of type .vhd or .vhdl"
        self.assertEqual(returned, expected_returned)

    def test_correct_input_retruns_object(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name, just_port=False))
        expected_returned = type(vhdl_obj())
        self.assertEqual(returned, expected_returned)

    def test_correct_input_retruns_object_just_port(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name, just_port=True))
        expected_returned = type(vhdl_obj())
        self.assertEqual(returned, expected_returned)

    #################
    ## Lib decode tests
    #################

    def test_decode_lib_type_list(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).lib)
        expected_returned = type([])
        self.assertEqual(returned, expected_returned)

    def test_decode_lib_type_list_of_strings(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).lib[0])
        expected_returned = type("Insert File path")
        self.assertEqual(returned, expected_returned)

    def test_decode_lib_no_spaces(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).lib
        space_found = False
        for lib in returned:
            if lib[0] == " " or lib[-1] == " ":
                space_found = True
        expected_returned = False
        self.assertEqual(space_found, expected_returned)

    def test_decode_lib_no_empty_list_elements(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).lib
        empty_element = False
        for lib in returned:
            if len(lib) == 0:
                empty_element = True
        expected_returned = False
        self.assertEqual(empty_element, expected_returned)

    def test_decode_lib_not_empty(self):
        file_name = "tests/test1.vhdl"
        returned = len((parse_vhdl(file_name).lib)) > 0
        expected_returned = True  # The returned list has data in it
        self.assertEqual(returned, expected_returned)

    # def test_decode_lib_correct_result(self):
    #     file_name = 'tests/test1.vhdl'
    #     returned = (parse_vhdl(file_name).lib)
    #     expected_returned =  ['ieee', 'ieee.std_logic_1164.all']
    #     self.assertEqual(returned, expected_returned)

    #################
    ## type decode tests
    #################

    def test_decode_type_list(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).type)
        expected_returned = type("Insert File path")
        self.assertEqual(returned, expected_returned)

    def test_decode_type_no_spaces(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).type
        space_found = False
        if " " in returned:
            space_found = True
        expected_returned = False
        self.assertEqual(space_found, expected_returned)

    def test_decode_type_not_empty(self):
        file_name = "tests/test1.vhdl"
        returned = len((parse_vhdl(file_name).type)) > 0
        expected_returned = True  # The returned string has data in it
        self.assertEqual(returned, expected_returned)

    #################
    ## data decode tests
    #################

    def test_decode_data_list(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).data)
        expected_returned = type("Insert File path")
        self.assertEqual(returned, expected_returned)

    def test_decode_data_no_spaces(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).data
        space_found = False
        if " " in returned:
            space_found = True
        expected_returned = False
        self.assertEqual(space_found, expected_returned)

    def test_decode_data_not_empty(self):
        file_name = "tests/test1.vhdl"
        returned = len((parse_vhdl(file_name).data)) > 0
        expected_returned = True  # The returned string has data in it
        self.assertEqual(returned, expected_returned)

    #################
    ## arch decode tests
    #################

    def test_decode_arch_list(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).arch)
        expected_returned = type("Insert File path")
        self.assertEqual(returned, expected_returned)

    def test_decode_arch_no_spaces(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).arch
        space_found = False
        if " " in returned:
            space_found = True
        expected_returned = False
        self.assertEqual(space_found, expected_returned)

    def test_decode_arch_not_empty(self):
        file_name = "tests/test1.vhdl"
        returned = len((parse_vhdl(file_name).arch)) > 0
        expected_returned = True  # The returned string has data in it
        self.assertEqual(returned, expected_returned)

    #################
    ## url decode tests
    #################

    def test_decode_url_list(self):
        file_name = "tests/test1.vhdl"
        returned = type(parse_vhdl(file_name).url)
        expected_returned = type("Insert File path")
        self.assertEqual(returned, expected_returned)

    def test_decode_url_no_spaces(self):
        file_name = "tests/test1.vhdl"
        returned = parse_vhdl(file_name).url
        space_found = False
        if " " in returned:
            space_found = True
        expected_returned = False
        self.assertEqual(space_found, expected_returned)

    def test_decode_url_not_empty(self):
        file_name = "tests/test1.vhdl"
        returned = len((parse_vhdl(file_name).url)) > 0
        expected_returned = True  # The returned string has data in it
        self.assertEqual(returned, expected_returned)


######

# Create a test suite and add the test classes
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(Test_Parse_VHDL_interface))

# Run the test suite
if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(test_suite)
