from core import Node, Tree, ForestDist
from tree_edit_distance import tree_edit_distance, cost_function
import matplotlib.pyplot as plt
import networkx as nx

# Plotting
def plot_graph(G: nx.DiGraph):
    # pos = nx.nx_agraph.pygraphviz_layout(G)
    labels = nx.get_node_attributes(G, 'symbol')
    nx.draw_networkx(G, labels=labels)

# Examples!
n1_1 = Node(value = "a")
n1_2 = Node(value = "b")
n1_3 = Node(value = "c")
n1_4 = Node(value = "d")

n1_1.children = [n1_2, n1_3, n1_4]
n1_2.parent_node = n1_1
n1_3.parent_node = n1_1
n1_4.parent_node = n1_1

T1 = Tree([n1_1, n1_2, n1_3, n1_4], root = n1_1)

n2_1 = Node(value = "a")
n2_2 = Node(value = "b")
n2_3 = Node(value = "c")
n2_4 = Node(value = "d")

n2_1.children = [n2_2, n2_4, n2_3]
n2_2.parent_node = n2_1
n2_3.parent_node = n2_1
n2_4.parent_node = n2_1

T2 = Tree([n2_1, n2_2, n2_3, n2_4], root = n2_1)

treedist, _ = tree_edit_distance(T1, T2)
print(treedist)

plt.figure(1)
T1_nx = T1.to_nx_di_graph()
plot_graph(T1_nx)

plt.figure(2)
T2_nx = T2.to_nx_di_graph()
plot_graph(T2_nx)

plt.show()
