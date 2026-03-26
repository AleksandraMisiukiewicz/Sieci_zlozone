import networkx as nx
from community import community_louvain


def group_louvain(G: nx.Graph):
    
    partition = community_louvain.best_partition(G)
    return partition


def group_list(partition: dict):
    groups = {}
    for node, group in partition.items():
        if group not in groups:
            groups[group] = []
        groups[group].append(node)
    return list(groups.values())


def save_list_groups(groups: list, filename: str):
    with open(filename, 'w') as f:
        for group in groups:
            f.write(str(len(group)) + '\n')


def show_group_stats(groups: list):
    print(f"Number of groups: {len(groups)}")
    print(f"Average group size: {sum(len(g) for g in groups) / len(groups):.2f}")
    print(f"Max group size: {max(len(g) for g in groups)}")

    groups.sort(key=len, reverse=True)

    for i, group in enumerate(groups):
        print(f"Group {i}: Size {len(group)}")

    print(f"Number of all nodes in groups: {sum(len(g) for g in groups)}")
    

