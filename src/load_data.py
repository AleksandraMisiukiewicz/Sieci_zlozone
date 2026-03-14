import pandas as pd
import networkx as nx


def load_graph(path):

    links = pd.read_csv(
        path,
        sep="\t",
        comment="#",
        header=None
    )

    links.columns = ["source", "target"]

    G = nx.from_pandas_edgelist(
        links,
        source="source",
        target="target",
        create_using=nx.DiGraph()
    )

    return G