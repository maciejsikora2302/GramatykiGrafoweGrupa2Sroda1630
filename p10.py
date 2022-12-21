import networkx as nx
from graph_functions import *


def p10(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    # parent I node (from the upper level) idx = 0
    left_side_graph.add_nodes_from([
        (0, dict(label='i')),
        (1, dict(label='i')),
        (2, dict(label='E')),
        (3, dict(label='E')),
        (4, dict(label='I')),
        (5, dict(label='I')),
        (6, dict(label='I')),
        (7, dict(label='E')),
        (8, dict(label='E')),
        (9, dict(label='E')),
        (10, dict(label='E')),
        (11, dict(label='E'))
    ])
    left_side_graph.add_edges_from([
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
    ])

    constraints = [
        {'first_node': 7, 'second_node': 8, 'constrained_middle_node': 9},
        {'first_node': 2, 'second_node': 7, 'same': True},
        {'first_node': 2, 'second_node': 10, 'same': True},
        {'first_node': 3, 'second_node': 9, 'same': True},
        {'first_node': 3, 'second_node': 11, 'same': True},
    ]

    try:
        isomorphic_mapping = find_isomorphic_wrapper(graph, left_side_graph, level=level, constraints=constraints)
    except Exception:
        return

    right_side_parent_node = (0, dict(label='i', x=None, y=None, level=level))

    # lists are indexed by nodes in template, so (1,2,3,4,5), minus 1 to start from 0
    X = [0] * 12
    Y = [0] * 12
    for t_node, g_node in isomorphic_mapping.items():
        if graph.nodes[g_node][Attribute.LABEL] == 'E':
            X[t_node - 1] = graph.nodes[g_node][Attribute.X]
            Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]

    right_side_nodes_new = [
        # copy existing E nodes
        (1, dict(label='i')),
        (2, dict(label='E', x=X[1], y=Y[1])),
        (3, dict(label='E', x=X[2], y=Y[2])),
        (4, dict(label='I')),
        (5, dict(label='I')),
        (6, dict(label='I')),
        # remade bottom nodes
        (7, dict(label='E', x=X[6], y=Y[6])),
        (8, dict(label='E', x=X[7], y=Y[7])),
        (9, dict(label='E', x=X[8], y=Y[8])),
    ]

    right_side_edges = [
        (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),  # top square
        (0, 4), (0, 5), (1, 6),  # hanging down
        (4, 7), (4, 8), (5, 8), (5, 9), (6, 7), (6, 9),  # lower I to e
        (7, 8), (8, 9),  # inter E
    ]

    add_to_graph(graph, isomorphic_mapping, right_side_parent_node, right_side_nodes_new, right_side_edges)
