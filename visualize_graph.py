import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(G: nx.DiGraph):
    pos = nx.spring_layout(G, seed=42)

    fig = plt.figure()
    ax = plt.gca()
    ax.set_axis_off()

    # rozróżnij izolowane węzły
    isolated = list(nx.isolates(G))
    connected = [n for n in G.nodes if n not in isolated]

    # rysuj normalne węzły
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=connected,
        node_size=20,
        ax=ax
    )

    # rysuj izolowane osobno (np. na czerwono)
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=isolated,
        node_size=30,
        node_color="red",
        ax=ax
    )

    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4)

    plt.show()