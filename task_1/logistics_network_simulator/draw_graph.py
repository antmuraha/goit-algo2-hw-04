import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G, pos):
    plt.figure(figsize=(10, 6))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        font_size=8,
    )
    labels = nx.get_edge_attributes(G, "capacity")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Display the graph
    plt.show()
