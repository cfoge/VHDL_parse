import argparse

# Define VHDL types and their corresponding formats
VHDL_TYPES = {
    "logic": "std_logic",
    "vec": "std_logic_vector",
    "sig": "signed",
    "un": "unsigned",
    "int": "integer",
    "bool": "boolean"
}

def create_signal(signal_name, signal_type="logic", width=None):
    if signal_type not in VHDL_TYPES:
        raise ValueError(f"Unsupported VHDL type: {signal_type}")

    vhdl_type = VHDL_TYPES[signal_type]

    if vhdl_type == "integer":
        return f"signal {signal_name:<15} : integer;"
    elif vhdl_type == "boolean":
        return f"signal {signal_name:<15} : boolean;"
    elif vhdl_type in ["std_logic_vector", "signed", "unsigned"]:
        if width is None:
            raise ValueError(f"Width must be specified for type {vhdl_type}")
        return f"signal {signal_name:<15} : {vhdl_type}({width - 1} downto 0);"
    else:  # Default is std_logic
        return f"signal {signal_name:<15} : {vhdl_type};"

def main():
    parser = argparse.ArgumentParser(description="Generate VHDL signals.")
    parser.add_argument("signals", nargs="+", help="Signal definitions in the format 'name [type] [width]'")
    args = parser.parse_args()
    
    signal_definitions = []

    for signal in args.signals:
        parts = signal.split()
        signal_name = parts[0]
        
        if len(parts) == 1:
            signal_definitions.append(create_signal(signal_name))
        elif len(parts) == 2:
            signal_param = parts[1]
            if signal_param.isdigit():
                width = int(signal_param)
                signal_definitions.append(create_signal(signal_name, "vec", width=width))
            else:
                signal_type = signal_param
                signal_definitions.append(create_signal(signal_name, signal_type=signal_type))
        elif len(parts) == 3:
            signal_type = parts[1]
            width = int(parts[2])
            signal_definitions.append(create_signal(signal_name, signal_type=signal_type, width=width))
        else:
            print(f"Invalid signal format: {signal}")
            exit(1)

    for definition in signal_definitions:
        print(definition)

if __name__ == "__main__":
    main()
