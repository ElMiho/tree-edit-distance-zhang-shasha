import collections
import networkx as nx

class Node:
    def __init__(self, id = None, parent_node = None, value = None, children = []):
        self.parent_node = parent_node
        self.children = children
        self.value = value
        self.id = id

class Tree:
    def __init__(self, nodes = [], root = None):
        self.nodes = nodes
        self.root = root
        self.ordering = self.get_ordering()
    
    def get_ordering(self):
        if self.nodes == []:
            return []
        
        idx_list = [0] * len(self.nodes)
        idx = 1

        def has_children_been_visited(node: Node):
            all_visited = True
            for child in node.children:
                pos = self.nodes.index(child)
                if idx_list[pos] == 0: 
                    all_visited = False
                    break

            if all_visited:
                return None
            else:
                return child

        # Find fist node
        current = self.root
        while current.children != []:
            current = current.children[0]
        
        # And visit the nodes in left-to-right postorder numbering
        while 0 in idx_list:
            if has_children_been_visited(current) == None:
                # Visit the current
                pos = self.nodes.index(current)
                idx_list[pos] = idx
                idx +=1 
                
                # And go to parent
                current = current.parent_node
            else:
                current = has_children_been_visited(current)

        return idx_list

    def l(self, i):
        ordering = self.ordering
        pos = ordering.index(i)
        current = self.nodes[pos]
        while current.children != []:
            current = current.children[0]

        return current
    
    def node_to_i(self, node):
        ordering = self.ordering
        pos = self.nodes.index(node)

        return ordering[pos]
    
    def i_to_node(self, i):
        pos = self.ordering.index(i)
        return self.nodes[pos]
    
    def LR_keyroots(self):
        keyroots = []
        
        ordering = self.ordering
        keyroots.append(max(ordering))

        for k in range(1, len(self.nodes)): # Excluding the last element since this is the root
            k_node = self.nodes[
                ordering.index(k)
            ]
            parent_k_node = k_node.parent_node
            parent_k = ordering[
                self.nodes.index(parent_k_node)
            ]

            if self.l(k) != self.l(parent_k):
                keyroots.append(k)

        return sorted(keyroots)

    def to_nx_di_graph(self) -> nx.DiGraph:
        q = collections.deque()
        G = nx.DiGraph()

        ordering = self.ordering
        for idx, node in enumerate(self.nodes):
            node.id = ordering[idx]
        
        for node in self.nodes:
            G.add_node(node.id, symbol=f"{node.value}({node.id})")

        for node in self.nodes:
            for child in node.children:
                if child in self.nodes:
                    G.add_edge(node.id, child.id)

            if node.parent_node in self.nodes:
                G.add_edge(node.parent_node.id, node.id)

        return G
    
    def node(self, i):
        return self.nodes[i-1]
    
class ForestDist:
    EMPTY = (0,0)

    def __init__(self):
        self.values = dict()

    @staticmethod
    def index(x, y):
        if x <= y:
            return (x, y)
        else:
            return ForestDist.EMPTY

    def set(self, l_i_i, l_j_j, value):
        i_index = ForestDist.index(*l_i_i)
        j_index = ForestDist.index(*l_j_j)
        self.values[(i_index, j_index)] = value

    def get(self, l_i_i, l_j_j):
        i_index = ForestDist.index(*l_i_i)
        j_index = ForestDist.index(*l_j_j)
        return self.values[(i_index, j_index)]
    
    def __repr__(self):
        values_str = ",\n".join("=".join((str(k),str(v))) for k,v in sorted(self.values.items()))
        return f"""ForestDist(
            {values_str}
        )"""