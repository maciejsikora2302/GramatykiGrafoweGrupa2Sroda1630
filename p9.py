from graph_functions import *
from general_utils import Attribute


def p9(graph: nx.Graph, level: int) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 8
    left_production_side_graph.add_nodes_from(
        [
            (parent_tmp_node_number, dict(label="I")),
            (1, dict(label="E")),
            (2, dict(label="E")),
            (3, dict(label="E")),
        ]
    )
    left_production_side_graph.add_edges_from(
        [
            (parent_tmp_node_number, 1),
            (parent_tmp_node_number, 2),
            (parent_tmp_node_number, 3),
            (1, 2),
            (1, 3),
            (2, 3),
        ]
    )

    isomorphic_mapping = find_isomorphic_wrapper(
        graph, left_production_side_graph, level=level
    )

    if not isomorphic_mapping:
        return

    X = []
    Y = []
    for _, node in isomorphic_mapping.items():
        if graph.nodes[node][Attribute.LABEL] == "E":
            X.append(graph.nodes[node][Attribute.X])
            Y.append(graph.nodes[node][Attribute.Y])

    right_side_parent_node = (parent_tmp_node_number, dict(label="i"))
    right_side_nodes_new = [
        (1, dict(label="I", x=(X[0] + X[1] + X[2]) / 3, y=(Y[0] + Y[1] + Y[2]) / 3)),
        (2, dict(label="E", x=X[0], y=Y[0])),
        (3, dict(label="E", x=X[1], y=Y[1])),
        (4, dict(label="E", x=X[2], y=Y[2])),
    ]

    right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    right_side_edges = [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 3),
        (2, 4),
        (3, 4),
    ]

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from(right_side_nodes)
    right_production_side.add_edges_from(right_side_edges)

    add_to_graph(
        graph,
        isomorphic_mapping,
        right_side_parent_node,
        right_side_nodes_new,
        right_side_edges,
    )
