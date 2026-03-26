import pandas as pd
import networkx as nx

def decode(name: str) -> str:
    return name.decode("utf-8")

def load_graph(path) -> nx.DiGraph:

    links = pd.read_csv(
        path,
        sep="\t",
        comment="#",
        header=None,
        encoding="utf-8"
    )

    links.columns = ["source", "target"]

    links.to_csv("data/links_decoded.csv", sep=",", index=False)

    

    G = nx.from_pandas_edgelist(
        links,
        source="source",
        target="target",
        create_using=nx.DiGraph()
    )

    return G

