import matplotlib.pyplot as plt
import networkx as nx

# stopień węzła = liczba jego połączeń
def degree_statistics(G):

    in_degrees = [d for n, d in G.in_degree()]
    out_degrees = [d for n, d in G.out_degree()]
    total_degrees = [d for n, d in G.degree()]

    print("Average in-degree:", sum(in_degrees) / len(in_degrees))
    print("Average out-degree:", sum(out_degrees) / len(out_degrees))
    print("Average degree:", sum(total_degrees) / len(total_degrees))

def degree_distribution(G):

    degrees = [d for n, d in G.degree()]

    plt.figure(figsize=(8,6))

    plt.hist(degrees, bins=50)

    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Number of nodes")

    plt.show()

def log_degree_distribution(G):

    degrees = sorted([d for n, d in G.degree()], reverse=True)

    plt.figure(figsize=(8,6))

    plt.loglog(degrees)

    plt.title("Degree Distribution (log-log)")
    plt.xlabel("Rank")
    plt.ylabel("Degree")

    plt.show()

def show_degree_statistics(G):

    degree_statistics(G)
    degree_distribution(G)
    log_degree_distribution(G)

# klasyfikacja typów węzłów
# Hub - węzły o bardzo dużym stopniu.
# Connector - węzeł który łączy różne społeczności, ale nie musi mieć dużego stopnia. (closeness centrality)
# Peripheral - węzły słabo połączone
# Isolate - węzeł bez połączeń
# Authority - węzeł do którego prowadzi dużo linków.
# Broker (Bridge) - węzły które łączą różne części sieci (betweenness centrality)
def compute_metrics(G):
    degree = dict(G.degree())
    in_degree = dict(G.in_degree())

    betweenness = nx.betweenness_centrality(G)

    closeness = nx.closeness_centrality(G)

    return degree, in_degree, betweenness, closeness

def find_hubs(degree, top_n=10):
    hubs = sorted(
        degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return hubs

def find_authorities(in_degree, top_n=10):
    authorities = sorted(
        in_degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

    return authorities

def find_brokers(betweenness, top_n=10):
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

def find_peripheral(degree):
    peripheral = [n for n, d in degree.items() if d <= 2]

    return peripheral

def find_isolates(degree):
    isolates = [n for n, d in degree.items() if d == 0]

    return isolates

def node_categories(G):
    degree, in_degree, betweenness, closeness = compute_metrics(G)

    print("\nHubs:")
    print(find_hubs(degree))

    print("\nAuthorities:")
    print(find_authorities(in_degree))

    print("\nBrokers:")
    print(find_brokers(betweenness))

    print("\nConnectors:")
    print(find_connectors(closeness))

    print("\nPeripheral nodes:", len(find_peripheral(degree)))

    print("\nIsolates:", len(find_isolates(degree)))

# Średnica (diameter) = najdłuższa najkrótsza ścieżka pomiędzy dowolnymi dwoma węzłami
def compute_diameter(G):

    largest_cc = max(nx.weakly_connected_components(G), key=len)

    G_sub = G.subgraph(largest_cc)

    diameter = nx.diameter(G_sub.to_undirected())

    return diameter

def average_path_length(G):

    largest_cc = max(nx.weakly_connected_components(G), key=len)

    G_sub = G.subgraph(largest_cc)

    avg_path = nx.average_shortest_path_length(G_sub.to_undirected())

    return avg_path

def network_diameter_print(G):

    diameter = compute_diameter(G)
    print("\nNetwork diameter:", diameter)

    print("Average path length:", average_path_length(G))