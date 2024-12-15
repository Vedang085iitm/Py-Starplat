import ast
import os
import sys
import time  # Importing the time module

GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_ast_from_code(code):
    # Parse the code into an actual AST object
    parsed_ast = ast.parse(code)
    return parsed_ast

def translate_ast_to_code(parsed_ast):
    # Ensure the AST contains at least one node in the body
    if not isinstance(parsed_ast, ast.Module) or not parsed_ast.body:
        raise ValueError(f"The AST does not contain a valid Module or it is empty.")
    
    # Look for the first function definition in the AST
    function_def = None
    for node in parsed_ast.body:
        if isinstance(node, ast.FunctionDef):
            function_def = node
            break
        elif isinstance(node, ast.ClassDef):
            # If it's a class, look inside it for methods (which are functions)
            for class_body_node in node.body:
                if isinstance(class_body_node, ast.FunctionDef):
                    function_def = class_body_node
                    break
    
    if function_def is None:
        # Output detailed debugging information
        print(f"AST does not contain a direct function definition or a method within a class.")
        for node in parsed_ast.body:
            print(f"Node type found: {type(node).__name__}")
        raise ValueError(f"The AST does not contain a function definition.")
    
    # Extract the function name and arguments
    function_name = function_def.name
    args = [arg.arg for arg in function_def.args.args]
    
    # Start building the function code
    code = f"function {function_name}(Graph {args[0]}, float {args[1]}, float {args[2]}, int {args[3]}, propNode < float > pageRank) {{\n"
    code += f"  float num_nodes = {args[0]}.num_nodes();\n"
    code += "  propNode < float > pageRank_nxt;\n"
    code += f"  {args[0]}.attachNodeProperty(pageRank = 1 / num_nodes, pageRank_nxt = 0);\n"
    code += "  int iterCount = 0;\n"
    code += "  float diff;\n"
    code += "  do {\n"
    code += f"    forall(v in {args[0]}.nodes()) {{\n"
    code += "      float sum = 0.0;\n"
    code += f"      for (nbr in {args[0]}.nodes_to(v)) {{\n"
    code += f"        sum = sum + nbr.pageRank / {args[0]}.count_outNbrs(nbr);\n"
    code += "      }\n"
    code += f"      float val = (1 - {args[2]}) / num_nodes + {args[2]} * sum;\n"
    code += "      v.pageRank_nxt = val;\n"
    code += "    }\n"
    code += "    pageRank = pageRank_nxt;\n"
    code += "    iterCount++;\n"
    code += f"  }} while ((diff > {args[1]}) && (iterCount < {args[3]}));\n"
    code += "}\n"
    
    return code

if __name__ == "__main__":
    start_time = time.time()  # Record the start time
    
    if len(sys.argv) != 2:
        print(f"{RED}Usage: python translator.py <path_to_input_file>{NC}")
        sys.exit(1)
    
    python_file = sys.argv[1]
    code = read_code_from_file(python_file)
    
    # Generate the AST object from the code
    try:
        parsed_ast = generate_ast_from_code(code)
    except ValueError as e:
        print(f"{RED}Error parsing code to AST: {e}{NC}")
        sys.exit(1)
    
    # Translate the AST to code
    try:
        generated_code = translate_ast_to_code(parsed_ast)
    except ValueError as e:
        print(f"{RED}Error translating AST to code: {e}{NC}")
        sys.exit(1)
    
    # Create the output directory if it doesn't exist
    os.makedirs('dslCodes', exist_ok=True)
    
    # Save the DSL code to a file in the output directory
    with open('dslCodes/pageRankDSL.txt', 'w') as file:
        file.write(generated_code)
    
    end_time = time.time()  # Record the end time
    elapsed_time_microseconds = (end_time - start_time) * 1_000_000  # Calculate elapsed time in microseconds
    
    print(f"{GREEN}DSL code generated successfully!{NC}")
    print(f"{GREEN}Time taken: {elapsed_time_microseconds:.2f} microseconds{NC}")  # Print the time taken in microseconds