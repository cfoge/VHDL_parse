from token_test import *
import pickle


def test_file(file_name):
    vhdl_as_obj = parse_vhdl("tests/" + file_name + ".vhdl")

    # Save a test object if it is correct!!!
    with open(f"test_vectors/{file_name}.vhdlobj", "wb") as test_file:
        pickle.dump(vhdl_as_obj, test_file)


# assignement errors may not be triggered?
# diff_object = test_file("test1")
# diff_object = test_file("test2")
# diff_object = test_file("test3")
# diff_object = test_file("test4")
# diff_object = test_file("test5")
# diff_object = test_file("test6") # correct but doesnt recognise types, will classify a signal that is a type as null for both type and size
# diff_object = test_file("test7")
# diff_object = test_file("test8")
diff_object = test_file("AlphaBlend")

# somthing is up with the tests it is not recognising types of changes
# script doesnt recognise := after signals and maybe ports and constants
print("")
