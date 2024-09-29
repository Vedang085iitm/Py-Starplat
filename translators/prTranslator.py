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
    # Commented out the AST printing for debugging
    # print(ast.dump(parsed_ast, indent=4))
    
    # Ensure the AST contains at least one node in the body
    if not isinstance(parsed_ast, ast.Module) or not parsed_ast.body:
        raise ValueError(f"{RED}The AST does not contain a valid Module or it is empty.{NC}")
    
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
        print(f"{RED}AST does not contain a direct function definition or a method within a class.{NC}")
        for node in parsed_ast.body:
            print(f"{RED}Node type found: {type(node).__name__}{NC}")
        raise ValueError(f"{RED}The AST does not contain a function definition.{NC}")
    
    # Extract the function name and arguments
    function_name = function_def.name
    args = [arg.arg for arg in function_def.args.args]
    
    # Start building the function code
    code = f"function {function_name}(Graph {args[0]}, float {args[1]}, float {args[2]}, int {args[3]}, propNode < float > pageRank) {{\n"
    code += "  float num_nodes = g.num_nodes();\n"
    code += "  propNode < float > pageRank_nxt;\n"
    code += "  g.attachNodeProperty(pageRank = 1 / num_nodes, pageRank_nxt = 0);\n"
    code += "  int iterCount = 0;\n"
    code += "  float diff;\n"
    code += "  do {\n"
    code += "    forall(v in g.nodes()) {\n"
    code += "      float sum = 0.0;\n"
    code += "      for (nbr in g.nodes_to(v)) {\n"
    code += "        sum = sum + nbr.pageRank / g.count_outNbrs(nbr);\n"
    code += "      }\n"
    code += "      float val = (1 - delta) / num_nodes + delta * sum;\n"
    code += "      v.pageRank_nxt = val;\n"
    code += "    }\n"
    code += "    pageRank = pageRank_nxt;\n"
    code += "    iterCount++;\n"
    code += "  } while ((diff > beta) && (iterCount < maxIter));\n"
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
    os.makedirs('output', exist_ok=True)
    
    # Save the DSL code to a file in the output directory
    with open('output/pageRankDSL.txt', 'w') as file:
        file.write(generated_code)
    
    end_time = time.time()  # Record the end time
    elapsed_time_microseconds = (end_time - start_time) * 1_000_000  # Calculate elapsed time in microseconds
    
    print(f"{GREEN}DSL code generated successfully!{NC}")
    print(f"{GREEN}Time taken: {elapsed_time_microseconds:.2f} microseconds{NC}")  # Print the time taken in microseconds