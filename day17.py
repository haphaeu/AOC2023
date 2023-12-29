import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix


"""
https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.dijkstra.html
https://stackoverflow.com/questions/53074947/examples-for-search-graph-using-scipy

Build a graph matrix of the grid, with connectivity and distances
between nodes. The matrix item (i, j) is the distance between 
nodes i and j. Note that directionality is important, ie:

   distance(i, j) != distance(j, i)

Example:

    grid
    241
    321                           to node j
    325                       0 1 2 3 4 5 6 7 8
       >4     >1            +-----------------
  (0)----(1)----(2)       0 | 0 4 0 3 0 0 0 0 0
   |  <2  |  <4  |      f 1 | 2 0 1 0 2 0 0 0 0
 v3|^2  v2|^4  v1|^1    r 2 | 0 4 0 0 0 1 0 0 0
   |  >2  |  >1  |      o 3 | 2 0 0 0 2 0 3 0 0
  (3)----(4)----(5)     m 4 | 0 4 0 3 0 1 0 2 0
   |  <3  |  <2  |        5 | 0 0 1 0 2 0 0 0 5
 v3|^3  v2|^2  v5|^1    i 6 | 0 0 0 3 0 0 0 2 0
   |  >2  |  >5  |        7 | 0 0 0 0 2 0 3 0 5
  (6)----(7)----(8)       8 | 0 0 0 0 0 1 0 2 0
      <3     <2

For convenience, for a grid of size N, it may be better to call
nodes (r,c), such that connectivity is:

   (r,c) -> (r+1,c), (r,c+1), (r-1,c), (r,c-1)
   given r+1,c+1 < N, r-1,c-1 >= 0

and then numbering the nodes i as:

    i = c + N * r

So the matrix above becomes:

    (r0, c0)->(r1, c1) => i->j: w   
    (0, 0)  -> (0, 1)  => 0->1: 4
    (0, 1)  -> (0, 0)  => 1->0: 2
    ...
 

"""


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

grid = np.array([[int(c) for c in line] for line in lines])


N = grid.shape[0]
graph = np.zeros((N * N, N * N))

for i in range(N * N):
    r = i // N
    c = i % N
    neighbors = [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]
    for r2, c2 in neighbors:
        if r2 < 0 or r2 >= N or c2 < 0 or c2 >= N:
            continue
        j = c2 + N * r2
        assert graph[i, j] == 0
        graph[i, j] = grid[r2, c2]

print(graph)

#######

graph = csr_matrix(graph)
dist_matrix, predecessors = dijkstra(graph, indices=0, return_predecessors=True)

# show path
path = np.zeros_like(grid)
node = N * N - 1
while (prev := predecessors[node]) != -9999:
    r = node // N
    c = node % N
    path[r, c] = 1
    node = prev
print(str(path).replace("0", ".").replace("1", "X"))
