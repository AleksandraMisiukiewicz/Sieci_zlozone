from src.load_data import load_graph
import networkx as nx
from src.network_analysis import *
from visualize_graph import draw_graph
from src.grupowanie.louvain import group_louvain, group_list, save_list_groups, show_group_stats


def main():

    G = load_graph("data/links.tsv")

    print("Graph loaded")

    partition = group_louvain(G.to_undirected())
    groups = group_list(partition)
    save_list_groups(groups, "data/output/groups_louvain.txt")
    show_group_stats(groups)




    #viusalization
    #draw_graph(G)

    #informacje o sieci

    # print("Number of nodes:", G.number_of_nodes())
    # print("Number of edges:", G.number_of_edges())
    
    # print("Density:", nx.density(G))
    # print("Average degree:", sum(dict(G.degree()).values()) / G.number_of_nodes())
    
    
    # largest_cc = max(nx.weakly_connected_components(G), key=len)
    
    # G_sub = G.subgraph(largest_cc)
    
    # #largest_cc = max(nx.weakly_connected_components(G), key=len)
    
    # print("Largest component size:", len(largest_cc))
    # print("Fraction of graph:", len(largest_cc) / G.number_of_nodes())
    
    # diameter = nx.diameter(G_sub.to_undirected())
    
    # print("Network diameter:", diameter)


    # show_degree_statistics(G)
    # node_categories(G)
    # network_diameter_print(G)
    # analyze_centralities(G)


if __name__ == "__main__":
    main()