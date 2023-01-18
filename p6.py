import networkx as nx
from graph_functions import *


def p6(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    left_side_graph.add_nodes_from(
        [
            (0, dict(label="i")),
            (1, dict(label="i")),
            (2, dict(label="E")),
            (3, dict(label="E")),
            (4, dict(label="I", level=1)),
            (5, dict(label="I", level=1)),
            (6, dict(label="E", level=1)),
            (7, dict(label="E", level=1)),
            (8, dict(label="E", level=1)),
            (9, dict(label="I", level=1)),
            (10, dict(label="I", level=1)),
            (11, dict(label="E", level=1)),
            (12, dict(label="E", level=1)),
            (13, dict(label="E", level=1)),
        ]
    )

    left_side_graph.add_edges_from(
        [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 3),
            (0, 4),
            (0, 5),
            (1, 9),
            (1, 10),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (6, 7),
            (7, 8),
            (9, 11),
            (9, 12),
            (10, 12),
            (10, 13),
            (11, 12),
            (12, 13),
        ]
    )

    constraints = [
        {"first_node": 6, "second_node": 8, "constrained_middle_node": 7},
        {"first_node": 11, "second_node": 13, "constrained_middle_node": 12},
        {"node": 6, "constrained_equal_node": 11},
        {"node": 7, "constrained_equal_node": 12},
        {"node": 8, "constrained_equal_node": 13},
    ]

    isomorphic_mapping = find_isomorphic_wrapper(
        graph, left_side_graph, level=level, constraints=constraints
    )

    if not isomorphic_mapping:
        return

    X = [0] * 14
    Y = [0] * 14
    levels = [0] * 14
    for t_node, g_node in isomorphic_mapping.items():
        X[t_node - 1] = graph.nodes[g_node][Attribute.X]
        Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]
        levels[t_node - 1] = graph.nodes[g_node][Attribute.LEVEL]

    merge_nodes(
        graph,
        [isomorphic_mapping[6], isomorphic_mapping[11]],
        (isomorphic_mapping[6], dict(label="E", x=X[6], y=Y[6], level=levels[6])),
    )
    merge_nodes(
        graph,
        [isomorphic_mapping[7], isomorphic_mapping[12]],
        (isomorphic_mapping[7], dict(label="E", x=X[7], y=Y[7], level=levels[7])),
    )
    merge_nodes(
        graph,
        [isomorphic_mapping[8], isomorphic_mapping[13]],
        (isomorphic_mapping[8], dict(label="E", x=X[8], y=Y[8], level=levels[8])),
    )


def p6_b(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    left_side_graph.add_nodes_from(
        [
            (0, dict(label="I", level=1)),
            (1, dict(label="I", level=1)),
            (2, dict(label="E", level=1)),
            (3, dict(label="E", level=1)),
            (4, dict(label="E", level=1)),
            (5, dict(label="I", level=1)),
            (6, dict(label="I", level=1)),
            (7, dict(label="E", level=1)),
            (8, dict(label="E", level=1)),
            (9, dict(label="E", level=1)),
        ]
    )

    left_side_graph.add_edges_from(
        [
            (0, 2),
            (0, 3),
            (1, 3),
            (1, 4),
            (2, 3),
            (3, 4),
            (5, 7),
            (5, 8),
            (6, 8),
            (6, 9),
            (7, 8),
            (8, 9),
        ]
    )

    constraints = [
        {"first_node": 2, "second_node": 4, "constrained_middle_node": 3},
        {"first_node": 7, "second_node": 9, "constrained_middle_node": 8},
        {"node": 2, "constrained_equal_node": 7},
        {"node": 3, "constrained_equal_node": 8},
        {"node": 4, "constrained_equal_node": 9},
    ]

    isomorphic_mapping = find_isomorphic_wrapper(
        graph, left_side_graph, level=level, constraints=constraints
    )

    print(isomorphic_mapping)

    if not isomorphic_mapping:
        return

    X = [0] * 10
    Y = [0] * 10
    levels = [0] * 10
    for t_node, g_node in isomorphic_mapping.items():
        X[t_node] = graph.nodes[g_node][Attribute.X]
        Y[t_node] = graph.nodes[g_node][Attribute.Y]
        levels[t_node] = graph.nodes[g_node][Attribute.LEVEL]

    merge_nodes(
        graph,
        [isomorphic_mapping[4], isomorphic_mapping[9]],
        (isomorphic_mapping[4], dict(label="E", x=X[4], y=Y[4], level=levels[4])),
    )
    merge_nodes(
        graph,
        [isomorphic_mapping[3], isomorphic_mapping[8]],
        (isomorphic_mapping[3], dict(label="E", x=X[3], y=Y[3], level=levels[3])),
    )

    merge_nodes(
        graph,
        [isomorphic_mapping[2], isomorphic_mapping[7]],
        (isomorphic_mapping[2], dict(label="E", x=X[2], y=Y[2], level=levels[2])),
    )
