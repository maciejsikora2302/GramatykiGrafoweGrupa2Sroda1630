import networkx as nx
from graph_functions import *
from general_utils import Attribute


def p2(graph: nx.Graph, level: int) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 0
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

    # print(isomorphic_mapping)

    if not isomorphic_mapping:
        return

    X = []
    Y = []
    node_added = []
    for _, node in isomorphic_mapping.items():
        if graph.nodes[node][Attribute.LABEL] == "E":
            X.append(graph.nodes[node][Attribute.X])
            Y.append(graph.nodes[node][Attribute.Y])
            node_added.append(node)

    # calulate distance between all endes from X and Y
    # and find the longest one
    distance = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            dist = ((X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2) ** 0.5
            distance.append((dist, i, j))
    distance.sort(key=lambda x: x[0], reverse=True)
    max_distance_i = distance[0][1]
    max_distance_j = distance[0][2]

    new_e_x = (X[max_distance_i] + X[max_distance_j]) / 2
    new_e_y = (Y[max_distance_i] + Y[max_distance_j]) / 2
    X.append(new_e_x)
    Y.append(new_e_y)

    right_side_parent_node = (parent_tmp_node_number, dict(label="i"))
    right_side_nodes_new = [
        (1, dict(label="I", x=(X[0] + X[1] + X[2]) / 3, y=(Y[0] + Y[1] + Y[2]) / 3)),
        (2, dict(label="I", x=(X[1] + X[2] + X[3]) / 3, y=(Y[1] + Y[2] + Y[3]) / 3)),
        (3, dict(label="E", x=X[0], y=Y[0])),
        (4, dict(label="E", x=X[1], y=Y[1])),
        (5, dict(label="E", x=X[2], y=Y[2])),
        (6, dict(label="E", x=X[3], y=Y[3])),
    ]

    right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    right_side_edges = [
        (3, 4),
        (3, 6),
        (3, 5),
        (4, 5),
        (4, 6),
        (5, 6),

        (3, 1),
        (5, 2),

        (4, 1),
        (4, 2),

        (6, 1),
        (6, 2),
    ]

    if (node_added[max_distance_i], node_added[max_distance_j]) in right_side_edges:
        # print((node_added[max_distance_i], node_added[max_distance_j]))
        right_side_edges.remove(
            (node_added[max_distance_i], node_added[max_distance_j])
        )
    elif (node_added[max_distance_j], node_added[max_distance_i]) in right_side_edges:
        # print((node_added[max_distance_j], node_added[max_distance_i]))
        right_side_edges.remove(
            (node_added[max_distance_j], node_added[max_distance_i])
        )

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from(right_side_nodes)
    right_production_side.add_edges_from(right_side_edges)

    # from pprint import pprint as pp
    # for node in right_side_nodes:
    #     pp(node)

    add_to_graph(
        graph,
        isomorphic_mapping,
        right_side_parent_node,
        right_side_nodes_new,
        right_side_edges,
    )
