from core import Node, Tree, ForestDist
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Cost function corresponding to counting the number of operations to transform T1 into T2
def cost_function(n1: Node, n2: Node) -> int:
    if n1.value == n2.value:
        return 0
    else:
        return 1

# Main function
def tree_edit_distance(T1: Tree, T2: Tree):
    LR_T1 = T1.LR_keyroots()
    LR_T2 = T2.LR_keyroots()

    T1_size = len(T1.nodes)
    T2_size = len(T2.nodes)

    treedist = np.empty((T1_size + 1, T2_size + 1))
    treedist[:] = np.nan

    # save the forestdist for each (i, j)
    forestdists_dict = dict()
    
    def compute_treedist(i, j):
        forestdist = ForestDist()

        l_i_node = T1.l(i)
        l_i = T1.node_to_i(l_i_node)
        l_j_node = T2.l(j)
        l_j = T2.node_to_i(l_j_node)

        forestdist.set(ForestDist.EMPTY, ForestDist.EMPTY, 0)

        EMPTY = Node()
        for i_1 in range(l_i, i + 1):
            forestdist.set((l_i, i_1), ForestDist.EMPTY, 
                           forestdist.get((l_i, i_1 - 1), ForestDist.EMPTY) + cost_function(T1.node(i_1), EMPTY) ) 

        for j_1 in range(l_j, j + 1):
            forestdist.set(ForestDist.EMPTY, (l_j, j_1), 
                           forestdist.get(ForestDist.EMPTY, (l_j, j_1 - 1)) + cost_function(EMPTY, T2.node(j_1)) ) 

        for i_1 in range(l_i, i + 1):
            for j_1 in range(l_j, j + 1):
                if T1.l(i_1) == T1.l(i) and T2.l(j_1) == T2.l(j):
                    option_1 = forestdist.get((l_i, i_1 - 1), (l_j, j_1)) + cost_function(T1.i_to_node(i_1), EMPTY)
                    option_2 = forestdist.get((l_i, i_1), (l_j, j_1 - 1)) + cost_function(EMPTY, T2.i_to_node(j_1))
                    option_3 = forestdist.get((l_i, i_1 - 1), (l_j, j_1 - 1)) + cost_function(T1.i_to_node(i_1), T2.i_to_node(j_1))

                    choosen_one = min([option_1, option_2, option_3])

                    forestdist.set((l_i, i_1), (l_j, j_1), choosen_one)
                    treedist[i_1, j_1] = forestdist.get((l_i, i_1), (l_j, j_1))
                else:
                    l_i1_node = T1.l(i_1)
                    l_i1 = T1.node_to_i(l_i1_node)
                    l_j1_node = T2.l(j_1)
                    l_j1 = T2.node_to_i(l_j1_node)

                    option_1 = forestdist.get((l_i, i_1 - 1), (l_j, j_1)) + cost_function(T1.i_to_node(i_1), EMPTY)
                    option_2 = forestdist.get((l_i, i_1), (l_j, j_1 - 1)) + cost_function(EMPTY, T2.i_to_node(j_1))
                    option_3 = forestdist.get((l_i, l_i1 - 1), (l_j, l_j1 - 1)) + treedist[i_1, j_1]

                    choosen_one = min([option_1, option_2, option_3])
                    forestdist.set((l_i, i_1), (l_j, j_1), choosen_one)

        forestdists_dict[(i, j)] = forestdist

    for i in LR_T1:
        for j in LR_T2:
            compute_treedist(i, j)

    return treedist, forestdists_dict

# Helper functions 
def construct_path(path_matrix: np.matrix, i0 = 0, j0 = 0) -> list[tuple]:
    """
    works by constructing the path backwards
    """
    m, n = path_matrix.shape
    path = []
    path.append((m-1, n-1))

    def next_element(i: int, j: int) -> None:
        if i == i0 and j == j0:
            return None
        else:
            options = [
                ((i, j - 1), path_matrix[i, j - 1]), 
                ((i - 1, j - 1), path_matrix[i - 1, j - 1]),
                ((i - 1, j), path_matrix[i - 1, j])
            ]
            # Pick by the smallest value in the matrix
            next_position = min(options, key = lambda t: t[1])
            path.insert(0, next_position[0])
            next_element(next_position[0][0], next_position[0][1])
    
    next_element(m-1, n-1)
    return path

def path_to_operations(path_matrix: np.matrix, path: list[int]):
    pass