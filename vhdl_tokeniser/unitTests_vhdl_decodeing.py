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
        expected_result = self.expected_result[19]  
        returned_result = len(parse_vhdl(self.file_name).nonSynth)
        self.assertEqual(returned_result, expected_result)
    
    def test_nonSynth_return_content_correct(self):
        # Override the file name and expected result for this specific test
        test = returned_result = parse_vhdl(self.file_name)
        expected_result = self.expected_result[20]  
        returned_result = parse_vhdl(self.file_name).nonSynth
        self.assertEqual(returned_result, expected_result)

    def test_func_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[21]  
        returned_result = len(parse_vhdl(self.file_name).func)
        self.assertEqual(returned_result, expected_result)
    
    def test_func_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[22]  
        returned_result = parse_vhdl(self.file_name).func
        self.assertEqual(returned_result, expected_result)

    def test_generate_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[23]  
        returned_result = len(parse_vhdl(self.file_name).generate)
        self.assertEqual(returned_result, expected_result)
    
    def test_generate_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[24]  
        returned_result = parse_vhdl(self.file_name).generate
        self.assertEqual(returned_result, expected_result)

    def test_generic_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[25]  
        returned_result = len(parse_vhdl(self.file_name).generic)
        self.assertEqual(returned_result, expected_result)
    
    def test_generic_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[26]  
        returned_result = parse_vhdl(self.file_name).generic
        self.assertEqual(returned_result, expected_result)

    def test_process_return_length_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[27]  
        returned_result = len(parse_vhdl(self.file_name).process)
        self.assertEqual(returned_result, expected_result)
    
    def test_process_return_content_correct(self):
        # Override the file name and expected result for this specific test
        expected_result = self.expected_result[28]  
        returned_result = parse_vhdl(self.file_name).process
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
    # suite.addTest(TestParseVHDLDecoding('test_signal_return_length_correct', file_name=file_name, expected_result=expected_result))
    # suite.addTest(TestParseVHDLDecoding('test_signal_return_content_correct', file_name=file_name, expected_result=expected_result))
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
    suite.addTest(TestParseVHDLDecoding('test_generic_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_generic_return_content_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_process_return_length_correct', file_name=file_name, expected_result=expected_result))
    suite.addTest(TestParseVHDLDecoding('test_process_return_content_correct', file_name=file_name, expected_result=expected_result))




    return suite

if __name__ == '__main__':
    # Pass variables from the main function
    file_name_main = 'tests/test1.vhdl'
    expected_result_main = ["full_adder_structural_vhdl",
                            2, ['ieee', 'ieee.std_logic_1164.all'], 
                            5, [['x1', 'in', 'std_logic', 1, None],['x2', 'in', 'std_logic', 1, None],['cin', 'in', 'std_logic', 1, None],['s', 'out', 'std_logic', 1, None],['cout', 'out', 'std_logic', 1, None]],
                            3, [['a1', '', 'std_logic', 1, None],['a2', '', 'std_logic', 1, None],['a3', '', 'std_logic', 1, None]],
                            5, [['a1', 'x1 xor x2'],  ['a2', 'x1 and x2'],  ['a3', 'a1 and cin'],  ['cout', 'a2 or a3'],  ['s', 'a1 xor cin']],
                            10, "structural", #arch
                            0, [], #constant
                            3, [['a1', '', 'std_logic', 1, None],['a2', '', 'std_logic', 1, None],['a3', '', 'std_logic', 1, None]],
                            0, [], #subtype
                            0, [],  # typedec
                            0, [], #nonsynth 
                            0, [], #func
                            0, [], #generate
                            0, [] , #generic
                            0, [] #process
                            ]
    
    file_name_main2 = 'tests/test2.vhdl'
    expected_result_main2 = ["comparator",
                            2, ['ieee', 'ieee.std_logic_1164.all'], #lib
                            5,  [['clock', 'in', 'std_logic', 1, None], ['a', 'in', 'std_logic_vector', 8, None], ['b', 'in', 'std_logic_vector', 8, None], ['iab', 'in', 'std_logic', 1, None], ['output', 'out', 'std_logic', 1, None]], #port
                            None, [], #sig
                            #assign is worng is missing  Output <= Result;
                            8, [['ab(0)', '(not a(0)) xnor (not b(0))'],  ['ab(1)', '(not a(1)) xnor (not b(1))'],  ['ab(2)', '(not a(2)) xnor (not b(2))'],  ['ab(3)', '(not a(3)) xnor (not b(3))'],  ['ab(4)', '(not a(4)) xnor (not b(4))'],  ['ab(5)', '(not a(5)) xnor (not b(5))'],  ['ab(6)', '(not a(6)) xnor (not b(6))'],  ['ab(7)', '(not a(7)) xnor (not b(7))'], ['output','result']], #assign
                            10, "behavioral",
                            0, [], #constant
                            2, [['ab', '', 'std_logic_vector', 8, None], ['result', '', 'std_logic', 1, None]] , #signal 
                            0, [], #subtype
                            0, [],  # typedec
                            0, [], #nonsynth 
                            0, [], #func
                            0, [], #generate
                            0, [] , #generic
                            1, [['Unnammed', 'clock', [['result', "'0'"], ['result', "'1'"]]]] #process
                            ]
    
    file_name_main3 = 'tests/test3.vhdl'
    expected_result_main3 = ["traffic_light_controller",
                            3, ['ieee', 'ieee.std_logic_1164.all','ieee.std_logic_unsigned.all'], #lib  
                            5,  [['sensor', 'in', 'std_logic', 1, None], ['clk', 'in', 'std_logic', 1, None], ['rst_n', 'in', 'std_logic', 1, None], ['light_highway', 'out', 'std_logic_vector', 3, None], ['light_farm', 'out', 'std_logic_vector', 3, None]], #port
                            12,  [['counter_1s', '', 'std_logic_vector', 28, 'x"0000000"'],  ['delay_count', '', 'std_logic_vector', 4, 'x"0"'],  ['delay_10s', '', 'std_logic', 1, 0],  ['delay_3s_f', '', 'std_logic', 1, 0],  ['delay_3s_h', '', 'std_logic', 1, 0],  ['red_light_enable', '', 'std_logic', 1, 0],  ['yellow_light1_enable', '', 'std_logic', 1, 0],  ['yellow_light2_enable', '', 'std_logic', 1, 0],  ['clk_1s_enable', '', 'std_logic', 1, None],  ['current_state', '', 'null', 'null', None],  ['next_state', '', 'null', 'null', None]], #sig
                            ####
                            11, [['ab(0)', '(not a(0)) xnor (not b(0))'],  ['ab(1)', '(not a(1)) xnor (not b(1))'],  ['ab(2)', '(not a(2)) xnor (not b(2))'],  ['ab(3)', '(not a(3)) xnor (not b(3))'],  ['ab(4)', '(not a(4)) xnor (not b(4))'],  ['ab(5)', '(not a(5)) xnor (not b(5))'],  ['ab(6)', '(not a(6)) xnor (not b(6))'],  ['ab(7)', '(not a(7)) xnor (not b(7))']], #assign
                            13, "traffic_light",
                            0, [], #constant
                            11, [] , #signal 
                            0, [], #subtype
                            1, [],  # typedec
                            0, [], #nonsynth 
                            0, [], #func
                            0, [], #generate
                            0, [] , #generic
                            4, [] #process
                            ]
    


    


  

        # self.primitives = []
        # self.modname = ''
        # self.url = ''


    # Create a custom test suite and run it
    suite = custom_test_suite_full(file_name_main, expected_result_main)
    print(f"Testing with {file_name_main}")
    unittest.TextTestRunner(verbosity=2).run(suite)
    ####
    suite2 = custom_test_suite_full(file_name_main2, expected_result_main2)
    print(f"Testing with {file_name_main2}")
    unittest.TextTestRunner(verbosity=2).run(suite2)
    ####
    suite3 = custom_test_suite_full(file_name_main3, expected_result_main3)
    print(f"Testing with {file_name_main3}")
    unittest.TextTestRunner(verbosity=2).run(suite3)
