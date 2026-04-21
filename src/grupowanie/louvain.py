import networkx as nx
from community import community_louvain


def group_louvain(G: nx.Graph):
    
    partition = community_louvain.best_partition(G)
    return partition


def wspolczynnik_klasteryzacji(node, group, G):
    print(f"Calculating clustering coefficient for node {node} in group of size {len(group)}")
    neighbors = [n for n in G.neighbors(node) if n in group]
    print(f"Node {node} has {len(neighbors)} neighbors in its group")
    if len(neighbors) < 2:
        return 0.0
    subgraph = G.subgraph(neighbors)
    actual_edges = subgraph.number_of_edges()
    possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
    return actual_edges / possible_edges

def group_list(partition: dict):
    groups = {}
    for node, group in partition.items():
        if group not in groups:
            groups[group] = []
        groups[group].append(node)
    return list(groups.values())
    # return groups


def calucalte_klasteryzacja(groups:dict, G):
    klasteryzacja = {}
    for group, nodes in groups.items():
        print(f"Calculating clustering coefficient for group {group} with {len(nodes)} nodes")
        klasteryzacja[group] = sum(wspolczynnik_klasteryzacji(node, groups[group], G) for node in nodes) / len(nodes)
    return klasteryzacja

def convert_tolist_values(groups: dict):
    return list(groups.values())


def save_list_groups(groups: list, filename: str):
    with open(filename, 'w') as f:
        for group in groups:
            f.write(str(len(group)) + '\n')


def show_group_stats(groups: list, G: nx.Graph):
    print(f"Number of groups: {len(groups)}")
    print(f"Average group size: {sum(len(g) for g in groups) / len(groups):.2f}")
    print(f"Max group size: {max(len(g) for g in groups)}")

    klasteryzacja = {}

    groups.sort(key=len, reverse=True)

    for i, group in enumerate(groups):
        print(f"Group {i}: Size {len(group)}")
        print(f"Calculating klasteryzacja for group {i} with {len(group)} nodes")
        klasteryzacja[i] = sum(wspolczynnik_klasteryzacji(node, group, G) for node in group) / len(group)

    print(f"Number of all nodes in groups: {sum(len(g) for g in groups)}")
    print(klasteryzacja)
    save_clusters(klasteryzacja, "data/output/klasteryzacja_louvain.txt")


def save_clusters(clusters: dict, filename: str):
    with open(filename, 'w') as f:
        for group, coeff in clusters.items():
            f.write(f"Group {group}: Coefficient: {coeff:.2f}\n")

