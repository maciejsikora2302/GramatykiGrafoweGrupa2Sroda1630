import networkx as nx
from graph_functions import *


def p1(graph: nx.Graph, level: int, low: float = 0.0, high: float = 1.0):
    left_production_side_graph = nx.Graph()
    parent_tmp_node_number = 8

    left_production_side_graph.add_nodes_from(
        [(parent_tmp_node_number, dict(label="El", level=0))]
    )

    right_side_parent_node = (
        parent_tmp_node_number,
        dict(label="el", x=None, y=None, level=level),
    )
    right_side_nodes_new = [
        (1, dict(label="I", x=(2 * low + high) / 3, y=(2 * low + high) / 3, level=1)),
        (2, dict(label="I", x=(low + 2 * high) / 3, y=(low + 2 * high) / 3, level=1)),
        (3, dict(label="E", x=low, y=low, level=1)),
        (4, dict(label="E", x=high, y=low, level=1)),
        (5, dict(label="E", x=high, y=high, level=1)),
        (6, dict(label="E", x=low, y=high, level=1)),
    ]

    right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    right_side_edges = [
        (3, 4),
        (3, 6),
        (3, 1),
        (4, 5),
        (4, 6),
        (4, 1),
        (4, 2),
        (5, 2),
        (5, 6),
        (6, 1),
        (6, 2),
    ]

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from(right_side_nodes)
    right_production_side.add_edges_from(right_side_edges)

    isomorphic_mapping = find_isomorphic_wrapper(
        graph, left_production_side_graph, level
    )

    if not isomorphic_mapping:
        return

    add_to_graph(
        graph,
        isomorphic_mapping,
        right_side_parent_node,
        right_side_nodes_new,
        right_side_edges,
    )
