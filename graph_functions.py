import networkx as nx
import typing
from general_utils import Attribute

def find_parents(graph: nx.Graph, level: int, label: str) -> list:
    parents = []
    for node in graph.nodes:
        if graph.nodes[node][Attribute.LEVEL] == level - 1 and graph.nodes[node][Attribute.LABEL] == label:
            parents.append(node)
    return parents

def node_comparator(found_node, searched_node) -> bool:
    return found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]
    # return found_node[Attribute.LEVEL] == searched_node[Attribute.LEVEL] and found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]

def node_comparator_factory(level: int) -> typing.Callable:
    def node_comparator(found_node, searched_node) -> bool:
        return found_node[Attribute.LEVEL] == level and found_node[Attribute.LABEL] == searched_node[Attribute.LABEL]

    return node_comparator


def find_isomporphic(graph: nx.Graph, left_side_graph: nx.Graph, level: int) -> dict:
    isomorphic_graphs = []
    graph_matcher = nx.algorithms.isomorphism.GraphMatcher(graph, left_side_graph, node_match=node_comparator_factory(level))
    for isomorphic_graph in graph_matcher.subgraph_isomorphisms_iter():
        isomorphic_graphs.append(isomorphic_graph)
    return isomorphic_graphs

def find_isomporphic_wrapper(graph: nx.Graph, left_side_graph: nx.Graph, level: int) -> dict:
    return find_isomporphic(graph, left_side_graph, level)

def add_to_graph(
    graph: nx.Graph, 
    isomorphic_mapping: dict, 
    right_side_parent_node: tuple, 
    right_side_nodes_new: list, 
    right_side_edges: list
    ):
    parent_tmp_node_number = right_side_parent_node[0]

    isomorphic_mapping_reverse = {v: k for k, v in isomorphic_mapping.items()}

    n = len(graph.nodes)
    right_side_nodes_mapping = { node[0]: node[0] + n for node in right_side_nodes_new } # define a dictionay mapping old node number (based on right_side_nodes ) => graph node.
    right_side_nodes_mapping[parent_tmp_node_number] = isomorphic_mapping_reverse[parent_tmp_node_number]
        

    right_side_edges_mapped = list(
        map(lambda edge: (right_side_nodes_mapping[edge[0]], right_side_nodes_mapping[edge[1]]), right_side_edges))

    right_side_nodes_mapped = list(
        map(lambda node: (right_side_nodes_mapping[node[0]], node[1]), right_side_nodes_new))
    
    existing_node_parent = graph.nodes[isomorphic_mapping_reverse[parent_tmp_node_number]]

    for node in right_side_nodes_mapped:
        node[1][Attribute.LEVEL] = existing_node_parent[Attribute.LEVEL] + 1

    graph.nodes[isomorphic_mapping_reverse[parent_tmp_node_number]][Attribute.LABEL] = right_side_parent_node[1][Attribute.LABEL]

    graph.add_nodes_from(right_side_nodes_mapped)
    graph.add_edges_from(right_side_edges_mapped)