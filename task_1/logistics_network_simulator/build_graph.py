import networkx as nx


def build_graph(edges):
    """
    Builds the flow network graph for logistics of goods from warehouses to stores.
    """
    G = nx.DiGraph()

    for edge in edges:
        G.add_edge(
            edge[0],
            edge[1],
            capacity=edge[2],
        )

    return G
