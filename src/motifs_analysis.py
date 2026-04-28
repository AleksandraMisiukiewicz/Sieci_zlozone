import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import json


OUTPUT_PATH = "data/output"
CHARTS_PATH = "charts"

def nx_to_igraph(G):
    mapping = {node: i for i, node in enumerate(G.nodes())}
    edges = [(mapping[u], mapping[v]) for u, v in G.edges()]

    g = ig.Graph(directed=G.is_directed())
    g.add_vertices(len(mapping))
    g.add_edges(edges)

    return g

TRIAD_NAMES = {
    0: "003",
    1: "012",
    2: "102",
    3: "021D",
    4: "021U",
    5: "021C",
    6: "111D",
    7: "111U",
    8: "030T",
    9: "030C",
    10: "201",
    11: "120D",
    12: "120U",
    13: "120C",
    14: "210",
    15: "300"
}


def visualize_triad_motifs():
    print("Generating triad motif visualizations")

    triad_graphs = {}

    triad_edges = {
        0: [],
        1: [(0, 1)],
        2: [(0, 1), (1, 0)],
        3: [(0, 1), (0, 2)],
        4: [(1, 0), (2, 0)],
        5: [(0, 1), (1, 2)],
        6: [(0, 1), (1, 0), (0, 2)],
        7: [(0, 1), (1, 0), (2, 0)],
        8: [(0, 1), (1, 2), (0, 2)],
        9: [(0, 1), (1, 2), (2, 0)],
        10: [(0, 1), (1, 0), (1, 2), (2, 1)],
        11: [(0, 1), (1, 0), (0, 2), (2, 1)],
        12: [(0, 1), (1, 0), (2, 0), (1, 2)],
        13: [(0, 1), (1, 2), (2, 1), (0, 2)],
        14: [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2)],
        15: [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1)]
    }

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(4, 4, figsize=(12, 12))

    for i, ax in enumerate(axes.flatten()):
        edges = triad_edges.get(i, [])

        g = ig.Graph(directed=True)
        g.add_vertices(3)
        g.add_edges(edges)

        layout = g.layout_circle()

        ig.plot(
            g,
            target=ax,
            layout=layout,
            vertex_size=20,
            vertex_label=None
        )

        label = TRIAD_NAMES.get(i, f"{i}")
        ax.set_title(label)

    plt.tight_layout()
    plt.savefig(f"{CHARTS_PATH}/motifs_triads.png")
    plt.close()

    print("Saved: charts/motifs_triads.png")

def analyze_motifs_directed(G_nx, motif_size=3, random_graphs=30):
    print("Analyzing DIRECTED motifs (igraph)")

    g = nx_to_igraph(G_nx)


    real = g.motifs_randesu(size=motif_size)
    real = np.array([m if m is not None else np.nan for m in real])


    random_results = []


    p = g.ecount() / (g.vcount() * (g.vcount() - 1))

    for _ in range(random_graphs):
        g_rand = g.copy()
        g_rand.rewire(n=10 * g.ecount(), mode="simple")

        motifs = g_rand.motifs_randesu(size=motif_size)
        motifs = [m if m is not None else np.nan for m in motifs]

        random_results.append(motifs)

    random_results = np.array(random_results)

    # sprawdzamy które kolumny mają jakiekolwiek dane
    valid_columns = ~np.all(np.isnan(random_results), axis=0)

    # filtrujemy dane
    random_results = random_results[:, valid_columns]
    real = real[valid_columns]

    # teraz liczymy statystyki BEZ warningów
    mean = np.mean(random_results, axis=0)
    std = np.std(random_results, axis=0)

    std[std == 0] = 1e-9
    z_score = (real - mean) / std

    indices = np.arange(len(valid_columns))[valid_columns]

    labels = [TRIAD_NAMES.get(i, f"Motif {i}") for i in indices]
    x = np.arange(len(real))

    results = {
        "indices": indices.tolist(),
        "labels": labels,
        "real": real.tolist(),
        "mean": mean.tolist(),
        "z_score": z_score.tolist()
    }

    with open(f"{OUTPUT_PATH}/motifs_directed.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Saved: data/output/motifs_directed.json")

    plt.figure()
    plt.bar(x - 0.2, real, width=0.4, label="Real")
    plt.bar(x + 0.2, mean, width=0.4, label="Random")

    plt.xticks(x, labels, rotation=45)

    plt.title("Directed motifs (triads)")
    plt.xlabel("Triad type")
    plt.ylabel("Count")
    plt.legend()

    plt.savefig(f"{CHARTS_PATH}/motifs_directed_counts.png")
    plt.close()

    print("Saved: charts/motifs_directed_counts.png")

    plt.figure()
    plt.bar(x, z_score)

    plt.xticks(x, labels, rotation=45)

    plt.title("Directed motifs Z-score")
    plt.xlabel("Triad type")
    plt.ylabel("Z-score")

    plt.savefig(f"{CHARTS_PATH}/motifs_directed_zscore.png")
    plt.close()

    print("Saved: charts/motifs_directed_zscore.png")

    return results