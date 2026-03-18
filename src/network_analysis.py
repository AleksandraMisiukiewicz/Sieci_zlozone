import json

import matplotlib.pyplot as plt
import networkx as nx


output_path = "data/output"

# stopień węzła = liczba jego połączeń
def degree_statistics(G):
    print("Calculating degree statistics")

    in_degrees = [d for n, d in G.in_degree()]
    out_degrees = [d for n, d in G.out_degree()]
    total_degrees = [d for n, d in G.degree()]

    print("Average in-degree:", sum(in_degrees) / len(in_degrees))
    print("Average out-degree:", sum(out_degrees) / len(out_degrees))
    print("Average degree:", sum(total_degrees) / len(total_degrees))

def degree_distribution(G: nx.Graph):
    print("Visualizing degree distribution")

    degrees = [d for n, d in G.degree()]

    plt.figure(figsize=(8,6))

    plt.hist(degrees, bins=50)

    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")

    plt.show()

def log_degree_distribution(G : nx.Graph):
    print("Visualizing degree distribution in logaritmic scale")

    degrees = sorted([d for n, d in G.degree()], reverse=True)

    plt.figure(figsize=(8,6))

    plt.loglog(degrees)

    plt.title("Degree Distribution (log-log)")
    plt.xlabel("Rank")
    plt.ylabel("Degree")

    plt.show()

def show_degree_statistics(G: nx.Graph):

    degree_statistics(G)
    degree_distribution(G)
    log_degree_distribution(G)

def save_degree_statistics(G: nx.Graph, filename: str):
    degrees = [d for _, d in G.degree()]
    
    degree_count = {}
    for d in degrees:
        degree_count[d] = degree_count.get(d, 0) + 1

    with open(f"{output_path}/{filename}", "w") as f:
        for d in sorted(degree_count):
            f.write(f"{d}, {degree_count[d]}\n")
            # saving in file in format: degree, count


# klasyfikacja typów węzłów
# Hub - węzły o bardzo dużym stopniu.
# Connector - węzeł który łączy różne społeczności, ale nie musi mieć dużego stopnia. (closeness centrality)
# Peripheral - węzły słabo połączone
# Isolate - węzeł bez połączeń
# Authority - węzeł do którego prowadzi dużo linków.
# Broker (Bridge) - węzły które łączą różne części sieci (betweenness centrality)
def compute_metrics(G : nx.Graph):
    print("Computing metrics")
    degree = dict(G.degree())
    in_degree = dict(G.in_degree())

    betweenness = nx.betweenness_centrality(G)

    closeness = nx.closeness_centrality(G)

    return degree, in_degree, betweenness, closeness

def find_hubs(degree: dict, top_n=10):
    hubs = sorted(
        degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return hubs

def find_authorities(in_degree: dict, top_n=10):
    authorities = sorted(
        in_degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return authorities

def find_brokers(betweenness: dict, top_n=10):
    brokers = sorted(
        betweenness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return brokers

def find_connectors(closeness, top_n=10):
    connectors = sorted(
        closeness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return connectors

def find_peripheral(degree: dict):
    peripheral = [n for n, d in degree.items() if d <= 2]

    return peripheral

def find_isolates(degree: dict):
    isolates = [n for n, d in degree.items() if d == 0]

    return isolates


def save_node_categories(data: list, filename: str):

    with open(f"{output_path}/{filename}", "w") as f:
        for item in data:
            f.write(f"{item}\n")
        

def node_categories(G):
    print("Computing node categories")
    degree, in_degree, betweenness, closeness = compute_metrics(G)

    print("\nFinding Hubs:")
    hubs = find_hubs(degree)
    save_node_categories(hubs, "hubs.txt")
    print(hubs)

    print("\nFincing Authorities:")
    authorities = find_authorities(in_degree)
    save_node_categories(authorities, "authorities.txt")
    print(authorities)

    print("\nFinding Brokers:")
    brokers = find_brokers(betweenness)
    save_node_categories(brokers, "brokers.txt")
    print(brokers)

    print("\n Finding Connectors:")
    connectors = find_connectors(closeness)
    save_node_categories(connectors, "connectors.txt")
    print(connectors)

    print("\n Finding Peripherals:")
    peripheperal = find_peripheral(degree)
    save_node_categories(peripheperal, "peripheral.txt")
    print("\nPeripheral nodes:", len(peripheperal))

    print("\n Finding isloated:")
    isolated = find_isolates(degree)
    save_node_categories(isolated, "isolates.txt")
    print("\nIsolates:", len(isolated))

# Średnica (diameter) = najdłuższa najkrótsza ścieżka pomiędzy dowolnymi dwoma węzłami
def compute_diameter(G: nx.Graph):

    largest_cc = max(nx.weakly_connected_components(G), key=len)

    G_sub = G.subgraph(largest_cc)

    diameter = nx.diameter(G_sub.to_undirected())

    return diameter

def average_path_length(G: nx.Graph):

    largest_cc = max(nx.weakly_connected_components(G), key=len)

    G_sub = G.subgraph(largest_cc)

    avg_path = nx.average_shortest_path_length(G_sub.to_undirected())

    return avg_path

def network_diameter_print(G: nx.Graph):

    diameter = compute_diameter(G)
    print("\nNetwork diameter:", diameter)

    print("Average path length:", average_path_length(G))

# Centralność węzłów i krawędzi (rozkłady)
# Metryki:
# degree centrality
# betweenness centrality
# closeness centrality
# PageRank
# edge betweenness

def analyze_centralities(G: nx.Graph):

    degree_centrality = nx.degree_centrality(G)

    betweenness_centrality = nx.betweenness_centrality(G)

    closeness_centrality = nx.closeness_centrality(G)

    pagerank = nx.pagerank(G)

    edge_betweenness = nx.edge_betweenness_centrality(G)

    def plot_distribution(values, title):

        plt.figure(figsize=(8,6))

        plt.hist(values, bins=50)

        plt.title(title)

        plt.xlabel("Centrality value")
        plt.ylabel("Frequency")

        plt.show()

    plot_distribution(degree_centrality.values(), "Degree Centrality Distribution")

    plot_distribution(betweenness_centrality.values(), "Betweenness Centrality Distribution")

    plot_distribution(closeness_centrality.values(), "Closeness Centrality Distribution")

    plot_distribution(pagerank.values(), "PageRank Distribution")

    plot_distribution(edge_betweenness.values(), "Edge Betweenness Distribution")

