from graphsBuildingBlocks.graph import *
from availableGraphs.SSSP import Compute_SSSP
# from translatedGraphs.TriangleCounting import Compute_TC
# from translatedGraphs.v_cover import v_cover

# input in input.txt
# first line is max_node (0 to max_node inclusive)
# following lines are edges: src dest weight

filepath = r'./tests/inputs/input.txt'
my_graph = DirGraph(filepath)
my_graph.parseGraph()
src_node = 0
print(my_graph)

result = Compute_SSSP(my_graph, src_node)

print(result)