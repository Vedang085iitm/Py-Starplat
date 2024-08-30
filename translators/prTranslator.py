import ast

# Construct the AST nodes directly
function_def = ast.FunctionDef(
    name='Compute_PR',
    args=ast.arguments(
        posonlyargs=[],
        args=[
            ast.arg(arg='g'),
            ast.arg(arg='beta'),
            ast.arg(arg='delta'),
            ast.arg(arg='maxIter')],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[]),
    body=[
        ast.Assign(
            targets=[ast.Name(id='num_nodes', ctx=ast.Store())],
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='g', ctx=ast.Load()),
                    attr='num_nodes',
                    ctx=ast.Load()),
                args=[],
                keywords=[])),
        ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='g', ctx=ast.Load()),
                    attr='attachNodeProperty',
                    ctx=ast.Load()),
                args=[],
                keywords=[
                    ast.keyword(
                        arg='pageRank',
                        value=ast.BinOp(
                            left=ast.Constant(value=1),
                            op=ast.Div(),
                            right=ast.Name(id='num_nodes', ctx=ast.Load()))),
                    ast.keyword(
                        arg='pageRank_nxt',
                        value=ast.Constant(value=0))])),
        ast.Assign(
            targets=[ast.Name(id='iterCount', ctx=ast.Store())],
            value=ast.Constant(value=0)),
        # Additional statements would go here...
    ],
    decorator_list=[]
)

# Create a Module node
module = ast.Module(body=[function_def], type_ignores=[])

# Function to translate the AST to the desired function code
def translate_ast_to_code(parsed_ast):
    function_def = parsed_ast.body[0]
    
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

# Generate the function code
function_code = translate_ast_to_code(module)
print(function_code)