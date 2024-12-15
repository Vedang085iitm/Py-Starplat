import ast
import sys
import time
import os

def translate_ast_to_code(parsed_ast):
    # Ensure the AST contains at least one node in the body
    if not isinstance(parsed_ast, ast.Module) or not parsed_ast.body:
        raise ValueError("The AST does not contain a valid Module or it is empty.")
    
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
        raise ValueError("The AST does not contain a function definition.")
    
    # Extract the function name and arguments
    function_name = function_def.name
    args = [arg.arg for arg in function_def.args.args]
    
    # Check if the function has the required number of arguments
    if len(args) < 2:  # Ensure there are at least 2 arguments
        raise ValueError(f"The function '{function_name}' does not have the required 2 arguments.")
    
    # Start building the function code
    code = f"function {function_name}(Graph {args[0]}, node {args[1]}, propNode < int > distance, propEdge < int > weight){{\n"
    code += f"  {args[0]}.attachNodeProperty(distance = INF, modified = False);\n"
    code += f"  {args[0]}.modified = True;\n"
    code += f"  {args[0]}.distance[{args[1]}] = 0;\n"
    code += "  bool finished = False;\n"
    code += "  fixedPoint until(finished: !modified) {\n"
    code += f"    forall(v in {args[0]}.nodes()) {{\n"
    code += f"      forall(nbr in {args[0]}.neighbors(v).filter(modified == True)) {{\n"
    code += f"        edge e = {args[0]}.get_edge(v, nbr);\n"
    code += "        < nbr.distance, nbr.modified > = < Min(nbr.distance, v.distance + e.weight), True >;\n"
    code += "      }\n"
    code += "    }\n"
    code += "  }\n"
    code += "}\n"
    
    return code

if __name__ == "__main__":
    start_time = time.time()  # Record the start time
    
    if len(sys.argv) != 2:
        print("Usage: python translator.py <path_to_input_file>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    
    with open(input_file_path, 'r') as file:
        source_code = file.read()
    
    parsed_ast = ast.parse(source_code)
    generated_code = translate_ast_to_code(parsed_ast)
    
    if generated_code is None:
        print("Error: The generated code is None.")
        sys.exit(1)
    
    os.makedirs('dslCodes', exist_ok=True)
    
    # Save the DSL code to a file in the output directory
    with open('dslCodes/ssspDSL.txt', 'w') as file:
        file.write(generated_code)
   
    end_time = time.time()  # Record the end time
    elapsed_time_microseconds = (end_time - start_time) * 1_000_000  # Calculate elapsed time in microseconds
    
    print(f"Time taken: {elapsed_time_microseconds:.2f} microseconds")  # Print the time taken in microseconds