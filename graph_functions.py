import networkx as nx
import typing
import numpy as np
from general_utils import Attribute, draw
from pprint import pprint as pp

def find_parents(graph: nx.Graph, level: int, label: str) -> list:
    parents = []
    for node in graph.nodes:
        if graph.nodes[node][Attribute.LEVEL] == level - 1 and graph.nodes[node][Attribute.LABEL] == label:
            parents.append(node)
    return parents

def node_comparator(found_node, searched_node) -> bool:
    return found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]

def node_comparator_factory(level: int) -> typing.Callable:
    def node_comparator(found_node, searched_node) -> bool:
        desired_level = level + searched_node.get(Attribute.LEVEL, 0)
        return found_node[Attribute.LEVEL] == desired_level and found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]

    return node_comparator


def find_isomporphic(graph: nx.Graph, left_side_graph: nx.Graph, level: int) -> dict:
    isomorphic_graphs = []
    graph_matcher = nx.algorithms.isomorphism.GraphMatcher(graph, left_side_graph, node_match=node_comparator_factory(level))
    for isomorphic_graph in graph_matcher.subgraph_isomorphisms_iter():
        # mapping should be directed from template to real graph:
        inversed_isomorphism = {v: k for k, v in isomorphic_graph.items()}
        isomorphic_graphs.append(inversed_isomorphism)
    return isomorphic_graphs

def find_isomorphic_wrapper(graph: nx.Graph, left_side_graph: nx.Graph, level: int, constraints: list = None) -> dict:
    '''
    constraints refer to node in left_side_graph.
    Example constraints:
        [{
            'first_node': 1,
            'second_node': 2,
            'constrained_middle_node': 3
        }]
    
    x of 'constrained_middle_node' == (x of 'first_node' + x of 'second_node') / 2
    y of 'constrained_middle_node' == (y of 'first_node' + y of 'second_node') / 2
    '''
    def predicate(mapping):
        eps = 1e-4

        checked_constraints = [False for _ in range(len(constraints))]

        for i, constraint in enumerate(constraints):
            first_node = graph.nodes[mapping[constraint['first_node']]]
            second_node = graph.nodes[mapping[constraint['second_node']]]
            expected_node = graph.nodes[mapping[constraint['constrained_middle_node']]]
            x1, y1 = first_node[Attribute.X], first_node[Attribute.Y]
            x2, y2 = second_node[Attribute.X], second_node[Attribute.Y]
            x3, y3 = expected_node[Attribute.X], expected_node[Attribute.Y]
            if (np.abs((x1 + x2) / 2 - x3) < eps and np.abs((y1 + y2) / 2 - y3) < eps):
                checked_constraints[i] = True

        # pp(checked_constraints)
        return all(checked_constraints)


    initially_found = find_isomporphic(graph, left_side_graph, level)

    #modify later here to add ability to choose which mapping to use
    try:
        return initially_found[0] if constraints is None else list(filter(predicate, initially_found))[0]
    except IndexError as e:
        return None

def add_to_graph(
    graph: nx.Graph, 
    isomorphic_mapping: dict, 
    right_side_parent_node: tuple, 
    right_side_nodes_new: list, 
    right_side_edges: list
    ):
    parent_tmp_node_number = right_side_parent_node[0]

    n = len(graph.nodes)
    right_side_nodes_mapping = { node[0]: node[0] + n for node in right_side_nodes_new } # define a dictionay mapping old node number (based on right_side_nodes ) => graph node.
    right_side_nodes_mapping[parent_tmp_node_number] = isomorphic_mapping[parent_tmp_node_number]

    right_side_edges_mapped = list(
        map(lambda edge: (right_side_nodes_mapping[edge[0]], right_side_nodes_mapping[edge[1]]), right_side_edges))

    right_size_edges_to_parent = [
        (isomorphic_mapping[parent_tmp_node_number], right_side_nodes_mapping[node[0]])
        for node in list(filter(lambda node: node[1][Attribute.LABEL] == 'I', right_side_nodes_new))
    ]

    right_side_edges_mapped = right_side_edges_mapped + right_size_edges_to_parent

    right_side_nodes_mapped = list(
        map(lambda node: (right_side_nodes_mapping[node[0]], node[1]), right_side_nodes_new))
    
    existing_node_parent = graph.nodes[isomorphic_mapping[parent_tmp_node_number]]

    for node in right_side_nodes_mapped:
        node[1][Attribute.LEVEL] = existing_node_parent[Attribute.LEVEL] + 1

    graph.nodes[isomorphic_mapping[parent_tmp_node_number]][Attribute.LABEL] = right_side_parent_node[1][Attribute.LABEL]

    graph.add_nodes_from(right_side_nodes_mapped)
    graph.add_edges_from(right_side_edges_mapped)

def merge_nodes(graph: nx.Graph, nodes: list, new_node: tuple):    
    graph.add_node(new_node)
    
    for n1,n2,data in graph.edges(data=True):
        if n1 in nodes:
            graph.add_edge(new_node,n2,data)
        elif n2 in nodes:
            graph.add_edge(n1,new_node,data)
    
    for n in nodes:
        graph.remove_node(n)