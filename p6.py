import networkx as nx
from graph_functions import *

def p6(graph: nx.Graph, level: int) -> None:
    left_side_graph = nx.Graph()

    left_side_graph.add_nodes_from([
        (0, dict(label='i')),
        (1, dict(label='i')),
        (2, dict(label='E')),
        (3, dict(label='E')),
        (4, dict(label='I', level=1)),
        (5, dict(label='I', level=1)),
        (6, dict(label='E', level=1)),
        (7, dict(label='E', level=1)),
        (8, dict(label='E', level=1)),
        (9, dict(label='I', level=1)),
        (10, dict(label='I', level=1)),
        (11, dict(label='E', level=1)),
        (12, dict(label='E', level=1)),
        (13, dict(label='E', level=1)),
    ])

    left_side_graph.add_edges_from([
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (0, 4),
        (0, 5),
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
    ])

    constraints = [
        {'first_node': 6, 'second_node': 8, 'constrained_middle_node': 7},
        {'first_node': 11, 'second_node': 13, 'constrained_middle_node': 12}
    ]

    isomorphic_mapping = find_isomorphic_wrapper(graph, left_side_graph, level=level, constraints=constraints)

    if not isomorphic_mapping:
        return

    X = [0] * 14
    Y = [0] * 14
    levels = [0] * 14
    for t_node, g_node in isomorphic_mapping.items():
        X[t_node - 1] = graph.nodes[g_node][Attribute.X]
        Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]
        levels[t_node - 1] = graph.nodes[g_node][Attribute.LEVEL]

    merge_nodes(graph, [isomorphic_mapping[6], isomorphic_mapping[11]], (14, dict(label='E', x=X[6], y=Y[6], level=levels[6])))
    merge_nodes(graph, [isomorphic_mapping[7], isomorphic_mapping[12]], (15, dict(label='E', x=X[6], y=Y[6], level=levels[6])))
    merge_nodes(graph, [isomorphic_mapping[8], isomorphic_mapping[13]], (16, dict(label='E', x=X[6], y=Y[6], level=levels[6])))
