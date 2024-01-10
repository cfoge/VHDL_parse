import unittest
from token_test import parse_vhdl

class TestParseVHDLDecoding(unittest.TestCase):

    def __init__(self, methodName='runTest', file_name='', expected_result=None):
        super().__init__(methodName)
        self.file_name = file_name
        self.expected_result = expected_result

    def test_data_return_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[0]  
        returned_result = parse_vhdl(self.file_name).data
        self.assertEqual(returned_result, expected_result)

    def test_lib_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[1]  
        returned_result = len(parse_vhdl(self.file_name).lib)
        self.assertEqual(returned_result, expected_result)
    
    def test_lib_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[2]  
        returned_result = parse_vhdl(self.file_name).lib
        self.assertEqual(returned_result, expected_result)

    def test_port_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[3]  
        returned_result = len(parse_vhdl(self.file_name).port)
        self.assertEqual(returned_result, expected_result)
    
    def test_port_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[4]  
        returned_result = parse_vhdl(self.file_name).port
        self.assertEqual(returned_result, expected_result)

    def test_signal_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[5]  
        returned_result = len(parse_vhdl(self.file_name).signal)
        self.assertEqual(returned_result, expected_result)
    
    def test_signal_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[6]  
        returned_result = parse_vhdl(self.file_name).signal
        self.assertEqual(returned_result, expected_result)

    def test_assign_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[7]  
        returned_result = len(parse_vhdl(self.file_name).assign)
        self.assertEqual(returned_result, expected_result)
    
    def test_assign_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[8]  
        returned_result = parse_vhdl(self.file_name).assign
        self.assertEqual(returned_result, expected_result)

    def test_arch_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[9]  
        returned_result = len(parse_vhdl(self.file_name).arch)
        self.assertEqual(returned_result, expected_result)
    
    def test_arch_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[10]  
        returned_result = parse_vhdl(self.file_name).arch
        self.assertEqual(returned_result, expected_result)

    def test_constant_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[11]  
        returned_result = len(parse_vhdl(self.file_name).constant)
        self.assertEqual(returned_result, expected_result)
    
    def test_constant_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[12]  
        returned_result = parse_vhdl(self.file_name).constant
        self.assertEqual(returned_result, expected_result)

    def test_signal_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[13]  
        returned_result = len(parse_vhdl(self.file_name).signal)
        self.assertEqual(returned_result, expected_result)
    
    def test_signal_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[14]  
        returned_result = parse_vhdl(self.file_name).signal
        self.assertEqual(returned_result, expected_result)

    def test_subtype_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[15]  
        returned_result = len(parse_vhdl(self.file_name).subtype)
        self.assertEqual(returned_result, expected_result)
    
    def test_subtype_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[16]  
        returned_result = parse_vhdl(self.file_name).subtype
        self.assertEqual(returned_result, expected_result)

    def test_type_dec_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[17]  
        returned_result = len(parse_vhdl(self.file_name).type_dec)
        self.assertEqual(returned_result, expected_result)
    
    def test_type_dec_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[18]  
        returned_result = parse_vhdl(self.file_name).type_dec
        self.assertEqual(returned_result, expected_result)




    def test_nonSynth_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[17]  
        returned_result = len(parse_vhdl(self.file_name).nonSynth)
        self.assertEqual(returned_result, expected_result)
    
    def test_nonSynth_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[18]  
        returned_result = parse_vhdl(self.file_name).nonSynth
        self.assertEqual(returned_result, expected_result)

    def test_func_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[19]  
        returned_result = len(parse_vhdl(self.file_name).func)
        self.assertEqual(returned_result, expected_result)
    
    def test_func_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[20]  
        returned_result = parse_vhdl(self.file_name).func
        self.assertEqual(returned_result, expected_result)





    def test_generate_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[19]  
        returned_result = len(parse_vhdl(self.file_name).generate)
        self.assertEqual(returned_result, expected_result)
    
    def test_generate_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[20]  
        returned_result = parse_vhdl(self.file_name).generate
        self.assertEqual(returned_result, expected_result)

def custom_test_suite_full(file_name, expected_result):
    suite = unittest.TestSuite()
    suite.addTest(TestParseVHDLDecoding('test_data_return_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_lib_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_lib_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_port_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_port_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_signal_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_signal_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_assign_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_assign_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_arch_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_arch_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_constant_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_constant_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_signal_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_signal_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_subtype_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_subtype_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_type_dec_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_type_dec_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_nonSynth_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_nonSynth_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_func_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_func_return_content_correct', file_name=file_name, expected_result=expected_result))

    suite.addTest(TestParseVHDLDecoding('test_generate_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_generate_return_content_correct', file_name=file_name, expected_result=expected_result))



    return suite

if __name__ == '__main__':
    # Pass variables from the main function
    file_name_main = 'tests/test1.vhdl'
    expected_result_main = ["full_adder_structural_vhdl",
                            2, ['ieee', 'ieee.std_logic_1164.all'], 
                            5, [['x1', 'in', 'std_logic', 1, None],['x2', 'in', 'std_logic', 1, None],['cin', 'in', 'std_logic', 1, None],['s', 'out', 'std_logic', 1, None],['cout', 'out', 'std_logic', 1, None]],
                            3, [['a1', '', 'std_logic', 1, None],['a2', '', 'std_logic', 1, None],['a3', '', 'std_logic', 1, None]],
                            5, [['a1', 'x1 xor x2'],  ['a2', 'x1 and x2'],  ['a3', 'a1 and cin'],  ['cout', 'a2 or a3'],  ['s', 'a1 xor cin']],
                            10, "structural",
                            0, [],
                            3, [['a1', '', 'std_logic', 1, None],['a2', '', 'std_logic', 1, None],['a3', '', 'std_logic', 1, None]],
                            0, [],
                            0, [],
                            0, [],
                            0, [],
                            0, []
                            ]
    


  

        # self.primitives = []
        # self.modname = ''
        # self.url = ''
    file_name_main2 = 'tests/test7.vhdl'
    expected_result_main2 = ["pia8255", 
                            4, ['ieee', 'ieee.std_logic_1164.all','ieee.std_logic_unsigned.all','ieee.numeric_std.all'], 
                            19, [],
                            47, [],
                            0, []
                            ]

    # Create a custom test suite and run it
    suite = custom_test_suite_full(file_name_main, expected_result_main)
    print(f"Testing with {file_name_main}")
    unittest.TextTestRunner(verbosity=2).run(suite)
    # suite2 = custom_test_suite_full(file_name_main2, expected_result_main2)
    # print(f"Testing with {file_name_main2}")
    # unittest.TextTestRunner(verbosity=2).run(suite2)
