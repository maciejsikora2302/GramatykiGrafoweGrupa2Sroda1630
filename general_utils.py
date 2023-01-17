import networkx as nx
from copy import copy
import matplotlib.pyplot as plt
import os


class Attribute:
    LEVEL = "level"
    LABEL = "label"
    X = "x"
    Y = "y"


def create_folder_tree(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)
        
def debug_print(graph: nx.Graph):
    print(graph)
    for node in graph.nodes:
        print(node, graph.nodes[node])
    print("="*100)

def draw(graph: nx.Graph, level: int = None, filename: str = "test_draw.png") -> None:
    # debug_print(graph)

    create_folder_tree(filename)

    if level is not None:
        graph = graph.subgraph(
            [
                node
                for node in graph.nodes
                if graph.nodes[node][Attribute.LEVEL] == level
            ]
        )

    xs = nx.get_node_attributes(graph, Attribute.X)
    ys = nx.get_node_attributes(graph, Attribute.Y)
    label_attr = nx.get_node_attributes(graph, Attribute.LABEL)
    levels = nx.get_node_attributes(graph, Attribute.LEVEL)

    max_level = max(levels.values())
    pos = {
        node: (
            graph.nodes[node][Attribute.X],
            graph.nodes[node][Attribute.Y]
            + (max_level - graph.nodes[node][Attribute.LEVEL]) * 2,
        )
        for node in graph.nodes
    }

    pos_labels = copy(pos)
    for node in graph.nodes():
        pos_labels[node] = (pos[node][0], pos[node][1] + 0.3)

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

    plt.figure(figsize=(12, 4 + 8 * max_level))

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


def save_graph(g: nx.Graph, filename: str):
    # add attribute to all nodes
    graph = g.copy()
    create_folder_tree(filename)
    for node in graph.nodes:
        graph.nodes[node]["node_type"] = graph.nodes[node][Attribute.LABEL]
        graph.nodes[node][Attribute.X] += graph.nodes[node][Attribute.LEVEL] * 50
        graph.nodes[node][Attribute.Y] += graph.nodes[node][Attribute.LEVEL] * 50
    nx.write_gexf(graph, filename)
