import networkx as nx
from graph_functions import *
from general_utils import Attribute

def p2(graph: nx.Graph, level: int) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 8
    left_production_side_graph.add_nodes_from([
        (parent_tmp_node_number, dict(label='I')),
        (1, dict(label='E')),
        (2, dict(label='E')),
        (3, dict(label='E'))
    ])
    left_production_side_graph.add_edges_from([
        (parent_tmp_node_number, 1),
        (parent_tmp_node_number, 2),
        (parent_tmp_node_number, 3),
        (1, 2),
        (1, 3),
        (2, 3)
    ])

    isomorphic_mapping = find_isomorphic_wrapper(graph, left_production_side_graph, level=level)

    X = []
    Y = []
    for _, node in isomorphic_mapping.items():
        if graph.nodes[node][Attribute.LABEL] == 'E':
            X.append(graph.nodes[node][Attribute.X])
            Y.append(graph.nodes[node][Attribute.Y])
        
    new_e_x = (X[0] + X[2]) / 2
    new_e_y = (Y[0] + Y[2]) / 2
    X.append(new_e_x)
    Y.append(new_e_y)

    right_side_parent_node = (parent_tmp_node_number, dict(label='i'))
    right_side_nodes_new = [
        (1, dict(label='I', x=(X[0] + X[1] + X[2]) / 3, y=(Y[0] + Y[1] + Y[2]) / 3)),
        (2, dict(label='I', x=(X[1] + X[2] + X[3]) / 3, y=(Y[1] + Y[2] + Y[3]) / 3)),
        (3, dict(label='E', x=X[0], y=Y[0])),
        (4, dict(label='E', x=X[1], y=Y[1])),
        (5, dict(label='E', x=X[2], y=Y[2])),
        (6, dict(label='E', x=X[3], y=Y[3]))
    ]

    right_side_nodes = [right_side_parent_node] + right_side_nodes_new

    right_side_edges = [
        (3,4), (3,6), (3,1), (4,5), (4,6), (4,1), (4,2), (5,2), (5,6), (6,1), (6,2),
    ]

    right_production_side = nx.Graph()
    right_production_side.add_nodes_from(right_side_nodes)
    right_production_side.add_edges_from(right_side_edges)


    add_to_graph(graph, isomorphic_mapping, right_side_parent_node, right_side_nodes_new, right_side_edges)

