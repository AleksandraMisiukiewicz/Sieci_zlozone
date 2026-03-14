from src.load_data import load_graph
import networkx as nx

def main():

    G = load_graph("data/links.tsv")

    print("Graph loaded")

    print("Number of nodes:", G.number_of_nodes())
    print("Number of edges:", G.number_of_edges())

    print("Density:", nx.density(G))
    print("Average degree:", sum(dict(G.degree()).values()) / G.number_of_nodes())


    largest_cc = max(nx.weakly_connected_components(G), key=len)

    G_sub = G.subgraph(largest_cc)

    largest_cc = max(nx.weakly_connected_components(G), key=len)

    print("Largest component size:", len(largest_cc))
    print("Fraction of graph:", len(largest_cc) / G.number_of_nodes())

    diameter = nx.diameter(G_sub.to_undirected())

    print("Network diameter:", diameter)

if __name__ == "__main__":
    main()