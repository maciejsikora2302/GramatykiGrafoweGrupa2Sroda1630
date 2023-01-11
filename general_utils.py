import networkx as nx
from copy import copy
import matplotlib.pyplot as plt


class Attribute:
    LEVEL = "level"
    LABEL = "label"
    X = "x"
    Y = "y"


def draw(graph: nx.Graph, level: int = None, filename: str = "test_draw.png") -> None:
    if level is not None:
        graph = graph.subgraph(
            [
                node
                for node in graph.nodes
                if graph.nodes[node][Attribute.LEVEL] == level
            ]
        )

    pos = nx.spring_layout(graph)

    pos_labels = copy(pos)
    for node in graph.nodes():
        pos_labels[node] = (pos[node][0], pos[node][1] + 0.3)

    label_attr = nx.get_node_attributes(graph, Attribute.LABEL)
    xs = nx.get_node_attributes(graph, Attribute.X)
    ys = nx.get_node_attributes(graph, Attribute.Y)
    levels = nx.get_node_attributes(graph, Attribute.LEVEL)

    red_labels = ["El", "el"]
    blue_labels = ["E", "e"]
    yellow_labels = ["I", "i"]

    node_colors = []
    for node in graph.nodes():
        if label_attr[node] in red_labels:
            node_colors.append("red")
        elif label_attr[node] in blue_labels:
            node_colors.append("blue")
        elif label_attr[node] in yellow_labels:
            node_colors.append("yellow")
        else:
            node_colors.append("white")

    labels = {
        node: f"{label_attr[node], (xs[node], ys[node]), levels[node]}"
        for node in graph.nodes()
    }

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=2000,
        node_color=node_colors,
        edgecolors="black",
        linewidths=5,
        alpha=0.5,
    )
    nx.draw_networkx_edges(graph, pos, width=5, alpha=0.3)
    nx.draw_networkx_labels(graph, pos_labels, labels)

    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.savefig(filename)
    plt.cla()
    plt.clf()


def save_graph(graph: nx.Graph, filename: str):
    # add attribute to all nodes
    for node in graph.nodes:
        graph.nodes[node]["node_type"] = graph.nodes[node][Attribute.LABEL]
    nx.write_gexf(graph, filename)
