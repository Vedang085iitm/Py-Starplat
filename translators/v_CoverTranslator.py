import ast
import sys
import os
import time  # Importing the time module

GREEN = '\033[0;32m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

class ASTToCustomTranslator(ast.NodeVisitor):
    def __init__(self):
        self.translated_code = []

    def translate(self, python_code):
        tree = ast.parse(python_code)
        self.visit(tree)
        return "".join(self.translated_code)

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def visit_FunctionDef(self, node):
        self.translated_code.append(f"function {node.name}(Graph g)\n{{\n")
        self.generic_visit(node)
        self.translated_code.append("}\n")

    def visit_Assign(self, node):
        targets = [self.visit(t) for t in node.targets]
        value = self.visit(node.value)
        if any(target in ["vc[v]", "vc[nbr]"] for target in targets) and value == "True":
            return
        if "propNode" in value:
            self.translated_code.append(f"    {value};\n")
        elif "attachNodeProperty" in value:
            self.translated_code.append(f"    g.attachNodeProperty(visited = False);\n")
        else:
            self.translated_code.append(f"    {targets[0]} = {value};\n")

    def visit_Expr(self, node):
        value = self.visit(node.value)
        if "attachNodeProperty" in value:
            self.translated_code.append(f"    g.attachNodeProperty(visited = False);\n")
        else:
            self.translated_code.append(f"    {value};\n")

    def visit_Call(self, node):
        func_name = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        if func_name == "type":
            return f"propNode<bool> visited"
        elif func_name == "filter":
            return f"g.nodes().filter({args[0]})"
        return f"{func_name}({', '.join(args)})"

    def visit_For(self, node):
        target = self.visit(node.target)
        iter = self.visit(node.iter)
        if "filter" in iter:
            self.translated_code.append(f"    forall({target} in {iter}){{\n")
        else:
            self.translated_code.append(f"    for({target} in {iter}){{\n")
        self.generic_visit(node)
        self.translated_code.append("    }\n")

    def visit_If(self, node):
        test = self.visit(node.test)
        if "g.visited[nbr]" in test:
            test = test.replace("g.visited[nbr]", "nbr.visited")
        self.translated_code.append(f"        if({test}){{\n")
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                targets = [self.visit(t) for t in stmt.targets]
                value = self.visit(stmt.value)
                if any(target in ["vc[v]", "vc[nbr]"] for target in targets) and value == "True":
                    continue
                if "g.visited[nbr]" in targets[0]:
                    targets[0] = targets[0].replace("g.visited[nbr]", "nbr.visited")
                if "g.visited[v]" in targets[0]:
                    targets[0] = targets[0].replace("g.visited[v]", "v.visited")
                self.translated_code.append(f"            {targets[0]} = {value};\n")
            else:
                self.visit(stmt)
        self.translated_code.append("        }\n")

    def visit_Return(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'vc':
            return
        value = self.visit(node.value)
        self.translated_code.append(f"  return {value};\n")

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return repr(node.value)

    def visit_Attribute(self, node):
        value = self.visit(node.value)
        return f"{value}.{node.attr}"

    def visit_Subscript(self, node):
        value = self.visit(node.value)
        slice = self.visit(node.slice)
        return f"{value}[{slice}]"

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_Lambda(self, node):
        args = [self.visit(arg) for arg in node.args.args]
        if not args:
            return "False"
        body = self.visit(node.body)
        return f"visited == False"

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.Not):
            return f"{operand} == False"
        return f"{node.op}{operand}"

    def visit_Compare(self, node):
        left = self.visit(node.left)
        comparators = [self.visit(comp) for comp in node.comparators]
        if isinstance(node.ops[0], ast.Is):
            return f"{left} == {comparators[0]}"
        return f"{left} {node.ops[0]} {comparators[0]}"

    def visit_BoolOp(self, node):
        values = [self.visit(value) for value in node.values]
        if isinstance(node.op, ast.And):
            return " and ".join(values)
        elif isinstance(node.op, ast.Or):
            return " or ".join(values)
        return f"{node.op}({', '.join(values)})"

    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            self.visit(child)

# Example usage:

def main():
    start_time = time.time()  # Record the start time
    
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
    translator = ASTToCustomTranslator()
    custom_code = translator.translate(python_code)

    # Create the output directory if it doesn't exist
    os.makedirs('dslCodes', exist_ok=True)
    
    # Save the DSL code to a file in the output directory
    with open('dslCodes/v_CoverDSL.txt', 'w') as file:
        file.write(custom_code)
    
    end_time = time.time()  # Record the end time
    elapsed_time_microseconds = (end_time - start_time) * 1_000_000  # Calculate elapsed time in microseconds
    
    print(f"{GREEN}DSL code generated successfully!{NC}")
    print(f"{GREEN}Time taken: {elapsed_time_microseconds:.2f} microseconds{NC}")  # Print the time taken in microseconds

if __name__ == "__main__":
    main()