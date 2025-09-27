import networkx as nx
from networkx.drawing import nx_pydot
from collections import deque
import sys

def read_graph(file_path):
    G = nx_pydot.read_dot(file_path)
    if G.is_directed():
        G = nx.DiGraph(G)
    else:
        G = nx.Graph(G)
    return G

def graph_to_adj_matrix(G):
    ordered_nodes = sorted(G.nodes())
    return nx.to_numpy_array(G, nodelist=ordered_nodes).tolist()

def bfs(adj_matrix):
    visited = set()
    predecessor = {}
    F = deque([0])
    visited.add(0)
    order = []
    while F:
        u = F.popleft()
        order.append(u)
        for v, val in enumerate(adj_matrix[u]):
            if val == 1 and v not in visited:
                visited.add(v)
                predecessor[v] = u
                F.append(v)
    return order, predecessor

if __name__ == "__main__":
    G = read_graph(sys.argv[1])
    print(G.nodes)
    print(G.edges)
    adj_matrix = graph_to_adj_matrix(G)
    print(adj_matrix)
    print(bfs(adj_matrix))