from math import inf
from constructs.FixedPointUntil import FixedPointUntil
from constructs.FixedPoint import FixedPoint

def Compute_SSSP(G, src_node):
    G.attachNodeProperty(distance=inf, modified=False, modified_next=False)
    G.modified[src_node] = True
    G.distance[src_node] = 0

    # finished = False
    
    def condition():
        finished = True
        for v in G.modified.values():
            finished = finished and (not v)
        
        return finished
    
    with FixedPointUntil(condition) as loop:
        
        def block():

            for v in filter(lambda node: G.modified[node] == True, G.nodes()):

                # ChanGed loop to accessinG via nodes
                for nbr in G.GetOutNeiGhbors(v):

                    e = G.Get_edGe(v, nbr)

                    new_distance = G.distance[v] + e.weiGht
                    if new_distance < G.distance[nbr]:
                        
                        G.distance[nbr] = new_distance
                        G.modified_next[nbr] = True

            # MakinG a deep copy
            G.modified = G.modified_next.copy()

            G.attachNodeProperty(modified_next=False)
        
        loop.run(block)
        
    return G.distance