import re
import sys

def extract_wire_connections(verilog_code):
    connections = {}
    inside_module = False
    current_instance = None

    # Updated pattern to match non-parameterized module instantiations
    module_inst_pattern = re.compile(r'\b(\w+)\s+(\w+)\s*\(')
    wire_pattern = re.compile(r'\s*\.\w+\s*\(\s*(\w+)(\s*\[\d+:\d+\])?\s*\)\s*,?')

    found_modules = []

    for line in verilog_code.split('\n'):
        module_inst_match = module_inst_pattern.search(line)
        if module_inst_match:
            current_instance = module_inst_match.group(2)  # Capture the instance name
            found_modules.append(module_inst_match.group(1))  # Capture the module name
            inside_module = True
            continue
        
        if inside_module and wire_pattern.search(line):
            wire_match = wire_pattern.search(line)
            if wire_match:
                wire_name = wire_match.group(1).strip()
                if wire_name not in connections:
                    connections[wire_name] = []
                connections[wire_name].append(current_instance)
        
        if inside_module and line.strip() == ');':
            inside_module = False

    return connections, found_modules

def annotate_wire_declarations(verilog_code, connections):
    output_lines = []
    inside_module = False
    current_instance = None

    module_inst_pattern = re.compile(r'\b(\w+)\s+(\w+)\s*\(')
    wire_pattern = re.compile(r'(\s*\.\w+)\s*\(\s*(\w+)(\s*\[\d+:\d+\])?\s*\)\s*,?')
    parameter_pattern = re.compile(r'^\s*\.PARAM\S*\s*\(')

    for line in verilog_code.split('\n'):
        module_inst_match = module_inst_pattern.search(line)
        if module_inst_match:
            current_instance = module_inst_match.group(2)
            inside_module = True
            output_lines.append(line)
            continue

        if inside_module and wire_pattern.search(line) and not parameter_pattern.match(line):
            wire_match = wire_pattern.search(line)
            if wire_match:
                port_name = wire_match.group(1).strip()
                wire_name = wire_match.group(2).strip()
                bit_range = wire_match.group(3) if wire_match.group(3) else ''
                if wire_name in connections:
                    connected_instances = [inst for inst in connections[wire_name] if inst != current_instance]
                    comment = f'  // {current_instance}'
                    if connected_instances:
                        comment += f', {", ".join(connected_instances)}'
                    output_lines.append(f'{line.strip()}{comment}')
            else:
                output_lines.append(line)
        else:
            output_lines.append(line)
            if inside_module and line.strip() == ');':
                inside_module = False

    return '\n'.join(output_lines)

def process_verilog_file(input_file, output_file):
    with open(input_file, 'r') as f:
        verilog_code = f.read()

    connections, found_modules = extract_wire_connections(verilog_code)
    
    # Print all found modules
    print("Found modules:")
    for module in found_modules:
        print(module)
    
    annotated_code = annotate_wire_declarations(verilog_code, connections)
    
    with open(output_file, 'w') as f:
        f.write(annotated_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_verilog_file(input_file, output_file)
