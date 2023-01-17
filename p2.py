import networkx as nx
from graph_functions import *
from general_utils import Attribute


def p2(graph: nx.Graph, level: int) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 2137
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

    X = [0] * 3
    Y = [0] * 3

    for t_node, g_node in isomorphic_mapping.items():
        if graph.nodes[g_node][Attribute.LABEL] == "E":
            # E-nodes in template are indexed from 1 to 3, so shifting them down by 1 makes them legal indices
            X[t_node - 1] = graph.nodes[g_node][Attribute.X]
            Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]

    # calulate distance between all endes from X and Y and find the longest one
    # longest_edge stores distance and indices of nodes from template graph
    longest_edge = (-1.0, -1, -1)
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            dist = ((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** 0.5
            if dist > longest_edge[0]:
                longest_edge = (dist, i+1, j+1)
    
    # position node 1 opposite to the longest edge, then this edge lies between nodes 2 and 3
    # to achieve this, swap 1 with node that currently opposes the longest edge
    opposite_node = 6 - longest_edge[1] - longest_edge[2]    # 1 + 2 + 3 = 6
    isomorphic_mapping[1], isomorphic_mapping[opposite_node] = isomorphic_mapping[opposite_node], isomorphic_mapping[1]

    # reassign attributes after permutting keys
    for t_node, g_node in isomorphic_mapping.items():
        if graph.nodes[g_node][Attribute.LABEL] == "E":
            # E-nodes in template are indexed from 1 to 3, so shifting them down by 1 makes them legal indices
            X[t_node - 1] = graph.nodes[g_node][Attribute.X]
            Y[t_node - 1] = graph.nodes[g_node][Attribute.Y]

    # new node
    X.append((X[1] + X[2]) / 2)
    Y.append((Y[1] + Y[2]) / 2)

    right_side_parent_node = (parent_tmp_node_number, dict(label="i"))
    right_side_nodes_new = [
        (1, dict(label="I", x=(X[0] + X[1] + X[3]) / 3, y=(Y[0] + Y[1] + Y[3]) / 3)),
        (2, dict(label="I", x=(X[0] + X[2] + X[3]) / 3, y=(Y[0] + Y[2] + Y[3]) / 3)),
        (3, dict(label="E", x=X[0], y=Y[0])),
        (4, dict(label="E", x=X[1], y=Y[1])),
        (5, dict(label="E", x=X[2], y=Y[2])),
        (6, dict(label="E", x=X[3], y=Y[3])),
    ]

    right_side_edges = [
        # boundary edges
        (3, 4),
        (4, 6),
        (6, 5),
        (5, 3),
        # internal edge to new node
        (3, 6),
        # hiperedges to I-node
        (1, 3),
        (1, 4),
        (1, 6),
        # hiperedges to I-node
        (2, 3),
        (2, 5),
        (2, 6),
    ]

    add_to_graph(
        graph,
        isomorphic_mapping,
        right_side_parent_node,
        right_side_nodes_new,
        right_side_edges,
    )
