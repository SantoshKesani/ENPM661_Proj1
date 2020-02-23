### 8 PUZZLE PROBLEM ###
# By - Santosh Kesani
# UID - 117035605

import numpy as np
import os


# Initializing a class to solve the 8 puzzle problem
class eightpuzz:
    def __init__(self, node_num, data, parentnode, tileaction, cost):
        self.data = data
        self.parentnode = parentnode
        self.tileaction = tileaction
        self.node_num = node_num
        self.cost = cost

# Getting Input for the initial node
def node_info():
    print("\nEnter the numbers for puzzle (Only 0-8, without repetition): \n "  )
    first_state = np.zeros(9)
    for i in range(9):
        node = int(input("Enter the " + str(i + 1) + " number: " + "\n"))
        if node < 0 or node > 8:
            print("Please only enter numbers which are [0-8]")
            exit(0)
        else:
            first_state[i] = np.array(node)
    return np.reshape(first_state, (3, 3))

# Finding the location of zero tile
def blank_tile_loc(current_loc):
    i, j = np.where(current_loc == 0)
    i = int(i)
    j = int(j)
    return i, j

# Function to move up
def up_move(current_loc):
    i, j = blank_tile_loc(current_loc)
    if i == 0:   # Checking if the current the location is already in the top row
        return None
    else:  # Moving the empty tile towards up using assignment with random variable
        temp_arr = np.copy(current_loc)
        temp = temp_arr[i - 1, j]
        temp_arr[i, j] = temp
        temp_arr[i - 1, j] = 0
        return temp_arr

# Function to move down
def down_move(current_loc):
    i, j = blank_tile_loc(current_loc)
    if i == 2:  # Checking if the current the location is already in the bottom row
        return None
    else:   # Moving the empty tile towards down using assignment with random variable
        temp_arr = np.copy(current_loc)
        temp = temp_arr[i + 1, j]
        temp_arr[i, j] = temp
        temp_arr[i + 1, j] = 0
        return temp_arr

# Function to move right
def right_move(current_loc):
    i, j = blank_tile_loc(current_loc)
    if j == 2:   # Checking if the current the location is already in the right most column
        return None
    else:   # Moving the empty tile towards right using assignment with random variable
        temp_arr = np.copy(current_loc)
        temp = temp_arr[i, j + 1]
        temp_arr[i, j] = temp
        temp_arr[i, j + 1] = 0
        return temp_arr

# Function to move left
def left_move(current_loc):
    i, j = blank_tile_loc(current_loc)
    if j == 0:  # Checking if the current the location is already in the left most column
        return None
    else:   # Moving the empty tile towards left using assignment with random variable
        temp_arr = np.copy(current_loc)
        temp = temp_arr[i, j - 1]
        temp_arr[i, j] = temp
        temp_arr[i, j - 1] = 0
        return temp_arr

# Function to decide the movement of tile
def tile_move(move, data):
    if move == 'Up':
        return up_move(data)
    if move == 'Down':
        return down_move(data)
    if move == 'Left':
        return left_move(data)
    if move == 'Right':
        return right_move(data)
    else:
        return None

# Function to check whether the given input is solvable or not
def solvability(puzzle):
    A = puzzle.reshape(-1)
    A = A.tolist()
    A = [a for a in A if a != 0]
    inversions = 0  # variable to store the inversions in a given input
    for i in range(0, len(A)):   # Finding the inversions
        x = A[i]
        for j in range(i, len(A)):
            if A[j] < x:
                inversions += 1
    if inversions % 2 == 0:     # If the inversions are even then the given input is solvable
        return ("true")
    else:
        return ("false")

# Finding the required nodes
def find_nodes(node):
    print("Finding the solution \n")
    move = ["Down", "Up", "Left", "Right"]
    required = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    node_temp = [node]
    final_nodes = []
    visited_nodes = []
    final_nodes.append(node_temp[0].data.tolist())  # Appending data of nodes in seen
    node_id = 0  # Defining IDs to all the nodes formed

    while node_temp:
        working_node = node_temp.pop(0)  # Pop the element 0 from the list
        if working_node.data.tolist() == required.tolist():
            print("Solution Found \n")
            return working_node, final_nodes, visited_nodes

        for action in move:
            temp_data = tile_move(action, working_node.data)
            if temp_data is not None:
                node_id += 1
                child_node = eightpuzz(node_id, np.array(temp_data), working_node, action, 0)  # Creating a child node

                if child_node.data.tolist() not in final_nodes:  # Add the child node data in final node list
                    node_temp.append(child_node)
                    final_nodes.append(child_node.data.tolist())
                    visited_nodes.append(child_node)
                    if child_node.data.tolist() == required.tolist():
                        print("Solution Found")
                        return child_node, final_nodes, visited_nodes
    return None, None, None  # Return when required node is not found

# Path - final to start node
def path(node):
    p = []  # Initializing an empty list
    p.append(node)
    parent_node = node.parentnode
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parentnode
    return list(reversed(p))

# Printing final states
def print_matrix(final_list):
    print("Printing the final solution and also the path to the required node \n")
    for l in final_list:
        print("Node No.:  " + str(l.node_num) + "\n" + "Action performed : " + str(l.tileaction) + "\n" + "Resulting Node :" + "\n" + str(l.data))

# Text file edit for path
def path_textfile(path_formed):
    if os.path.exists("nodePath.txt"):   # Checking the existence of textfile and removing it
        os.remove("nodePath.txt")

    f = open("nodePath.txt", "a")
    for node in path_formed:    # Rewriting the textfile with path found
        if node.parentnode is not None:
            f.write(str(node.node_num) + "\t" + str(node.parentnode.node_num) + "\t" + str(node.cost) + "\n")
    f.close()

# Text file edit of all node
def allnodes_textfile(explored):
    if os.path.exists("Nodes.txt"):     # Checking existence of textfile and removing it
        os.remove("Nodes.txt")

    f = open("Nodes.txt", "a")
    for element in explored:     # Rewriting the textfile with all the nodes found
        f.write('[')
        for i in range(len(element)):
            for j in range(len(element)):
                f.write(str(element[j][i]) + " ")
        f.write(']')
        f.write("\n")
    f.close()

# Text file edit of node info
def nodeinfo_textfile(visited):
    if os.path.exists("NodesInfo.txt"):     # Checking existence of textfile and removing it
        os.remove("NodesInfo.txt")

    f = open("NodesInfo.txt", "a")
    for n in visited:       # Rewriting the textfile with the node info
        if n.parentnode is not None:
            f.write(str(n.node_num) + "\t" + str(n.parentnode.node_num) + "\t" + str(n.cost) + "\n")
    f.close()


### MAIN FUNCTION ###
# Storing the given matrix in random array
puzz_matrix = node_info()

# Calling the function to check whether solution exists or not
solvability(puzz_matrix)

# Calling the class
reqval = eightpuzz(0, puzz_matrix, None, None, 0)

# Brute Force Search
final, N, visit = find_nodes(reqval)

if final is None and N is None and visit is None:
    print("Goal State not found")
else:
    # Print and write the final output
    print_matrix(path(final))
    path_textfile(path(final))
    allnodes_textfile(N)
    nodeinfo_textfile(visit)