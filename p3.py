import networkx as nx
from graph_functions import *
from general_utils import Attribute
from pprint import pprint as pp

def p3(graph: nx.Graph, level: int, test: bool = None) -> None:
    left_production_side_graph = nx.Graph()

    parent_tmp_node_number = 0
    left_production_side_graph.add_nodes_from([
        (parent_tmp_node_number, dict(label='I')),
        (1, dict(label='E')),
        (2, dict(label='E')),
        (3, dict(label='E')),
        (4, dict(label='E'))
    ])
    left_production_side_graph.add_edges_from([
        (parent_tmp_node_number, 1),
        (parent_tmp_node_number, 2),
        (parent_tmp_node_number, 3),
        (1, 2),
        (2, 3),
        (3, 4),
        (1, 4)
    ])

    # draw(left_production_side_graph)

    constraints = [
        {'first_node': 1, 'second_node': 3, 'constrained_middle_node': 4},
    ]

    try:
        isomorphic_mapping = find_isomporphic_wrapper(graph, left_production_side_graph, level=level, constraints=constraints)
        if test:
            pp(isomorphic_mapping)
            return len(isomorphic_mapping)
        isomorphic_mapping = isomorphic_mapping[0]
    except IndexError:
        print('No isomorphic mapping found for p3')
        return

def p3_test():
    
    low = 1.0
    high = 40.0

    g = nx.Graph()

    parent_tmp_node_number = 0
    g.add_nodes_from([
        (parent_tmp_node_number, dict(label='I', x=1.0, y=1.0, level=1)),
        (1, dict(label='E', x=low, y=low, level=1)),
        (2, dict(label='E', x=high, y=low, level=1)),
        (3, dict(label='E', x=high, y=high, level=1)),
        (4, dict(label='E', x=(high+low)/2, y=(high+low)/2, level=1))
    ])
    g.add_edges_from([
        (parent_tmp_node_number, 1),
        (parent_tmp_node_number, 2),
        (parent_tmp_node_number, 3),
        (1, 2),
        (2, 3),
        (3, 4),
        (1, 4)
    ])

    if p3(g, 1, test=True) == 2:
        print('p3 test passed')