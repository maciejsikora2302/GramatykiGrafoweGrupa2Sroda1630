import networkx as nx
from graph_functions import *


def p10(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    # parent I node (from the upper level) idx = 0
    left_side_graph.add_nodes_from(
        [
            (0, dict(label="i")),
            (1, dict(label="i")),
            (2, dict(label="E")),
            (3, dict(label="E")),
            (4, dict(label="I", level=1)),
            (5, dict(label="I", level=1)),
            (6, dict(label="I", level=1)),
            (7, dict(label="E", level=1)),
            (8, dict(label="E", level=1)),
            (9, dict(label="E", level=1)),
            (10, dict(label="E", level=1)),
            (11, dict(label="E", level=1)),
        ]
    )
    left_side_graph.add_edges_from(
        [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (2, 3),
            (0, 4),
            (0, 5),
            (1, 6),
            (4, 7),
            (4, 8),
            (5, 8),
            (5, 9),
            (6, 10),
            (6, 11),
            (7, 8),
            (8, 9),
            (10, 11),
        ]
    )

    constraints = [
        {"first_node": 7, "second_node": 9, "constrained_middle_node": 8},
        {"node": 2, "constrained_equal_node": 7},
        {"node": 2, "constrained_equal_node": 10},
        {"node": 3, "constrained_equal_node": 9},
        {"node": 3, "constrained_equal_node": 11},
    ]

    isomorphic_mapping = find_isomorphic_wrapper(graph, left_side_graph, level=level, constraints=constraints)

    if not isomorphic_mapping:
        return

    X = [0] * 12
    Y = [0] * 12
    levels = [0] * 12
    for t_node, g_node in isomorphic_mapping.items():
        X[t_node - 1] = graph.nodes[g_node][Attribute.X]
        Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]
        levels[t_node - 1] = graph.nodes[g_node][Attribute.LEVEL]

    merge_nodes(
        graph,
        [isomorphic_mapping[7], isomorphic_mapping[10]],
        (isomorphic_mapping[7], dict(label="E", x=X[7], y=Y[7], level=levels[7])),
    )
    merge_nodes(
        graph,
        [isomorphic_mapping[9], isomorphic_mapping[11]],
        (isomorphic_mapping[9], dict(label="E", x=X[9], y=Y[9], level=levels[9])),
    )

    graph.remove_edge(isomorphic_mapping[7], isomorphic_mapping[9])
