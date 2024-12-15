import ast
import os
import sys
import time  # Importing the time module

# Define the ANSI escape code for colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

class PythonToStarPlatTranslator(ast.NodeVisitor):
    def __init__(self):
        self.dsl_code = []

    def visit_FunctionDef(self, node):
        self.dsl_code.append(f"function {node.name}(Graph g) {{\n")
        self.generic_visit(node)
        self.dsl_code.append("}\n")

    def visit_Assign(self, node):
        targets = [self.visit(t) for t in node.targets]
        value = self.visit(node.value)
        self.dsl_code.append(f"  long {targets[0]} = {value};\n")

    def visit_AugAssign(self, node):
        target = self.visit(node.target)
        op = self.visit(node.op)
        value = self.visit(node.value)
        self.dsl_code.append(f"  {target} {op} {value};\n")

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return str(node.value)

    def visit_For(self, node):
        target = self.visit(node.target)
        iter_call = self.visit(node.iter)
        self.dsl_code.append(f"  forall({target} in {iter_call}) {{\n")
        self.generic_visit(node)
        self.dsl_code.append("  }\n")

    def visit_If(self, node):
        test = self.visit(node.test)
        self.dsl_code.append(f"    if ({test}) {{\n")
        for stmt in node.body:
            self.visit(stmt)
        self.dsl_code.append("    }\n")

    def visit_Compare(self, node):
        left = self.visit(node.left)
        right = self.visit(node.comparators[0])
        op = self.visit(node.ops[0])
        return f"{left} {op} {right}"

    def visit_Lt(self, node):
        return "<"

    def visit_Gt(self, node):
        return ">"

    def visit_Call(self, node):
        func_name = self.visit(node.func)
        if func_name == "filter":
            lambda_func = self.visit(node.args[0])
            iter_call = self.visit(node.args[1])
            return f"{iter_call}.filter({lambda_func})"
        else:
            args = ", ".join(self.visit(arg) for arg in node.args)
            return f"{func_name}({args})"

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        attr = node.attr
        return f"{value}.{attr}"

    def visit_Lambda(self, node):
        return self.visit(node.body)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return f"{left} {op} {right}"

    def visit_Add(self, node):
        return "+"

    def visit_Return(self, node):
        value = self.visit(node.value)
        self.dsl_code.append(f"  return {value};\n")

    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

    def get_code(self):
        return "".join(self.dsl_code)

def translate_to_starplat(python_code):
    tree = ast.parse(python_code)
    translator = PythonToStarPlatTranslator()
    translator.visit(tree)
    return translator.get_code()

def main():
    start_time = time.time()  # Start timing

    # Check if a file path is provided
    if len(sys.argv) < 2:
        print(f"{RED}Usage: python translator.py <path_to_input_file>{NC}")
        return

    input_file = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"{RED}File '{input_file}' does not exist.{NC}")
        return

    # Read code from input file
    with open(input_file, "r") as file:
        python_code = file.read()

    # Translate the code
    dsl_code = translate_to_starplat(python_code)

    # Create the output directory if it doesn't exist
    os.makedirs('dslCodes', exist_ok=True)

    # Save the DSL code to a file in the output directory
    with open('dslCodes/triangleCountingDSL.txt', 'w') as file:
        file.write(dsl_code)

    end_time = time.time()  # End timing
    elapsed_time_microseconds = (end_time - start_time) * 1_000_000  # Calculate elapsed time in microseconds

    print(f"{GREEN}DSL code generated successfully!{NC}")
    print(f"{GREEN}Time taken: {elapsed_time_microseconds:.2f} microseconds{NC}")  # Print the time taken in microseconds

if __name__ == "__main__":
    main()