import sys
import os
import argparse
from token_test import parse_vhdl

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description='Signal Bundler: Bundles specified signals into a new bus.')
    parser.add_argument('vhdl_file', type=str, help='The VHDL file with signal definitions.')
    parser.add_argument('new_bus_name', type=str, help='The name of the new bundled signal.')
    parser.add_argument('signals_to_bundle', nargs='+', help='List of signals to bundle into the new bus.')

    args = parser.parse_args()

    # Extract arguments
    vhdl_file = args.vhdl_file
    new_bus_name = args.new_bus_name
    sigs_to_bundle = args.signals_to_bundle

    # Parse the VHDL file with the port/signal definitions we are interested in
    file1 = parse_vhdl(vhdl_file)

    collected_sigs = []

    # Collect signals from ports
    for sig in sigs_to_bundle:
        for port in file1.port:
            if port[0].lower() == sig.lower():
                collected_sigs.append(port)

    # Collect signals from signals
    for sig in sigs_to_bundle:
        for file_sig in file1.signal:
            if file_sig[0].lower() == sig.lower():
                collected_sigs.append(file_sig)

    # Change the order of the found signals/ports to match the requested signal order
    reordered = []
    for rew in sigs_to_bundle:
        for found_sig in collected_sigs:
            if rew.lower() == found_sig[0].lower():
                reordered.append(found_sig)

    # Calculate final bus width
    bundle_width = 0
    for sig in reordered:
        bundle_width += sig[3]

    # Define bundled signal
    str_out = f"signal {new_bus_name} : std_logic_vector({bundle_width-1} downto 0);\n\n"

    # Create assignments of signals to bundled signal
    counter = 0
    for sig in reordered:
        if sig[3] == 1:
            str_out += f"{new_bus_name}({counter})           <= {sig[0]};\n"
        else:
            str_out += f"{new_bus_name}({sig[3]-1 + counter} downto {counter}) <= {sig[0]};\n"
        counter += sig[3]

    print(f"Bundling {sigs_to_bundle} into new bus called {new_bus_name}...\n")
    print(str_out)
    print()

if __name__ == '__main__':
    main()
