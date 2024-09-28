import ast
import pprint
import os
import sys

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_script.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    code = read_code_from_file(input_file)
    
    # Parse the code into an AST
    parsed_code = ast.parse(code)
    
    # Pretty print the AST
    ast_dump = pprint.pformat(ast.dump(parsed_code, indent=4))
    
    # Ensure the ASTs directory exists
    os.makedirs('ASTs', exist_ok=True)
    
    # Extract the base name of the input file (without the extension)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # Create the output file name
    output_file = f'ASTs/{base_name}_ast.txt'
    
    # Write the AST dump to the output file
    with open(output_file, 'w') as f:
        f.write(ast_dump)