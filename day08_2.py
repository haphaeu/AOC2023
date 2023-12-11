from math import lcm

data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

with open("day08.txt") as f:
    data = f.read()

"""
The first line of `data` has instructions to go left or right, L means
left, R means right. Then there's a list of nodes and the associated 
connected nodes if you go left or right. For example `AAA = (BBB, CCC)`
means that from node `AAA` if you go left you end up in `BBB` and if 
you go right you end up in `CCC`.

You start simultaneously from all the nodes ending in `A`, for example
`11A` and `22A`. And then, following the left-right instructions from 
the first line, how many steps does until you simultaneously end up in 
nodes ending with `Z`?

If you run out of left-right instruction, cycle through the same list 
of left-right instructions again.
"""

# Parse the data and create a dictionary to store the connections
connections = {}
lines = data.strip().split("\n")
for line in lines[2:]:
    print(line)
    node, connections_str = line.split(" = ")
    connections[node] = tuple(connections_str.strip("()").split(", "))

# Find all starting nodes ending with 'A'
starting_nodes = [node for node in connections.keys() if node.endswith("A")]

# Initialize the current nodes with the starting nodes
current_nodes = starting_nodes.copy()


def count_steps(node):
    print(f"{node=}")
    steps = 0
    while not node.endswith("Z"):
        # Update the current nodes based on the left-right instructions
        left_node, right_node = connections[node]
        direction = lines[0][steps % len(lines[0])]
        print(
            f"Step {steps+1:_}: Node {node} goes {direction} to {left_node} or {right_node}",
            end="\r",
        )
        node = left_node if direction == "L" else right_node
        steps += 1
    print()
    return steps


# Print the number of steps
steps_each = []
for node in current_nodes:
    steps = count_steps(node)
    print(f"Node {node} took {steps} steps to reach Z   ")
    steps_each.append(steps)
print(lcm(*steps_each))

# Output: 13_663_968_099_527
