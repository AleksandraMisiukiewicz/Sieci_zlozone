#jedna z metod link prediction
import networkx as nx

def tradic_closure(G: nx.Graph):
    new_edges = []
    for node in G.nodes():
        neighbors = set(G.neighbors(node))
        for neighbor in neighbors:
            second_neighbors = set(G.neighbors(neighbor))
            for second_neighbor in second_neighbors:
                if second_neighbor != node and second_neighbor not in neighbors:
                    new_edges.append((node, second_neighbor))
    return new_edges


def save_tradic_edges(edges: list, filename: str):
    with open(filename, 'w') as f:
        for edge in edges:
            f.write(f"{edge[0]}\t{edge[1]}\n")