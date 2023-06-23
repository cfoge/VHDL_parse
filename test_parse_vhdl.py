from parse_vhdl import *
import pickle

def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
            
    return li_dif

def show_dif(self, other): # != operator returns the differences as a string
        if(self.data == other.data):
            name = "name match"
        else:
            name = "name no match"

        diff_obj = vhdl_obj()
        diff_obj.data.append(name)
        diff_obj.generic.append(diff(self.generic,other.generic))
        diff_obj.port.append(diff(self.port,other.port))
        diff_obj.children.append(diff(self.children,other.children))
        #diff_obj.component.append(diff(self.component,other.component)) # these are objects, i need to go through them and compare the diff in the contents
        diff_obj.attribute.append(diff(self.attribute,other.attribute))
        diff_obj.constant.append(diff(self.constant,other.constant))
        diff_obj.process.append(diff(self.process,other.process))
        diff_obj.signal.append(diff(self.signal,other.signal))

        return diff_obj

def test_file(file_name):
    vhdl_as_obj = parse_vhdl("tests/"+file_name +".vhdl")

# Save a test object if it is correct!!!
#     with open('test3.vhdlobj', 'wb') as test_file:
#       pickle.dump(vhdl_as_obj, test_file)

# load a test object with the same name as our test file
    with open('tests/' +file_name +'.vhdlobj', 'rb') as test_file:
        test_obj = pickle.load(test_file) 
    file1 = vhdl_as_obj
    file2 = test_obj
    diff_obj = show_dif(file1,file2)


    

    if len(diff_obj.generic[0]) != 0:
         print("test: " + file_name + " Failed! = generic")
    if len(diff_obj.port[0]) !=0:
         print("test: " + file_name + " Failed! = port")
    if len(diff_obj.children[0])!=0:
         print("test: " + file_name + " Failed! = childeren")
    if len(diff_obj.attribute[0])!=0:
         print("test: " + file_name + " Failed! = attribute")
    if len(diff_obj.lib)!=0:
         print("test: " + file_name + " Failed! = lib")
    if len(diff_obj.constant[0])!=0:
         print("test: " + file_name + " Failed! = constant")
    if len(diff_obj.assign)!=0:
         print("test: " + file_name + " Failed! = assignments")
    if len(diff_obj.process[0])!=0:
         print("test: " + file_name + " Failed! = process")
    if len(diff_obj.signal[0])!=0:
         print("test: " + file_name + " Failed! = signal")
    return diff_obj

# assignement errors may not be triggered?
# diff_object = test_file("test1")
# diff_object = test_file("test2")
# diff_object = test_file("test3")
diff_object = test_file("test4") # missed 2nd generic, missed second port, thinks it is a child
print("")