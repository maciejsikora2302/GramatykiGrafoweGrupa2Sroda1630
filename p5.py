import networkx as nx
from graph_functions import *


def p5(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    # parent I node (from the upper level) idx = 0
    left_side_graph.add_nodes_from(
        [
            (0, dict(label="I")),
            (1, dict(label="E")),
            (2, dict(label="E")),
            (3, dict(label="E")),
            (4, dict(label="E")),
            (5, dict(label="E")),
            (6, dict(label="E")),
        ]
    )
    left_side_graph.add_edges_from(
        [(0, 1), (0, 2), (0, 4), (1, 6), (2, 6), (2, 3), (3, 4), (4, 5), (5, 1)]
    )

    constraints = [
        {"first_node": 2, "second_node": 4, "constrained_middle_node": 3},
        {"first_node": 1, "second_node": 4, "constrained_middle_node": 5},
        {"first_node": 1, "second_node": 2, "constrained_middle_node": 6},
    ]

    isomorphic_mapping = find_isomorphic_wrapper(
        graph, left_side_graph, level=level, constraints=constraints
    )

    if not isomorphic_mapping:
        return

    right_side_parent_node = (0, dict(label="i", x=None, y=None, level=level))

    # lists are indexed by nodes in template, so (1,2,3,4,5), minus 1 to start from 0
    X = [0] * 6
    Y = [0] * 6
    for t_node, g_node in isomorphic_mapping.items():
        if graph.nodes[g_node][Attribute.LABEL] == "E":
            X[t_node - 1] = graph.nodes[g_node][Attribute.X]
            Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]

    right_side_nodes_new = [
        # copy existing E nodes
        (1, dict(label="E", x=X[0], y=Y[0])),
        (2, dict(label="E", x=X[1], y=Y[1])),
        (3, dict(label="E", x=X[2], y=Y[2])),
        (4, dict(label="E", x=X[3], y=Y[3])),
        (5, dict(label="E", x=X[4], y=Y[4])),
        (6, dict(label="E", x=X[5], y=Y[5])),
        # add new internal I nodes
        (7, dict(label="I", x=(X[0] + X[5] + X[4]) / 3, y=(Y[0] + Y[5] + Y[4]) / 3)),
        (8, dict(label="I", x=(X[1] + X[2] + X[4]) / 3, y=(Y[1] + Y[2] + Y[4]) / 3)),
        (9, dict(label="I", x=(X[2] + X[3] + X[4]) / 3, y=(Y[2] + Y[3] + Y[4]) / 3)),
        (10, dict(label="I", x=(X[1] + X[5] + X[4]) / 3, y=(Y[1] + Y[5] + Y[4]) / 3)),
    ]

    right_side_edges = [
        (1, 6),
        (6, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 1),  # boundary edges
        (2, 5),
        (3, 5),
        (6, 5),  # new interal edges
        (1, 7),
        (5, 7),
        (6, 7),  # hiperedges of <1,5,6> triangle
        (2, 8),
        (3, 8),
        (5, 8),  # hiperedges of <2,3,5> triangle
        (3, 9),
        (4, 9),
        (5, 9),  # hiperedges of <3,4,5> triangle
        (2, 10),
        (5, 10),
        (6, 10),  # hiperedges of <2,5,6> triangle
    ]

    add_to_graph(
        graph,
        isomorphic_mapping,
        right_side_parent_node,
        right_side_nodes_new,
        right_side_edges,
    )
