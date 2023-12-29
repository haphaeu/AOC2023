data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".strip()

lines = data.splitlines()

import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix

graph = np.array([list(map(int, line)) for line in lines])
graph = csr_matrix(graph)

dijkstra(graph, directed=False, indices=0, return_predecessors=True)

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.dijkstra.html
# https://stackoverflow.com/questions/53074947/examples-for-search-graph-using-scipy
#
# 241
# 321                              to node j
# 325                           0 1 2 3 4 5 6 7 8
#        >4     >1            +-----------------      for a grid of size N,
#   (0)----(1)----(2)       0 | 0 4 0 3 0 0 0 0 0     it may be better to call nodes (x,y),
#    |  <2  |  <4  |      f 1 | 2 0 1 0 2 0 0 0 0     such that connectivity is:
#  v3|^2  v2|^4  v1|^1    r 2 | 0 4 0 0 0 1 0 0 0        (x,y) -> (x+1,y), (x,y+1), (x-1,y), (x,y-1)
#    |  >2  |  >1  |      o 3 | 2 0 0 0 2 0 3 0 0        given x+1,y+1 < N, x-1,y-1 >= 0
#   (3)----(4)----(5)     m 4 | 0 4 0 3 0 1 0 2 0     and then numbering the nodes i as:
#    |  <3  |  <2  |        5 | 0 0 1 0 2 0 0 0 5        i = x + N * y
#  v3|^3  v2|^2  v5|^1    i 6 | 0 0 0 3 0 0 0 2 0
#    |  >2  |  >5  |        7 | 0 0 0 0 2 0 3 0 5
#   (6)----(7)----(8)       8 | 0 0 0 0 0 1 0 2 0
#       <3     <2
