import networkx as nx
from networkx.drawing import nx_pydot
from collections import deque
import sys


# funcao pra ler o grafo do arquivo
def read_graph(file_path):
    # le o arquivo dot usando networkx
    G = nx_pydot.read_dot(file_path)
    if G.is_directed():
        G = nx.DiGraph(G)
    else:
        G = nx.Graph(G)
    return G


def graph_to_adj_matrix(G):
    # converte para matriz de adjacencia
    nodes = sorted(G.nodes())
    matrix = nx.to_numpy_array(G, nodelist=nodes).tolist()
    return matrix, nodes


def graph_to_adj_list(G):
    # converte para lista de adjacencia
    nodes = sorted(G.nodes())
    adj_list = {}
    for node in nodes:
        adj_list[node] = sorted(list(G.neighbors(node)))
    return adj_list, nodes


def bfs_matrix(adj_matrix, nodes):
    # BFS usando matriz
    if len(nodes) == 0:
        return [], {}

    n = len(nodes)
    visited = [False] * n
    parent = {}
    fila = deque([0])  # primeiro vertice
    visited[0] = True
    ordem_visita = []

    print(f"BFS iniciando no vertice: {nodes[0]}")

    while fila:
        atual = fila.popleft()
        ordem_visita.append(nodes[atual])

        # verifica todos os vizinhos
        for vizinho in range(n):
            if (
                adj_matrix[atual][vizinho] == 1.0 and not visited[vizinho]
            ):  # comparacao com 1.0
                visited[vizinho] = True
                parent[nodes[vizinho]] = nodes[atual]
                fila.append(vizinho)

    return ordem_visita, parent


def dfs_list(adj_list, nodes):
    # DFS com lista de adjacencia
    visited = set()
    parent = {}
    tempo_inicio = {}
    tempo_fim = {}
    ordem_visita = []
    tempo = [0]  # precisa ser lista pra funcionar
    arvores = 0

    def dfs_visita(vertice):
        # visita um vertice
        tempo[0] += 1
        tempo_inicio[vertice] = tempo[0]
        visited.add(vertice)
        ordem_visita.append(vertice)

        # vai pros vizinhos
        for vizinho in adj_list[vertice]:
            if vizinho not in visited:
                parent[vizinho] = vertice
                dfs_visita(vizinho)

        tempo[0] += 1
        tempo_fim[vertice] = tempo[0]

    print("DFS:")

    # percorre todos os vertices
    for vertice in nodes:
        if vertice not in visited:
            arvores += 1
            print(f"Arvore {arvores} - vertice: {vertice}")
            dfs_visita(vertice)

    print(f"Total: {arvores} arvore(s)")
    return ordem_visita, parent, tempo_inicio, tempo_fim


def print_bfs_results(ordem, parent):
    print("\n=== BFS ===")
    print(f"Visitacao: {' -> '.join(ordem)}")
    print("Pais:")
    for v in sorted(parent.keys()):
        print(f"  {v} -> {parent[v]}")


def print_dfs_results(ordem, parent, inicio, fim):
    print("\n=== DFS ===")
    print(f"Visitacao: {' -> '.join(ordem)}")
    print("Pais:")
    for v in sorted(parent.keys()):
        print(f"  {v} -> {parent[v]}")

    print("Tempos:")
    for v in sorted(inicio.keys()):
        print(f"  {v}: {inicio[v]}/{fim[v]}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python reader.py arquivo.dot")
        sys.exit(1)

    arquivo = sys.argv[1]  # nome do arquivo
    debug = False  # pra debug depois

    # le o grafo
    grafo = read_graph(arquivo)

    print("=== INFO DO GRAFO ===")
    if grafo.is_directed():
        tipo = "Direcionado"
    else:
        tipo = "Nao direcionado"
    print(f"Tipo: {tipo}")
    print(f"Vertices: {sorted(grafo.nodes())}")
    print(f"Arestas: {list(grafo.edges())}")
    print()

    # matriz pra BFS
    matriz, vertices = graph_to_adj_matrix(grafo)
    print(f"Matriz (vertices: {vertices}):")
    for i in range(len(matriz)):
        print(f"  {vertices[i]}: {matriz[i]}")

    ordem_bfs, pai_bfs = bfs_matrix(matriz, vertices)
    print_bfs_results(ordem_bfs, pai_bfs)

    # lista pra DFS
    lista_adj, vertices = graph_to_adj_list(grafo)
    print("\nLista:")
    for v in vertices:
        print(f"  {v}: {lista_adj[v]}")

    ordem_dfs, pai_dfs, inicio_dfs, fim_dfs = dfs_list(lista_adj, vertices)
    print_dfs_results(ordem_dfs, pai_dfs, inicio_dfs, fim_dfs)
