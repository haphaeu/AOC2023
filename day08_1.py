data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

with open("day08.txt") as f:
    data = f.read()

lines = data.splitlines()

"""
Copilot prompt:

The first line of `data` has instructions to go left or right, L means left, R means right.

After that, there is a blank line, and then there's a list of nodes and connected nodes if you go left or right. For example `AAA = (BBB, CCC)` means that from node `AAA` if you go left you end up in `BBB` and if you go right you end up in `CCC` 

Following the left-right instructions from the first line, and starting in the node `AAA`, how many steps does it take to reach the node `ZZZ`? 

If you run out of left-right instruction, cycle through the same list of left-right instructions again.
"""

# Parse the left-right instructions
instructions = lines[0]

# Parse the nodes and connected nodes
nodes = {}
for line in lines[2:]:
    node, connections = line.split(" = ")
    left, right = connections.strip("()").split(", ")
    nodes[node] = (left, right)

# Follow the left-right instructions until reaching ZZZ
current_node = "AAA"
steps = 0
while current_node != "ZZZ":
    left, right = nodes[current_node]
    if instructions[steps % len(instructions)] == "L":
        current_node = left
    else:
        current_node = right
    steps += 1

print("Number of steps to reach ZZZ:", steps)
