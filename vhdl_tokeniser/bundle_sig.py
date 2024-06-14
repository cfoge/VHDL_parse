# signal bundler, takes posts and signals and creates a new bus consisting of other signals
# needs arg interface


import sys
from token_test import *
import os
import argparse

new_bus_name = 'Bundled'
sigs_to_bundle = ['slaveAddr','sda','dataIn','scl']
# parse the vhdl file with the port/signal definitons we are interested in
file1 = parse_vhdl("vhdl_tokeniser/tests/test5.vhdl") 

collected_sigs = []

for sig in  sigs_to_bundle:
    for port in file1.port:
        if port[0].lower() == sig.lower():
            collected_sigs.append(port)

for sig in  sigs_to_bundle:
    for file_sig in file1.signal:
        if file_sig[0].lower() == sig.lower():
            collected_sigs.append(file_sig)

# change the order of the found signals/ports to match the requested signal order
reordered = []
for rew in sigs_to_bundle:
    for found_sig in collected_sigs:
        if rew.lower() == found_sig[0].lower():
           reordered.append(found_sig)


#calc final bus width
bundle_width = 0
for sig in reordered:
    bundle_width = bundle_width + sig[3]

# define bundled signal
str_out = f"signal {new_bus_name} : std_logic_vector({bundle_width-1} downto 0);\n\n"

# create assignments of signals to bundled signal
counter = 0
space = ' '
for sig in reordered:
    if sig[3] == 1:
        str_out = str_out + f"{new_bus_name}({counter})           <= {sig[0]};\n"

    else:
       str_out = str_out + f"{new_bus_name}({sig[3]-1 + counter} down to {counter}) <= {sig[0]};\n"
    counter = counter + sig[3]

print(f"Bundaling {sigs_to_bundle} into new bus called {new_bus_name}...")
print()
print(str_out)
print()