# A command line program for Comparing pins found in a VHDL file with those declared in an XDC file
# Arg 1 is the XDC file, Arg 2 is the Vhdl Top level file
# Robert D Jordan 2022

import sys
import re

with open(sys.argv[1]) as f: #import xdc file as string
    xdc = f.readlines()

# create lists for pin names and intermediate steps
pinPackages = []
pinNameFull = []
pinNameReduced = []
pinNameFinal = []
pinNameNoDup = []
XDCPinName = []

for i in xdc:
    if("PACKAGE_PIN" in i): # Find lines with "PINPACKAGE" in them
        pinPackages.append(i) #extract names between {} from XDC file

for i in pinPackages:  
    pinNameFull.append(re.findall(r'\{.*?\}', i))  #extract names between {} from XDC file

for i in pinNameFull:   
    pinNameReduced.append(re.sub("([\(\[]).*?([\)\]])","",i[0])) # remove everything between [] from XDC file (pin numbers)

for i in pinNameReduced:
    pinNameFinal.append( re.sub(r"[\([{})\]]", "", i)) # all bracket types from XDC file (extra formatting)

XDCPinName = [i for j, i in enumerate(pinNameFinal) if i not in pinNameFinal[:j]]  # remove duplicates

# print("Pin Names in XDC : " + str(XDCPinName)) # printing result

with open(sys.argv[2]) as f: #import xdc file as string
   vhd = f.readlines()

portStart = []
portEnd = []
portName = []
portNameFinal = []
commentedOut = []

# iterate through list of elements to find "port (" , the start of the port decleration and "end entity"
for i in vhd:
   
    if("port (" in i):
       
        # Find possible index for the start of port decleration
        portStart.append(vhd.index(i))

    if("end entity" in i):
       
        # Find possible index for the end of port decleration
        portEnd.append(vhd.index(i))

del vhd[portEnd[0]:len(vhd)] #remove from after port dec, do this first to preserve indexing
del vhd[0:portStart[0]] #remove from before port dec


# iterate through list of elements and if ":" extract up untill ":", which should be the port name
for i in vhd:
   
    if(":" in i):
        line = vhd.index(i) 
        match =  re.search(":", vhd[line]) 
        portName.append(i[0:match.start()])

for i in portName:  
    if("--" in i): # If line was comented out create a list of them
        commentedOut.append(re.sub(r'[- ]',"",i)) # remove extra characters and whitespace
    portNameFinal.append(re.sub(r'[- ]',"",i)) # remove extra characters and whitespace
  
      

#find ports/pins in XDC not in Vhd
inXDCNotVhd = list(set(XDCPinName)-set(portNameFinal))
#find ports/pins in VHD not in Xdc
inVhdNotXDC = list(set(portNameFinal)-set(XDCPinName))

# Mark all commented out signals
for i in inVhdNotXDC:
    if i in commentedOut:
        inVhdNotXDC[inVhdNotXDC.index(i)] = str(i + " * Commented Out")
     

print("**************************************************")
print("In XDC but NOT in Vhd:")
print(*inXDCNotVhd, sep = "\n")
print("**************************************************")
print("In Vhd but NOT in XDC:")
print(*inVhdNotXDC, sep = "\n")
print("**************************************************")
